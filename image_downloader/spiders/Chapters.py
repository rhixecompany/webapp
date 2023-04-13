import scrapy
from image_downloader.items import *
from scrapy.loader import ItemLoader


class ChaptersSpider(scrapy.Spider):
    name = 'Chapters'
    allowed_domains = ['asurascans.com']

    def start_requests(self):
        yield scrapy.Request('https://www.asurascans.com/manga/?page=1&order=update/')

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        comic_page_links = response.xpath(
            '//div[contains(@class, "bsx")]/a/@href')
        yield from response.follow_all(comic_page_links, callback=self.parsecomic)
        pagination_links = response.css('a.r::attr(href)')
        yield from response.follow_all(pagination_links, callback=self.parse)

    def parsecomic(self, response):
        chapter_page_links = response.css('ul.clstyle li a::attr(href)')
        yield from response.follow_all(chapter_page_links, callback=self.parsechapter)
        self.logger.info(
            'A Comic Page response from %s just finished!', response.url)

    def parsechapter(self, response):
        loader = ItemLoader(item=ChapterDownloaderItem(), selector=response)
        cslug = response.xpath(
            '//div[contains(@class, "bixbox")]/ol/li[3]/a/@href').get().split('/')[-2],
        slug = response.xpath(
            '//div[contains(@class, "allc")]/a/@href').get().split('/')[-2],
        title = response.xpath(
            '//div[contains(@class, "allc")]/a/text()').get().strip(),
        name = response.xpath(
            '//h1[contains(@class, "entry-title")]/text()').get().strip(),
        imageslist = response.xpath(
            '//*[@id="readerarea"]/p/img/@src').getall()
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('chapterslug', cslug)
        loader.add_value('name', name)
        loader.add_value('numPages', len(imageslist))
        for img in imageslist:
            loader.add_value('image_urls', response.urljoin(img))
        yield loader.load_item()
        self.logger.info(
            'A Chapter Page response from %s just finished!', response.url)
