#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on: __DATE__
# Project: __PROJECT_NAME__
#
#                      .-"``"-.
#                     /______; \
#                    {_______}\|
#                    (/ a a \)(_)
#                    (.-.).-.)
#  ____________ooo__(    ^    )________________
# /                  '-.___.-'                 \
#| Hello Chebyshev:                             |
#|  Are you writting BUUUUGs again?             |
#|  please make good explaination Notes.        |
#|                                              |
#|      --May you have fun with this framework. |
#|               tips from qiulimao@2016.06.07  |
# \_____________________________ooo____________/
#                    |_  |  _|  jgs
#                    \___|___/
#                    {___|___}
#                     |_ | _|
#                     /-'Y'-\
#                    (__/ \__)
#

from pyspider.libs.base_handler import *
from pyspider.libs.useragent import IphoneSafari,LinuxChrome
from pyspider.libs.cleaners import  TakeFirst,JoinCleaner,StripBlankMoreThan2
from pyspider.libs.cleaners import  reduceclean,mapclean,mapreduce
from pyspider.libs.utils import utf8,unicode_string,md5string

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
        ```python

            for url in response.xpath("//a/@href"):
                self.crawl(url,callback=self.detail_page)

        ```
        this does the same effect as below:
        """
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
