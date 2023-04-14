from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class MyImagesPipeline(ImagesPipeline):

    @classmethod
    def from_settings(cls, settings):
        gcs_store = cls.STORE_SCHEMES['gs']
        gcs_store.GCS_PROJECT_ID = settings['GCS_PROJECT_ID']
        gcs_store.POLICY = settings['IMAGES_STORE_GCS_ACL'] or None
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        if adapter.get('title') and adapter.get('slug') and adapter.get('image_urls'):
            if adapter.get('name') and adapter.get('numPages') and adapter.get('image_urls'):
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [Request(u, meta={'foldername': item.get('title'), 'filename': item.get('name')}) for u in urls]
            else:
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [Request(u, meta={'foldername': item.get('title')}) for u in urls]
        else:
            raise DropItem(f"Missing field in File-Path-Item:{item}")

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        if adapter.get('title') and adapter.get('slug') and adapter.get('image_urls'):
            if adapter.get('name') and adapter.get('numPages') and adapter.get('image_urls'):

                return '%s/%s/%s' % (request.meta['foldername'], request.meta['filename'], request.url.split('/')[-1])
            else:
                return '%s/%s' % (request.meta['foldername'], request.url.split('/')[-1])
        else:
            raise DropItem(f"Missing field in File-Path-Item:{item}")


class DownloaderImagesPipeline(ImagesPipeline):

    @classmethod
    def from_settings(cls, settings):
        # gcs_store = cls.STORE_SCHEMES['gs']
        # gcs_store.GCS_PROJECT_ID = settings['GCS_PROJECT_ID']
        # gcs_store.POLICY = settings['IMAGES_STORE_GCS_ACL'] or None
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        if adapter.get('title') and adapter.get('slug') and adapter.get('image_urls'):
            if adapter.get('name') and adapter.get('numPages') and adapter.get('image_urls'):
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [Request(u, meta={'foldername': item.get('title'), 'filename': item.get('name')}) for u in urls]
            else:
                urls = ItemAdapter(item).get(self.images_urls_field, [])
                return [Request(u, meta={'foldername': item.get('title')}) for u in urls]
        else:
            print(f"Missing field image_urls in :{item}")

    def file_path(self, request, response=None, info=None, *, item=None):
        import hashlib
        adapter = ItemAdapter(item)
        if adapter.get('title') and adapter.get('slug') and adapter.get('image_urls'):
            if adapter.get('name') and adapter.get('numPages') and adapter.get('image_urls'):

                image_url_hash = hashlib.shake_256(
                    request.url.encode()).hexdigest(5)
                return '%s/%s/%s%s' % (request.meta['foldername'], request.meta['filename'], image_url_hash, request.url.split('/')[-1])
            else:
                image_url_hash = hashlib.shake_256(
                    request.url.encode()).hexdigest(5)
                return '%s/%s%s' % (request.meta['foldername'], image_url_hash, request.url.split('/')[-1])
        else:
            print(f"Missing field in File-Path-Item:{item}")

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:

            raise DropItem("Item contains no images")
        adapter = ItemAdapter(item)
        adapter['image_paths'] = image_paths
        return item
