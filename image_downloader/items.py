# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html


from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

from scrapy.item import Field, Item

# import os
# def remove_extension(value):
#     return os.path.splitext(value)[0]


def split_text(value):
    return value.split('/')[-2],


def stripTags(value):
    return value.strip().replace("\n", "")


class ComicDownloaderItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    alternativetitle = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    images = Field()
    image_urls = Field()
    image_paths = Field()
    description = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=Join())
    rating = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    status = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    author = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    artist = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    released = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    created_by = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    serialization = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    numChapters = Field(output_processor=TakeFirst())
    category = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    genre = Field(input_processor=MapCompose(
        remove_tags, stripTags))


class ChapterDownloaderItem(Item):
    title = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    slug = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    chapterslug = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(
        remove_tags, stripTags), output_processor=TakeFirst())
    numPages = Field(output_processor=TakeFirst())
    images = Field()
    image_urls = Field()
    image_paths = Field()
