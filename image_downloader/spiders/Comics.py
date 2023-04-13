import scrapy
from image_downloader.items import *
from scrapy.loader import ItemLoader
from Comics.models import Website


class ComicsSpider(scrapy.Spider):
    name = 'Comics'
    allowed_domains = ['asurascans.com']

    def start_requests(self):
        url = 'https://www.asurascans.com/manga/?page=1&order=update/'
        wesite, created = Website.objects.filter(
            url=url.split('/')[-4]).get_or_create(url=url.split('/')[-4])
        yield scrapy.Request(url)

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        comic_page_links = response.xpath(
            '//div[contains(@class, "bsx")]/a/@href')
        yield from response.follow_all(comic_page_links, callback=self.parsecomic)
        pagination_links = response.css('a.r::attr(href)')
        yield from response.follow_all(pagination_links, callback=self.parse)

    def parsecomic(self, response):
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
        self.logger.info(
            'A Comic Page response from %s just finished!', response.url)
        yield loader.load_item()
