# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from bookscrape.items import Book

class CrosswaySpider(scrapy.Spider):
    name = "crossway"
    allowed_domains = ["crossway.org"]
    start_urls = ['http://crossway.org/books']

    detail_xpath = {
    	'title': '//div[@id="book-detail"]//h1',
    	'author': '//p[@class="detail-contributors"]//strong[text()="By"]/a/text()',
    }

    def parse(self, response):
    	detail_links = response.xpath('//a[contains(@class,"thumb-cover")]/@href')

    	for href in detail_links:
    		yield Request(response.urljoin(href), callback=self.parse_detail)

	def parse_detail(self, response):
		#iterate over xpath to scrape and load item details
		item = ItemLoader(item=Book(), response=response)

		for field, xpath in detail_xpath:
			item.add_xpath(field, xpath)

		for field, value in hardcoded_values:
			item.add_value(field, value)

		return item.load_item()
