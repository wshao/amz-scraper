import scrapy
from scrapy.utils.project import get_project_settings
import re


class ReviewSpider(scrapy.Spider):
    name = "ReviewSpider"

    '''
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com']
    '''

    def start_requests(self):

        settings = get_project_settings()
        ASINs = settings.get('ASINS')
        urls = []
        domain = 'https://www.amazon.com'
        path = '/product-reviews'
        defaultPrams = "ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1"

        self.log("***ASINs:***")
        self.log(ASINs)
        self.log("***ASINs:***")

        if ASINs is not None:
            for asin in ASINs:
                url = domain + path + "/" + asin + "/?" + defaultPrams
                urls.append(url)

        self.log("***URLS:***")
        self.log(urls)
        self.log("***URLS:***")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        review_cards = response.css('.review')

        self.log("helloworld:")
        self.log(response.url)
        self.log("The review cards is:" + str(len(review_cards)))
        asin = self.get_asin_from_url(response.url)

        for review_card in review_cards:
            title = review_card.css('a.review-title span::text').get()
            variant = review_card.css('div.review-format-strip a.a-color-secondary::text').get()
            review_date = review_card.xpath('//span[@data-hook="review-date"]/text()').get()
            review_text = review_card.css("div.review-data span.review-text").get()
            rating_block = review_card.css('i.review-rating').xpath("@class").get()
            rating = self.find_rating(rating_block)

            yield {
                'asin': asin,
                'title': title,
                'variant': variant,
                'review date': review_date,
                'rating': rating,
                'review test': review_text
            }

        next_page = response.css('ul.a-pagination li.a-last a::attr("href")').get()

        if next_page is not None:
            self.log("There is a next page: " + next_page)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def getTrackingAsins(self):
        self.log("This is to read from the configured ASINs")

    def find_rating(self, rating_blocks):

        if "a-star-1" in rating_blocks:
            return 1
        elif "a-star-2" in rating_blocks:
            return 2
        elif "a-star-3" in rating_blocks:
            return 3
        elif "a-star-4" in rating_blocks:
            return 4
        else:
            return 5

    def get_asin_from_url(self, url):

        self.log("===============Parse ASIN URL : "+ url)
        if url is not None:
            asin = re.findall('/product-reviews/(.+)/', url)
            self.log("The asin is : " + asin[0])
            if asin:
                return asin[0]
