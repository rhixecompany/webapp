from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from image_downloader import settings as my_settings
from image_downloader.spiders.comic import ComicSpider


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        configure_logging()
        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        process = CrawlerProcess(settings=crawler_settings)

        process.crawl(ComicSpider)
        process.start()
