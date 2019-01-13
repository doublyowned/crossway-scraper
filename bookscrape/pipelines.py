# -*- coding: utf-8 -*-
import requests
import json
import q

class BookscrapePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        crawler.spider.categories = []

        return cls()

    def process_item(self, item, spider):
        base_url =  'http://127.0.0.1:8000/books/'
        author_data = {
            'name': item['author'],
            'pic_url': item['author_pic'],
            'blurb': item['author_blurb'],
        }

        book_api_keys = ['title', 'category', 'pic_url', 'medium', 'ISBN_10', 'blurb']

        book_data = {book_field: item[book_field] for book_field in book_api_keys}
        

        headers = {
            'Content-Type': 'Application/JSON',
        }

        # spider.categories.append(item['category'])
        # print 'APPEND CATEGORY', item.category
        a = requests.get(base_url + '/authors/api/' + author_data['name'])
        if a.status_code == 404:
            a = requests.post(base_url + 'authors/api/', author_data)

        book_data['author'] = a.json()['id']

        body = json.dumps(book_data)
        print 'POSTING', body
        r = requests.post(base_url + 'api/', data=body, headers=headers)
        # q.d()
        # print r.json()
        # print 'processed: ', item


