# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsscrapyItem(scrapy.Item):
    rating = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    username = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    revdate = scrapy.Field(serializer=str)
