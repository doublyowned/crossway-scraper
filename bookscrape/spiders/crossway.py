# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from bookscrape.items import Book

class CrosswaySpider(scrapy.Spider):
    name = "crossway"
    allowed_domains = ["crossway.org"]
    start_urls = ['http://crossway.org/books']

    detail_xpath = {
        'title': '//div[@id="book-detail"]//h1/text()',
        'author': '//p[@class="detail-contributors"]//strong[text()="By"]/a/text()',
        'category': '//td[text()="Category:"]/following::td/a/text()'
    }

    hardcoded_values = {
        'publisher': 'Crossway'
    }

    def parse(self, response):
        detail_links = response.xpath('//a[contains(@class,"thumb-cover")]/@href').extract()

        print detail_links

        for href in detail_links:
            yield Request(response.urljoin(href), callback=self.parse_detail)

    def parse_detail(self, response):
        item = ItemLoader(item=Book(), response=response)
        item.default_output_processor = TakeFirst()

        #iterate over xpath to scrape and load item details
        for field, xpath in self.detail_xpath.iteritems():
            item.add_xpath(field, xpath)

        #add hardcoded values
        for field, value in self.hardcoded_values.iteritems():
            item.add_value(field, value)

        #add book detaail url
        item.add_value('url', response.url)

        return item.load_item()
