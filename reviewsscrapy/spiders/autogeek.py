# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AutoGeekSpider(CrawlSpider):
    name = 'ag'
    allowed_domains = ['autogeek.net']
    start_urls = ['https://www.autogeek.net/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='cat-nav']", unique=True),
             callback="parse_review", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='contents-table']", unique=True),
             callback="parse_review", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='pdReviewsViewAllBtn']", unique=True),
             callback="parse_review", follow=True),
        )

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
            yield {
                'product': response.xpath(".//span[@class='pdPrSummaryTitleItemName']/a/text()").extract_first(),
                'rating': review.xpath(".//span[@class='pdPrSummaryTitleItemName']/a/text()").extract_first(),
                'reviewer': review.xpath(".//div[@class='pdPrReviewsName']/text()").extract_first(),
                'revdate': review.xpath(".//div[@class='pdPrReviewDate']/text()").extract_first(),
                'title': review.xpath(".//div[@class='pdPrTitle']/text()").extract_first(),
                'body': review.xpath(".//div[@class='pdPrBody']/text()").extract_first(),
                'pros': review.xpath(".//div[@class='pdPrListPros']/text()").extract_first(),
                'cons': review.xpath(".//div[@class='pdPrListCons']/text()").extract_first(),
                }
            # review = ReviewsscrapyItem()
            # review['title'] = response.xpath('//*[@id="rightbody"]/div[3]/h1[1]/span/text()').extract()
            # print(review['title'])
        # text = response.css('[class="section page-centered"]div::text').extract()[1]
        # scraped_info = {
        #     'title': review[',
        #     #  'text': text
        #     }
        # yield review

    # grab the nav links that go to cat pages index from site homepage
    # def parse(self, response):
    #     links = response.css('.cat-nav a::attr(href)').extract()
    #     for url in links:
    #         print("index: " + url)
    #         yield scrapy.Request(url, callback=self.parse_cat_page_links)

    # grab the links to each sub cat
    # def parse_cat_page_links(self, response):
    #     catlinks = response.css('.contents-product a::attr(href)').extract()
    #     for link in catlinks:
    #         print("cat: " + urljoin(response.url, link))
    #         yield scrapy.Request(urljoin(response.url, link), callback=self.parse_product_index_links)
    #
    # # grab the links to product
    # def parse_product_index_links(self, response):
    #     prodlinks = response.css('.contents-product a::attr(href)').extract()
    #     for link in prodlinks:
    #         print("pindex: " + urljoin(response.url, link))
    #         yield scrapy.Request(urljoin(response.url, link), callback=self.parse_product_page_links)
    #
    # # grab the 'View all reviews' link if there is one
    # def parse_product_page_links(self, response):
    #     revlink = response.css('.pdReviewsViewAllBtn a::attr(href)').extract()
    #     print(urljoin(response.url, revlink))
    #     yield scrapy.Request(urljoin(response.url, revlink), callback=self.parse_review)
