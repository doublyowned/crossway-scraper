# -*- coding: utf-8 -*-
import requests
import json
import q

class BookscrapePipeline(object):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     crawler.spider.categories = []

    #     return cls()


    def process_item(self, item, spider):
        base_url =  'http://127.0.0.1:8000/books/'

        book_api_keys = ['title', 'category', 'pic_url', 'medium', 'ISBN_10', 'blurb']
        book_data = {book_field: item[book_field] for book_field in book_api_keys}

        author_data = {
            'name': item['author'],
            'pic_url': item['author_pic'],
            'blurb': item['author_blurb'],
            'books': [book_data]
        }

        headers = {
            'Content-Type': 'Application/JSON',
        }

        if item['blurb']:
            print "I DEFINITELY HAVE A BLURB!!!!!!!!!!!!!!!!!!", item['blurb']


        body = json.dumps(author_data)
        a = requests.post(base_url + 'authors/api/', data=body, headers=headers)
        # spider.categories.append(item['category'])

