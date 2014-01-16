#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json

import tornado.ioloop
import tornado.web

from productparser import get

__author__ = 'cliu'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello")


class ProductParserHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('template.html')

    def post(self):
        url = self.get_argument('url')
        title, price, srcs = get(url)
        dic = {
            'title': title,
            'price': price,
            'srcs': srcs
        }
        self.write(json.dumps(dic))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/product-parser", ProductParserHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
