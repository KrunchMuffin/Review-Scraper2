from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from reviewsscrapy.items import ReviewsItem, ProductsItem


class AutogeekSpider(CrawlSpider):
    name = 'ag'
    allowed_domains = ['autogeek.net']
    start_urls = ['https://www.autogeek.net/']

    rules = (
        Rule(LinkExtractor(allow=r"displayProductReviews\.php.*", unique=True), callback="parse_review", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='cat-nav']", unique=True),
             callback=None),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='contents-table']", unique=True),
             callback=None),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='pdReviewsViewAllBtn']", unique=True),
             callback=None),
    )

    @staticmethod
    def parse_review(response):
        ploader = ItemLoader(ProductsItem(), response=response)
        print(response.xpath("//span[@class='pdPrSummaryTitleItemName']/a/text()").get())
        ploader.add_xpath('_id', "//span[@class='pdPrSummaryTitleItemName']/a/text()")
        ploader.add_xpath('price', "//span[@class='pdPrSummaryTitleItemPrice']/span")
        ploader.add_value('scraped_from', response.request.url)
        ploader.add_xpath('image_urls', "//div[@class='pdPrSummaryOverallImg']/a/img/@src")
        ploader.add_xpath('description', "//div[@class='textpad']/p[2]/strong/text()")
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
            loader.add_value('website', 'autogeek')

            yield loader.load_item()

        # next_page = response.selector.xpath("//div[@class='pdReviewsPagingArrow pdRight']/a/@href").extract_first()
        #
        # if next_page is not None:
        #     next_page_link = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page_link, callback=self.parse)
