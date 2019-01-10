# -*- coding: utf-8 -*-
import scrapy

class Book(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()
    publisher = scrapy.Field()
