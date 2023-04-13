import scrapy
from image_downloader.items import ChapterDownloaderItem, ComicDownloaderItem
from scrapy.loader import ItemLoader
from Comics.models import Website


class ReaperscansSpider(scrapy.Spider):
    name = 'reaperscans'

    def start_requests(self):
        url = 'https://reaperscans.com/comics'
        wesite, created = Website.objects.filter(
            url=url.split('/')[-2]).get_or_create(url=url.split('/')[-2])
        yield scrapy.Request(url)

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        links = response.css('li .text-sm::attr(href)')
        yield from response.follow_all(links, callback=self.parsewebtoon)
        for x in range(1, 10):
            yield (scrapy.Request(f'https://reaperscans.com/comics?page={x}', callback=self.parse))

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
                yield response.follow(url, self.parsechapter)
        # # Single Chapter Page
        # chapter_page = chapt.css('a::attr(href)').get()
        # if chapter_page is not None:
        #     yield response.follow(chapter_page, self.parsechapter)

    def parsechapter(self, response):
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
