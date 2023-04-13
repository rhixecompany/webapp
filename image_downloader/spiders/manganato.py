import scrapy
from image_downloader.items import ComicDownloaderItem, ChapterDownloaderItem
from scrapy.loader import ItemLoader


class ManganatoSpider(scrapy.Spider):
    name = 'manganato'
    start_urls = ['https://manganato.com/genre-all/']

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        comic_page_links = response.css('a.genres-item-name::attr(href)')
        yield from response.follow_all(comic_page_links, callback=self.parse_webtoon)
        for x in range(1, 4):
            yield (scrapy.Request(f'https://manganato.com/genre-all/{x}', callback=self.parse))
        # next_page = response.xpath(
        #     '//div[contains(@class, "group-page")]/a/@href')
        # yield from response.follow_all(next_page, callback=self.parse)

    def parse_webtoon(self, response):
        loader = ItemLoader(item=ComicDownloaderItem(), selector=response)
        title = response.css('div.story-info-right h1::text').get()
        slug = response.url.split('/')[-1]
        img = response.css(
            'span.info-image img.img-loading::attr(src)').get()
        description = response.css(
            '.panel-story-info-description::text').getall()
        # views = response.css(
        #    'span.stre-value ::text').getall()[1].strip()
        rating = response.css('em#rate_row_cmd em::text').getall()[5].strip()
        author = response.css('tr a.a-h::text').getall()[0]
        genre = response.css(
            'table tr td.table-value a.a-h::text').getall()[:50]
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('description', description)
        loader.add_value('image_urls', response.urljoin(img))
        loader.add_value('rating', rating)
        loader.add_value('author', author)
        loader.add_value('genre', genre)
        # loader.add_value('artist', artist)
        # loader.add_value('serialization', serialization)
        # loader.add_value('created_by', created_by)
        # loader.add_value('status', status)
        # loader.add_value('category', category)
        # loader.add_value('alternativetitle', alternativetitle)
        # loader.add_value('released', released)
        # loader.add_value('numChapters', len(
        #     response.css('.eph-num a::attr(href)').getall()))
        yield loader.load_item()
        chapter_page = response.css(
            '.chapter-name::attr(href)').get()
        if chapter_page:
            yield response.follow(chapter_page, self.parsechapter)
        # chapter_page_links = response.css(
        #     'ul.row-content-chapter li.a-h a.chapter-name::attr(href)')
        # yield from response.follow_all(chapter_page_links, callback=self.parsechapter)

    def parsechapter(self, response):
        loader = ItemLoader(item=ChapterDownloaderItem(), selector=response)
        slug = response.xpath(
            '//div[contains(@class, "panel-breadcrumb")]/a[2]/@href').get().split('/')[-1]
        title = response.xpath(
            '//div[contains(@class, "panel-breadcrumb")]/a[2]/text()').get().strip()
        name = response.xpath(
            '//div[contains(@class, "panel-breadcrumb")]/a[3]/text()').get().strip()
        cslug = response.xpath(
            '//div[contains(@class, "panel-breadcrumb")]/a[3]/@href').get().split('/')[-1]
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('name', name)
        loader.add_value('chapterslug', cslug)
        imageslist = response.xpath(
            '//div[contains(@class, "container-chapter-reader")]/img/@src').getall()
        loader.add_value('numPages', len(imageslist))
        for img in imageslist:
            loader.add_value('image_urls', response.urljoin(img))
        yield loader.load_item()
