#coding:utf-8

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-05-20 15:28:20
# Modified on 2016-10-26 20:46:20
# Project: app_news_163 product

from weblocust.libs.base_handler import *
from weblocust.libs.useragent import IphoneSafari,LinuxChrome
from weblocust.libs.cleaners import  TakeFirst,JoinCleaner,StripBlankMoreThan2,reduceclean,mapclean,mapreduce
import json
from  itertools import product
from hashlib import md5
#from weblocust.libs.response import Response
# http://3g.163.com/touch/article/list/BBM54PGAwangning/20-20.html
# http://3g.163.com/touch/article.html?channel=mobile&offset=7&docid=BNGBJECD0011179O&version=A
# http://3g.163.com/touch/comment.html?#docid=BNGBJECD0011179O&board=mobile_bbs&title=%25E4%25B8%2580%25E5%258A%25A03%25E6%259B%259D%25E5%2585%2589:%25E9%2585%258D6GB%25E8%25BF%2590%25E8%25A1%258C%25E5%2586%2585%25E5%25AD%2598&from=article
# http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/BNGBJECD0011179O/comments/newList?offset=10&limit=10&headLimit=3&tailLimit=1&callback=newList&ibc=newswap

class Handler(BaseHandler):
    crawl_config = {
      'headers': {'User-Agent': IphoneSafari}
    }

    source_news_list_url =u"http://3g.163.com/touch/article/list/{category}/{offset}-10.html"
    source_one_news_url = u'http://3g.163.com/touch/article.html?docid={docid}&version=A'
    source_one_news_detail = u'http://3g.163.com/touch/article/{docid}/full.html'
    source_one_news_comment = u'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{docid}/comments/newList?offset={offset}&limit=30&headLimit=3&tailLimit=1&callback=newList&ibc=newswap'
    category_list = [u"BA8J7DG9wangning",u'BCR0CBQ2wangning',u'BBM54PGAwangning',u'BA8DOPCSwangning']
    category_dict = {
        "recommand":u"BA8J7DG9wangning",
        "news":u"BBM54PGAwangning",
        "car":u"BA8DOPCSwangning",
        "military":u"BAI67OGGwangning",
        "technology":u"BA8D4A3Rwangning",
        "finacial":u"BA8EE5GMwangning",
        "sports":u"BA8E6OEOwangning",
    }
    pages = range(0,3)

    _all_category_page_url_tube = [(source_news_list_url.format(category=c[1],offset=p*10),c[0]) \
                                    for c,p in product(category_dict.items(),pages)]
    
    
    @every(minutes=4 * 60)
    def on_start(self):
        add_task = lambda t:self.crawl(t[0],callback=self.news_list,save={'category':t[1]})
        map(add_task,self._all_category_page_url_tube)
         

    @config(age=60)
    def news_list(self, response):
        """
        response.xpath method is available
        实际的新闻数量少了一些，那是因为我过滤了一部分，那部分是图片或者special专题
        """
        news_list =  json.loads(response.text[9:-1])
        #return news_list
        for k,v in news_list.items():
            for one in v:
                if not one.has_key("skipType"):
                    # 不是special 图片等等的新闻
                    category = response.save.get("category")

                    docid = one.get("docid")
                    comment_count = one.get("commentCount")
                    comment_count = 2100 if comment_count > 2100 else comment_count

                    news_detail_url = self.source_one_news_detail.format(docid=one.get("docid"))
                    news_taskid = md5(news_detail_url).hexdigest()
                    pass2next = {'news_digest':one,"docid":docid,"category":category}
                    self.crawl(news_detail_url,callback=self.news_detail,save=pass2next)
                    comment_page_total = comment_count / 30
                    getcomment = lambda url,age:self.crawl(url,callback=self.comments,save={"__parent__":news_taskid},age=age)
                    for p in range(0,comment_page_total):
                        comment_url = self.source_one_news_comment.format(docid=docid,offset=30*p)
                        getcomment(comment_url,-1)
                        
                    last_comment_url = self.source_one_news_comment.format(docid=docid,offset=30*comment_page_total)
                    getcomment(last_comment_url,58*60)
                    
                    
    @config(age=60)                
    def news_detail(self,response):
        news_detail =  json.loads(response.text[12:-1])
        news_digest = response.save.get("news_digest")
        docid = response.save.get("docid")
        category = response.save.get("category")
        one_news = {
          "docid":docid,
          "news_detail":news_detail.get(docid),
          "news_digest":news_digest,
          "category":category,
        }
        return one_news
    
    @config(age=60)
    def comments(self,response):
        replys =  json.loads(response.text[9:-3])
        refer = response.save.get("__parent__")
        for k,v in replys["comments"].items():
            one_comment = dict(v,**{"__refer__":refer,"__extraid__":k})
            yield one_comment