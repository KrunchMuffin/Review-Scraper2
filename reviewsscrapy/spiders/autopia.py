# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from reviewsscrapy.items import ReviewsItem


class AutoGeekSpider(CrawlSpider):
    name = 'autopia'
    allowed_domains = ['autopia-carcare.com']
    start_urls = ['https://www.autopia-carcare.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@id='leftnav-top']", unique=True),
             callback="parse_review", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='contents-table']", unique=True),
             callback="parse_review", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='pdReviewsViewAllBtn']", unique=True),
             callback="parse_review", follow=True),
        )

    # .//div[@class='pdReviewsPagingArrow pdRight']/a
    def parse_review(self, response):

        # //div[@class='pdPrWrapper'] --> all reviews
        # //span[@class='pdPrSummaryTitleItemName']/a/text()  --> product name
        # //div[@class='pdPrListOverallRating']/div --> star rating
        # //div[@class='pdPrReviewsName']/text() --> reviewer name
        # //div[@class='pdPrReviewDate']/text() --> review date
        # //div[@class='pdPrTitle']/text() --> review title
        # //div[@class='pdPrBody']/text() --> review body
        # //div[@class='pdPrListPros']/text() --> pros
        # //div[@class='pdPrListCons']/text() --> cons

        for review in response.xpath("//div[@class='pdPrWrapper']"):
            loader = ItemLoader(ReviewsItem(), selector=review, response=response)
            loader.add_xpath('product', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
            loader.add_xpath('rating', "count(.//div[@class='pdPrListOverallRating']/div/span)")
            loader.add_xpath('reviewer', ".//div[@class='pdPrReviewsName']/text()")
            loader.add_xpath('revdate', ".//div[@class='pdPrReviewDate']/text()")
            loader.add_xpath('title', ".//div[@class='pdPrTitle']/text()")
            loader.add_xpath('body', ".//div[@class='pdPrBody']/text()")
            loader.add_xpath('pros', ".//div[@class='pdPrListPros']/text()")
            loader.add_xpath('cons', ".//div[@class='pdPrListCons']/text()")
            loader.add_value('scraped_from', response.request.url)
            yield loader.load_item()

            # yield {
            #     'product': response.xpath(".//span[@class='pdPrSummaryTitleItemName']/a/text()").extract_first(),
            #     'rating': review.xpath("count(.//div[@class='pdPrListOverallRating']/div/span)"),
            #     'reviewer': review.xpath(".//div[@class='pdPrReviewsName']/text()").extract_first(),
            #     'revdate': review.xpath(".//div[@class='pdPrReviewDate']/text()").extract_first(),
            #     'title': review.xpath(".//div[@class='pdPrTitle']/text()").extract_first(),
            #     'body': review.xpath(".//div[@class='pdPrBody']/text()").extract_first(),
            #     'pros': review.xpath(".//div[@class='pdPrListPros']/text()").extract_first(),
            #     'cons': review.xpath(".//div[@class='pdPrListCons']/text()").extract_first(),
            #     }

            next_page = response.selector.xpath("//div[@class='pdReviewsPagingArrow pdRight']/a/@href").extract_first()

            if next_page is not None:
                next_page_link = response.urljoin(next_page)
                yield scrapy.Request(url=next_page_link, callback=self.parse)

    # def absolute_url(self, url, loader_context):
    #     return loader_context['response'].urljoin(url)
