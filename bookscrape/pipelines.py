# -*- coding: utf-8 -*-
import requests
import json
import q

class BookscrapePipeline(object):
    def process_item(self, item, spider):
        body = json.dumps(dict(item))
        headers = {
            'Content-Type': 'Application/JSON',
        }

        r = requests.post('http://127.0.0.1:8000/books/books/', data=body, headers=headers)
        # q.d()
        # print r.json()
        print 'processed: ', item

