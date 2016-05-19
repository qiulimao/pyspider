#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on __DATE__
# Project: __PROJECT_NAME__

from pyspider.libs.base_handler import *
from pyspider.libs.useragent import IphoneSafari,LinuxChrome
from pyspider.libs.response import Response

class Handler(BaseHandler):
    crawl_config = {
      'headers': {'User-Agent': LinuxChrome}
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('__START_URL__', callback=self.index_page)

    @config(age=60)
    def index_page(self, response):
        """
        response.xpath method is available
        """
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
