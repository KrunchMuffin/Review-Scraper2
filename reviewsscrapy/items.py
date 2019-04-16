# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def remove_unwanted(value):
    return value.replace(u'\ufffd', "'") \
        .replace("\t", "") \
        .replace("\u00e2\u20ac\u2122", "'") \
        .replace("’", "'").replace("â€™", "'").replace("ï¿½â‚¬â„¢", "'").replace("ï¿½â‚¬", '"')


class ReviewsItem(scrapy.Item):
    product = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_unwanted),
        output_processor=TakeFirst()
        )
    rating = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    reviewer = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_unwanted),
        output_processor=TakeFirst()
        )
    revdate = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    title = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_unwanted, remove_tags),
        output_processor=TakeFirst()
        )
    body = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_tags),
        output_processor=TakeFirst()
        )
    pros = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_unwanted),
        output_processor=TakeFirst()
        )
    cons = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_unwanted),
        output_processor=TakeFirst()
        )
    scraped_from = scrapy.Field()
