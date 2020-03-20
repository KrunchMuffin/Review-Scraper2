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
        .replace("\t", "").replace('â�‚��"�', "'").replace("Ã¢?‚??""?t", "'t") \
        .replace(u"\u00e2\u20ac\u2122", "'").replace("s", "'s").replace("Ã¢â‚¬â""¢", "'t") \
        .replace("’", "'").replace("â€™", "'").replace("ï¿½â‚¬â„¢", "'").replace("ï¿½â‚¬", '"').replace("?s", "'s")


def remove_words(value):
    return value.replace("Your Choice!", "").replace("Choose Your Pads!", "")


def remove_by(value):
    return value.replace("by", "")


class ReviewsItem(scrapy.Item):
    default_output_processor = TakeFirst()
    # product = scrapy.Field(
    #     input_processor=MapCompose(str.strip, remove_unwanted)
    # )
    product_id = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_words, str.strip),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    reviewer = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, remove_by, str.strip),
        output_processor=TakeFirst()
    )
    revdate = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    body = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    pros = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    cons = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    reviewer_location = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    is_verified = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    images = scrapy.Field()
    scraped_from = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    website = scrapy.Field()


class ProductsItem(scrapy.Item):
    default_output_processor = TakeFirst()
    _id = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_words, str.strip),
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    scraped_from = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image_urls = scrapy.Field()
    images = scrapy.Field()
    click_count = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(remove_unwanted, remove_tags, str.strip),
        output_processor=TakeFirst()
    )
