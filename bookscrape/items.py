# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader.processors import Join

class Book(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    pic_url = scrapy.Field()
    publisher = scrapy.Field()
    medium = scrapy.Field()
    ISBN_10 = scrapy.Field()
    blurb = scrapy.Field()
    author = scrapy.Field()
    author_blurb = scrapy.Field()
    author_pic = scrapy.Field()

