# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo

from reviewsscrapy.items import ReviewsItem, ProductsItem


class MongoReviewsPipeline(object):
    collection_name = 'reviews'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_SERVER'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'dpr')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not isinstance(item, ReviewsItem):
            return item  # return the item to let other pipeline to handle it
        # self.collection.insert(dict(item))
        # self.db[self.collection_name].insert_one(dict(item))
        try:
            self.db[self.collection_name].find_one_and_update(
                {"product_id": item["product_id"], "title": item["title"],
                 "reviewer_location": item["reviewer_location"]},
                {"$set": dict(item)},
                upsert=True)

            return item

        except pymongo.errors.DuplicateKeyError as e:
            logging.warning(e)


class MongoProductsPipeline(object):
    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        # self.ids_seen = set()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_SERVER'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'dpr')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not isinstance(item, ProductsItem):
            return item  # return the item to let other pipeline to handle it
        # if item['_id'] in self.ids_seen:
        #     raise DropItem("Duplicate item found: %s" % item)
        # else:
        # self.db[self.collection_name].insert_one(dict(item))
        try:
            self.db[self.collection_name].insert_one(dict(item))
        except pymongo.errors.DuplicateKeyError as e:
            logging.warning(e)

        # self.db[self.collection_name].update_one({'_id': item['_id']}, {"$set": item}, upsert=True)
        return item
