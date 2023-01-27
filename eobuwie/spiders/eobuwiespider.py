import scrapy
from scrapy.exceptions import CloseSpider
from eobuwie.items import EobuwieItem
from scrapy.loader import ItemLoader

class EobuwieSpider(scrapy.Spider):
    name = 'eobuwie'
    handle_httpstatus_list = [404]
    page_number = 1

    def start_requests(self):
        yield scrapy.Request(f'https://www.eobuwie.com.pl/{self.type1}/{self.type2}/{self.type3}.html?p=1')

    def parse_products(self, response):
        products = response.css('div.one-col-wrapper')
        for product in products:
            l = ItemLoader(item = EobuwieItem(), selector=products)
            l.add_css('name', 'h1.e-heading.e-heading--third-level.e-product-name.e-product-name--only-desktop')
            l.add_css('price', 'div.e-product-price__normal')
            l.add_css('price', 'div.e-product-price__special')
            l.add_css('rating_count', 'span.e-rating-summary__count')

            yield l.load_item()

    def parse(self, response):
        if response.status == 404:
            raise CloseSpider('Received 404 response')

        if len(response.css('a.toolbar-bottom__navigation-button')) == 0:
            raise CloseSpider('No items on the page')

        for link in response.css('a.products-list__link::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)
            
        self.page_number += 1
        next_page = f'https://www.eobuwie.com.pl/{self.type1}/{self.type2}/{self.type3}.html?p={self.page_number}'
        yield response.follow(next_page, callback=self.parse)
                