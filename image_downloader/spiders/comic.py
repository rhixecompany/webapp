import scrapy
from image_downloader.items import ChapterDownloaderItem
from scrapy.loader import ItemLoader


class ComicSpider(scrapy.Spider):
    name = 'comic'

    def start_requests(self):
        yield scrapy.Request('https://www.asurascans.com/manga/1672760368-murim-login/')

    def parse(self, response):

        # All Chapter page
        chapter_page_links = response.css('ul.clstyle li a::attr(href)')
        yield from response.follow_all(chapter_page_links, callback=self.parse_chapters)
        self.logger.info(
            'A Comic response from %s just Finished!', response.url)

    def parse_chapters(self, response):
        loader = ItemLoader(item=ChapterDownloaderItem(), selector=response)
        loader.add_value('title', response.css(
            '.hentry .allc a::text').get().strip())
        loader.add_value('slug', response.css(
            '.hentry .allc a::attr(href)').get().split('/')[-2])
        loader.add_value('chapterslug', response.url.split('/')[-2])
        loader.add_css('name', 'h1.entry-title::text')
        img_list = response.css('.rdminimal p img ::attr(src)').getall()
        loader.add_value('numPages', len(img_list))
        for img_url in img_list:
            loader.add_value('image_urls', response.urljoin(img_url))
        yield loader.load_item()
        self.logger.info(
            'A Chapter response from %s just Finished!', response.url)
