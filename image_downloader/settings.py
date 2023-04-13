from pathlib import Path
import sys
import os
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, 'core'))
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

BOT_NAME = 'image_downloader'

SPIDER_MODULES = ['image_downloader.spiders']
NEWSPIDER_MODULE = 'image_downloader.spiders'


USER_AGENT = "Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"

ROBOTSTXT_OBEY = False
# DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

ITEM_PIPELINES = {
    # 'image_downloader.pipelines.getimages.MyImagesPipeline': 1,
    'image_downloader.pipelines.getimages.DownloaderImagesPipeline': 300,
    'image_downloader.pipelines.cleanup.CrawlerPipeline': 400,
}


# IMAGES_STORE = 'gs://rhixescans/media/'
# GCS_PROJECT_ID = 'modified-badge-382221'
# IMAGES_STORE_GCS_ACL = 'publicRead'
IMAGES_STORE = 'media'
# IMAGES_URLS_FIELD = 'image_urls'
# IMAGES_RESULT_FIELD = 'images'
# IMAGES_EXPIRES = 30
MEDIA_ALLOW_REDIRECTS = True

SPIDER_MIDDLEWARES = {
    'image_downloader.middlewares.custommiddlewares.ImageDownloaderSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'image_downloader.middlewares.custommiddlewares.ImageDownloaderDownloaderMiddleware': 543,
}

# SPIDER_MIDDLEWARES = {
#     'image_downloader.middlewares.deltafetch.DeltaFetch': 100,
# }
# DELTAFETCH_ENABLED = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
# TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
TWISTED_REACTOR = ''
FEED_EXPORT_ENCODING = "utf-8"
