from scrapy.spiders import Spider
import scrapy
from image_downloader.items import ChapterDownloaderItem, ComicDownloaderItem
from scrapy.loader import ItemLoader


class MySpider(Spider):
    name = 'myspider'
    site_urls = ['https://www.asurascans.com/manga/']
    other_urls = ['https://reaperscans.com/comics']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other)
                     for x in self.other_urls]
        requests += [scrapy.Request(x, self.parse_shop)
                     for x in self.site_urls]
        return requests

    def parse_shop(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        comic_page_links = response.xpath(
            '//div[contains(@class, "bsx")]/a/@href')
        yield from response.follow_all(comic_page_links, callback=self.parsecomic)
        pagination_links = response.css('a.r::attr(href)')
        yield from response.follow_all(pagination_links, callback=self.parse_shop)

    def parsecomic(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        loader = ItemLoader(item=ComicDownloaderItem(), selector=response)
        title = response.xpath(
            '//h1[contains(@class, "entry-title")]/text()').get().strip(),
        slug = response.xpath(
            '//div[contains(@class, "bixbox")]/ol/li[2]/a/@href').get().split('/')[-2],
        img = response.css(
            '.wp-post-image::attr(src)').get()
        description = response.css(
            '[itemprop="description"] p::text').getall()
        created_by = response.css('[itemprop="author"] i::text').get().strip()
        rating = response.css('[itemprop="ratingValue"]::text').get().strip()
        status = response.css('.imptdt i::text').get().strip()
        category = response.css('.imptdt a::text').get().strip()
        alternativetitle = response.css('.wd-full span::text').get()
        released = response.css('.fmed span::text').get().strip()
        author = response.css('.fmed span::text')[1].get().strip()
        artist = response.css('.fmed span::text')[2].get().strip()
        serialization = response.css('.fmed span::text')[3].get().strip()
        genre = response.css('.mgen [rel="tag"]::text').getall()
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('description', description)
        loader.add_value('image_urls', response.urljoin(img))
        loader.add_value('created_by', created_by)
        loader.add_value('rating', rating)
        loader.add_value('status', status)
        loader.add_value('category', category)
        loader.add_value('alternativetitle', alternativetitle)
        loader.add_value('released', released)
        loader.add_value('author', author)
        loader.add_value('artist', artist)
        loader.add_value('serialization', serialization)
        loader.add_value('genre', genre)
        loader.add_value('numChapters', len(
            response.css('.eph-num a::attr(href)').getall()))
        yield loader.load_item()
        # # Single Chapter Page
        # chapter_page = response.xpath(
        #     '//div[contains(@class, "eph-num")]/a/@href').get()
        # if chapter_page is not None:
        #     yield response.follow(chapter_page, self.parsechapter)

        # All Chapter Page
        chapter_page = response.xpath(
            '//div[contains(@class, "eph-num")]/a/@href').getall()

        for url in chapter_page:
            if url is not None:
                yield response.follow(url, self.parsechapter)

    def parsechapter(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
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

    def parse_other(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        links = response.css('li .text-sm::attr(href)')
        yield from response.follow_all(links, callback=self.parsewebtoon)
        for x in range(1, 10):
            yield (scrapy.Request(f'https://reaperscans.com/comics?page={x}', callback=self.parse_other))

    def parsewebtoon(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        loader = ItemLoader(item=ComicDownloaderItem(), selector=response)
        slug = response.url.split('/')[-1],
        title = response.css('h1::text').get().strip()
        description = response.css('[aria-label="card"] p::text').getall()
        img = response.css('.transition img::attr(src)').get()
        status = response.css('.flex dd::text')[1].get()
        numChapters = response.css('.flex dd::text')[4].get()
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('image_urls', response.urljoin(img))
        loader.add_value('description', description)
        loader.add_value('status', status)
        loader.add_value('numChapters', numChapters)
        yield loader.load_item()
        chapt = response.css('[role="list"]')[0]
        # All Chapter Page
        chapter_page = chapt.css('a::attr(href)').getall()
        for url in chapter_page:
            if url is not None:
                yield response.follow(url, self.parsechapter1)
        # # Single Chapter Page
        # chapter_page = chapt.css('a::attr(href)').get()
        # if chapter_page is not None:
        #     yield response.follow(chapter_page, self.parsechapter)

    def parsechapter1(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        loader = ItemLoader(item=ChapterDownloaderItem(), selector=response)
        cslug = response.url.split('/')[-1],
        slug = response.css(
            '.inline-flex::attr(href)')[1].get().split('/')[-1],
        title = response.css('p::text').get().strip()
        name = response.css('nav .text-white::text')[5].get().strip()
        numPages = len(response.css('p img').getall())
        loader.add_value('title', title)
        loader.add_value('slug', slug)
        loader.add_value('chapterslug', cslug)
        loader.add_value('name', name)
        loader.add_value('numPages', numPages)

        for img in response.css('p img::attr(src)').getall():
            loader.add_value('image_urls', response.urljoin(img))
        yield loader.load_item()
