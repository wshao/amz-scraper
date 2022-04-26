import scrapy
from scrapy.utils.project import get_project_settings
import re


class RatingSpider(scrapy.Spider):
    name = "RatingSpider"

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
        defaultPrams = "ie=UTF8&reviewerType=all_reviews&sortBy=recent&formatType=current_format&pageNumber=1"

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


    def parse_size_panel(self,response):

        #First, it check the size panel
        sizePanel =  response.css('div#inline-twister-expander-content-size_name')
        if sizePanel is not None:
            sizeOptions = sizePanel.css('ul.dimension-values-list li')
            sizeAsinList = []
            for sizeOption in sizeOptions:
                sizeAsin = sizeOption.xpath('@data-asin').get()
                if sizeAsin is not None:
                    sizeAsinList.append(sizeAsin)
                    g
                    yield scrapy.Request()
        # else:


    # def get_asin_dp_url_by_asin(self, response, asin):

        # currentUrl = response.url;
        # if asin is not None:



    def parse(self, response):

        self.log("helloworld:")
        self.log(response.url)

        filter_section = response.css('div#filter-info-section')
        self.log(filter_section)
        asin = self.get_asin_from_url(response.url)

        if filter_section is not None:
            variant = filter_section.css('span#reviews-filter-info-segment::text').get()
            rating_review_text = filter_section.xpath('//div[@data-hook="cr-filter-info-review-rating-count"]/span/text()').get()
            self.log("The Variant is: "+ variant)
            self.log("rating review text is: "+ rating_review_text)
            self.log("Rating is :" + self.rating_from_text(rating_review_text))
            self.log("Review is :" + self.review_from_text(rating_review_text))

            yield {
                'asin' : asin,
                'variant' : variant,
                'rating'  : self.rating_from_text(rating_review_text),
                'review'  : self.review_from_text(rating_review_text)
            }



        # self.log("helloworld:")
        # self.log(response.url)
        # self.log("The review cards is:" + str(len(review_cards)))
        # asin = self.get_asin_from_url(response.url)
        #
        # for review_card in review_cards:
        #     title = review_card.css('a.review-title span::text').get()
        #     variant = review_card.css('div.review-format-strip a.a-color-secondary::text').get()
        #     review_date = review_card.xpath('//span[@data-hook="review-date"]/text()').get()
        #     review_text = review_card.css("div.review-data span.review-text").get()
        #     rating_block = review_card.css('i.review-rating').xpath("@class").get()
        #     rating = self.find_rating(rating_block)
        #
        #     yield {
        #         'asin': asin,
        #         'title': title,
        #         'variant': variant,
        #         'review date': review_date,
        #         'rating': rating,
        #         'review test': review_text
        #     }
        #
        # next_page = response.css('ul.a-pagination li.a-last a::attr("href")').get()
        #
        # if next_page is not None:
        #     self.log("There is a next page: " + next_page)
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

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

    def rating_from_text(self, text):

        if text is not None:

            rating = re.findall(' *(.+) global ratings',text)
            if rating:
                return rating[0]

    def review_from_text(self, text):

        if text is not None:

            review = re.findall('\| (.+) global reviews',text)
            if review:
                return review[0]