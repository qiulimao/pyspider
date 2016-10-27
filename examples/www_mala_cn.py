#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-05-24 08:53:10
# Modified on 2016-10-26 20:46:20
# Project: www_mala_cn

from weblocust.libs.base_handler import *
from weblocust.libs.useragent import IphoneSafari,LinuxChrome
from weblocust.libs.cleaners import  TakeFirst,JoinCleaner,StripBlankMoreThan2,reduceclean,mapclean,mapreduce
from hashlib import md5
import re

class Handler(BaseHandler):
    crawl_config = {
        "headers":{
            "User-Agent":LinuxChrome,
            "Cookie":"BDTUJIAID=7a30faefac485c4451ca0f85d1e773d0; _ga=GA1.2.1583355597.1463064808; j1vO_3e8b_saltkey=oXJ07j10; j1vO_3e8b_lastvisit=1464048419; j1vO_3e8b_sendmail=1; j1vO_3e8b_ulastactivity=1464052040%7C0; j1vO_3e8b_auth=f2a0kuBjmA8dKjKRRM9bVX%2B4fYzqIY9T9Kni8VjqCp0TB6Rj73u0oSO6CNzldW2u%2BYfLOIS7mOgKPZH4ZVDDV1KBuebP; j1vO_3e8b_lastcheckfeed=6453872%7C1464052040; j1vO_3e8b_lip=171.217.168.15%2C1464052040; j1vO_3e8b_myrepeat_rr=R0; j1vO_3e8b_onlineusernum=12; yunsuo_session_verify=2392085babaaed74d5053fb187f4f554; j1vO_3e8b_st_p=6453872%7C1464052086%7C394f6e52f94bf98d89dcb34c2c5a4116; j1vO_3e8b_visitedfid=70; j1vO_3e8b_viewid=tid_13605375; j1vO_3e8b_checkpm=1; pgv_pvi=421787374; pgv_info=ssi=s6009804737; j1vO_3e8b_lastact=1464052090%09connect.php%09check; j1vO_3e8b_connect_is_bind=0; CNZZDATA1000273024=277578993-1463059542-%7C1464048153; j1vO_3e8b_smile=1D1; Hm_lvt_c22ba055deeea85b97a72af37a38dae5=1464019728,1464019742,1464019772,1464051929; Hm_lpvt_c22ba055deeea85b97a72af37a38dae5=1464052094"
        }
    }

    @every(minutes=1 * 60)
    def on_start(self):
        self.crawl('http://www.mala.cn/', callback=self.index_page)
    
    
    @config(age=58*60)
    def index_page(self, response):

        for each_url in response.xpath("//a[starts-with(./@href,'http://www.mala.cn/thread-')]/@href"):
            save2next = {"refer":md5(each_url).hexdigest()}
            self.crawl(each_url,callback=self.detail_page,save=save2next)
    

    @config(age=58*60)
    def detail_page(self, response):

        posts = response.xpath("//div[@id='postlist']/div[starts-with(./@id,'post_')]")
        current_page = response.xpath("//div[@id='ct']/div/div[@class='pg']/strong/text()")
        current_page_num = int(current_page[0]) if current_page else 1
        parentid = response.save.get("refer")
        for i,post in enumerate(posts):
            extraid = (current_page_num-1)*20+i
            yield self.parse_one_message(post,parentid,extraid)
        more_page = response.xpath("//div[@id='ct']/div/div[@class='pg']/label/span/text()")
        if more_page:
            total_page = int(re.search("(?P<total_page>\d+)",more_page[0].encode("utf-8")).group("total_page"))
            
            if current_page_num < total_page:
                next_page_url = response.xpath("//div[@id='ct']/div/div[@class='pg']/strong/following-sibling::a[1]/@href")[0]
                age = 58*60 if current_page_num == total_page-1 else -1
                self.crawl(next_page_url,callback=self.detail_page,save={"refer":parentid},age=age)


        
    def parse_one_message(self,part_response,parentid,extraid):
        raw_topic = part_response.xpath(".//td[starts-with(./@id,'postmessage_')]")
        raw_time = part_response.xpath(".//div[@class='authi']/em[starts-with(./@id,'authorposton')]/text()")

        item = {
            "topic":reduceclean(part_response,".//td[starts-with(./@id,'postmessage_')]",JoinCleaner,StripBlankMoreThan2),
            "time":reduceclean(part_response,".//div[@class='authi']/em[starts-with(./@id,'authorposton')]/text()",TakeFirst),
            "__refer__":"__self__" if extraid==0 else parentid,
            "__extraid__":"__main__" if extraid==0 else extraid
        }
        return item
