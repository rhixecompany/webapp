from django.core.management.base import BaseCommand
# from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from image_downloader import settings as my_settings
from image_downloader.spiders.asurascans import AsurascansSpider
from image_downloader.spiders.reaperscans import ReaperscansSpider
from twisted.internet import reactor, defer

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings


# class Command(BaseCommand):

#     help = 'Release spider'

#     def handle(self, *args, **options):
#         configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#         crawler_settings = Settings()
#         crawler_settings.setmodule(my_settings)
#         runner = CrawlerRunner(crawler_settings)
#         d = runner.crawl(AsurascansSpider)
#         d = runner.crawl(ReaperscansSpider)
#         d.addBoth(lambda _: reactor.stop())
#         reactor.run()  # the script will block here until the crawling is finished


# class Command(BaseCommand):
#     help = 'Release spider'

#     def handle(self, *args, **options):
# crawler_settings = Settings()
# crawler_settings.setmodule(my_settings)
#         configure_logging(crawler_settings)

#         process = CrawlerProcess(settings=crawler_settings)

#         process.crawl(AsurascansSpider)
#         process.crawl(ReaperscansSpider)
#         process.start()


class Command(BaseCommand):

    help = 'Release spider'

    def handle(self, *args, **options):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(AsurascansSpider)
            yield runner.crawl(ReaperscansSpider)
            reactor.stop()

        crawl()
        reactor.run()
