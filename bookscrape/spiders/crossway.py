# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

import q

from bookscrape.items import Book

class CrosswaySpider(scrapy.Spider):
    name = "crossway"
    allowed_domains = ["crossway.org"]
    start_urls = ['http://crossway.org/books']

    def by_previous_text(text):
        return '//td[text()="' + text + '"]/following::td/text()'

    detail_xpath = {
        'title': '//div[@id="book-detail"]//h1/text()',
        'author': '//p[@class="detail-contributors"]//strong[text()="By"]/following::a/text()',
        'category': '//td[text()="Category:"]/following::td/a/text()',
        'pic_url': '//*[@id="cover"]/@src',
        'medium': by_previous_text('Format:'),
        'ISBN_10': by_previous_text('ISBN-10:'),
        'blurb': '//div[@class="top-details desktop"]/following::div',
        'author_pic': '//div[@class="book-detail-author clear"]/a/img/@src', 
        'author_blurb': '//div[@class="book-detail-author clear"]/div/p',
        # 'author': '//div[@class="book-detail-author clear"]/div/p/p'
    }

    hardcoded_values = {
        'publisher': 'Crossway'
    }

    def parse(self, response):
        #grab relevant links for further parsing
        pagination_link = response.xpath('//a[@class="next"]/@href')
        detail_links = response.xpath('//a[contains(@class,"thumb-cover")]/@href').extract()

        #send book detail links to be parsed
        for href in detail_links:
            yield Request(response.urljoin(href), callback=self.parse_detail)

        #if there's a next page, parse it as well
        for next_href in pagination_link.extract():
            yield Request(response.urljoin(next_href), callback=self.parse)



    def parse_detail(self, response):
        item = ItemLoader(item=Book(), response=response)
        item.default_output_processor = TakeFirst()

        #iterate over xpath to scrape and load item details
        for field, xpath in self.detail_xpath.iteritems():
            item.add_xpath(field, xpath)

        #add hardcoded values
        for field, value in self.hardcoded_values.iteritems():
            item.add_value(field, value)

        return item.load_item()

    # def closed(self, spider):
    #     categories = self.categories
    #     unique= set(c for c in categories)
    #     
    #     print 'unique categ', unique