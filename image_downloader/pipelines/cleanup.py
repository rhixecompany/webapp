from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from django.db.models import Q
from Comics.models import Comic, Chapter, Page, Genre, Category


class CrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('title') and adapter.get('slug') and adapter.get('image_paths'):
            if adapter.get('title') and adapter.get('slug') and adapter.get('name') and adapter.get('numPages') and adapter.get('image_paths'):
                try:
                    com = Comic.objects.get(Q(slug__contains=item['slug']))
                    try:
                        chapter, created = Chapter.objects.filter(
                            Q(name__icontains=item['name'])
                        ).update_or_create(comic=com, name=item['name'], slug=item['chapterslug'], numPages=item['numPages'])
                    except:
                        raise DropItem(f"Duplicate Item Found{item}")
                    images = item['image_paths']
                    if images is not None:
                        for img in images:
                            page, created = Page.objects.filter(
                                Q(images__icontains=img)
                            ).update_or_create(chapter=chapter, images=img)
                            chapter.pages.add(page)
                            chapter.save()
                    else:
                        raise DropItem(f"Missing field in Chapter-Item:{item}")

                    return item
                except Comic.DoesNotExist:
                    raise DropItem(f"Missing field in Chapter-Data:{item}")
            else:
                images = item['image_paths']
                if images is not None:
                    for va1 in images:
                        genrelist = item.get('genre')
                        if item.get('category') and genrelist is not None:
                            try:
                                category, created = Category.objects.filter(
                                    Q(name__icontains=item['category'])
                                ).update_or_create(name=item['category'])
                                comic, created = Comic.objects.filter(
                                    Q(title__icontains=item['title']) |
                                    Q(slug__icontains=item['slug'])
                                ).update_or_create(category=category, title=item['title'], slug=item['slug'], images=va1, image_urls=item['image_urls'],  status=item['status'], description=item.get('description'), numChapters=item['numChapters'],  rating=item.get('rating'), released=item.get('released'), author=item.get('author'),  artist=item.get('artist'), created_by=item.get('created_by'),  alternativetitle=item.get('alternativetitle'), serialization=item.get('serialization'))
                                for genres in genrelist:
                                    obj1, created = Genre.objects.filter(
                                        Q(name__icontains=genres)
                                    ).update_or_create(name=genres)
                                    comic.genres.add(obj1)
                                    comic.save()
                            except:
                                raise DropItem(f"Duplicate Item Found{item}")
                        else:
                            try:
                                comic, created = Comic.objects.filter(
                                    Q(title__icontains=item['title']) |
                                    Q(slug__icontains=item['slug'])
                                ).get_or_create(title=item['title'], slug=item['slug'], images=va1, image_urls=item['image_urls'],  status=item['status'], description=item.get('description'), numChapters=item['numChapters'],  rating=item.get('rating', '1.0'), released=item.get('released', '-'), author=item.get('author', '-'),  artist=item.get('artist', '-'), created_by=item.get('created_by', '-'),  alternativetitle=item.get('alternativetitle', '-'), serialization=item.get('serialization', '-'))
                            except:
                                raise DropItem(f"Duplicate Item Found{item}")
                    return item
                else:
                    raise DropItem(f"Missing field in Comic-Item:{item}")

        else:
            raise DropItem(f"Missing field in Comic-Item:{item}")
