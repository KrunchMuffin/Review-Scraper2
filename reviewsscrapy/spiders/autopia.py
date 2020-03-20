# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from reviewsscrapy.items import ReviewsItem, ProductsItem
import logging


class AutopiaSpider(CrawlSpider):
    name = 'autopia'
    allowed_domains = ['autopia-carcare.com']
    start_urls = ['https://www.autopia-carcare.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=(['//ul[@class="cat-nav"]',
                                             '//div[@id="contents-table"]',
                                             ]),
                           unique=True, deny=r"https://myaccount.autopia-carcare.com/.+"), callback=None),
        Rule(LinkExtractor(deny=r"https://myaccount.autopia-carcare.com/.+"), callback="parse_review", follow=False),
    )

    @staticmethod
    def parse_review(response):
        # if item:
        print(response.xpath("//span[@class='pdPrSummaryTitleItemName']/a/text()").get())
        ploader = ItemLoader(ProductsItem(), response=response)
        ploader.add_xpath('_id', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
        ploader.add_xpath('price', "//span[@class='pdPrSummaryProductPrice']/text()")
        ploader.add_value('scraped_from', response.request.url)
        ploader.add_xpath('image_urls', "//a[@itemprop='contentUrl']/@href")
        yield ploader.load_item()

        for review in response.xpath("//div[@class='pdPrWrapper']"):
            is_verified: bool = False
            loader = ItemLoader(ReviewsItem(), response=response, selector=review)
            loader.add_xpath('product_id', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
            is_verified = len(response.xpath(".//div[@class='pdPrVerifiedBuyer']")) > 0
            loader.add_xpath('rating', "count(.//div[@class='pdPrListOverallRating']/div/span)")
            loader.add_xpath('reviewer', ".//div[@class='pdPrReviewsName']")
            loc = response.xpath(".//div[@class='pdPrReviewerLocation']/text()").get()
            if loc is None or len(loc.strip()) == 0:
                loc = "N/A"
            loader.add_value('reviewer_location', loc)
            loader.add_value('is_verified', "Yes" if is_verified == 1 else "No")
            loader.add_xpath('revdate', ".//div[@class='pdPrReviewDate']")
            loader.add_xpath('title', ".//div[@class='pdPrTitle']")
            loader.add_xpath('body', ".//div[@class='pdPrBody']")
            loader.add_xpath('pros', ".//div[@class='pdPrListPros']/text()")
            loader.add_xpath('cons', ".//div[@class='pdPrListCons']/text()")
            loader.add_xpath('image_urls', ".//div[@class='pdPrReviewPhotos']/a/@href")
            loader.add_value('scraped_from', response.request.url)
            loader.add_value('website', 'autopia')

            yield loader.load_item()
    # else:
    #     logging.warning('No item received for %s', response.url)
