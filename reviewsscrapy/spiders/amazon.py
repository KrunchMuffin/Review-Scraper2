# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy.loader import ItemLoader
from reviewsscrapy.items import ReviewsItem, ProductsItem
import logging


class AmazonSpider(CrawlSpider):
    name = 'amazon_us'
    allowed_domains = ['amazon.com', 'amzn.to']
    start_urls = [
        # 'https://www.amazon.com/s?i=automotive&rh=n%3A15684181%2Cn%3A15718271%2Cn%3A15718651&dc&qid=1584642770&rnid=15690151&ref=sr_hi_3'
        'https://amzn.to/2vzAHP6'
    ]

    rules = (
        # Rule(LinkExtractor(restrict_xpaths="//div[@class='a-section a-spacing-none reviews-content a-size-base']",
        #                    unique=True), callback='parse_review', follow=False),
        Rule(LinkExtractor(restrict_xpaths=(["//div[@class='a-section octopus-pc-category-card-v2-content']",
                                             "//li[@class='s-result-item  celwidget  ']",
                                             "//div[@id='search-results']",
                                             "//a[@data-hook='see-all-reviews-link-foot']",
                                             "//div[@class='a-section a-spacing-none reviews-content a-size-base']"
                                             ]),
                           unique=True), callback='parse_review', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//div[@id='search-results']",
        #                    deny=r"https://www.amazon.com/gp/slredirect/picassoRedirect.html/.+"),
        #      callback="parse_review", follow=False),

        # Rule(LinkExtractor(restrict_xpaths="//a[@data-hook='see-all-reviews-link-foot']", unique=True),
        #      callback=None, follow=True),

    )

    #
    # @staticmethod
    def parse_review(self, response):
        # if item:
        # desc //span[@id='productTitle']/text()
        print(response.request.url)
        print(response.xpath("//span[@id='productTitle']/text()").get())
        # ploader = ItemLoader(ProductsItem(), response=response)
        # ploader.add_xpath('_id', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
        # ploader.add_xpath('price', "//span[@class='pdPrSummaryProductPrice']/text()")
        # ploader.add_value('scraped_from', response.request.url)
        # ploader.add_xpath('image_urls', "//a[@itemprop='contentUrl']/@href")
        # yield ploader.load_item()
        #
        # for review in response.xpath("//div[@class='pdPrWrapper']"):
        #     is_verified: bool = False
        #     loader = ItemLoader(ReviewsItem(), response=response, selector=review)
        #     loader.add_xpath('product_id', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
        #     is_verified = len(response.xpath(".//div[@class='pdPrVerifiedBuyer']")) > 0
        #     loader.add_xpath('rating', "count(.//div[@class='pdPrListOverallRating']/div/span)")
        #     loader.add_xpath('reviewer', ".//div[@class='pdPrReviewsName']")
        #     loc = response.xpath(".//div[@class='pdPrReviewerLocation']/text()").get()
        #     if loc is None or len(loc.strip()) == 0:
        #         loc = "N/A"
        #     loader.add_value('reviewer_location', loc)
        #     loader.add_value('is_verified', "Yes" if is_verified == 1 else "No")
        #     loader.add_xpath('revdate', ".//div[@class='pdPrReviewDate']")
        #     loader.add_xpath('title', ".//div[@class='pdPrTitle']")
        #     loader.add_xpath('body', ".//div[@class='pdPrBody']")
        #     loader.add_xpath('pros', ".//div[@class='pdPrListPros']/text()")
        #     loader.add_xpath('cons', ".//div[@class='pdPrListCons']/text()")
        #     loader.add_xpath('image_urls', ".//div[@class='pdPrReviewPhotos']/a/@href")
        #     loader.add_value('scraped_from', response.request.url)
        #     loader.add_value('website', 'autopia')
        #
        #     yield loader.load_item()

        # else:
        #     logging.warning('No item received for %s', response.url)

        next_page = response.selector.xpath("//li[@class='a-last']/a/@href").get()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
