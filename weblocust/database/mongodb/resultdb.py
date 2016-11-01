#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-10-13 22:18:36
# Modified on 2016-11-01 20:07:33

import json
import time
import random 
from pymongo import MongoClient
import pymongo
from weblocust.database.base.resultdb import ResultDB as BaseResultDB
from .mongodbbase import SplitTableMixin


class ResultDB(SplitTableMixin, BaseResultDB):
    collection_prefix = ''

    def __init__(self, url, database='resultdb'):
        self.conn = MongoClient(url)
        self.conn.admin.command("ismaster")
        self.database = self.conn[database]
        self.projects = set()

        self._list_project()
        for project in self.projects:
            collection_name = self._collection_name(project)
            #self.database[collection_name].ensure_index('taskid')
            #self.database[collection_name].create_index('updatetime')
            self.ensure_index(collection_name)

    def _parse(self, data):
        data['_id'] = str(data['_id'])
        if 'result' in data:
            #data['result'] = json.loads(data['result'])
            pass
        return data

    def _stringify(self, data):
        """ it is in mongodb,why stringify this? """
        return data 

        if 'result' in data:
            data['result'] = json.dumps(data['result'])
        return data

    def save(self, project, taskid, url, result):
        collection_name = self._collection_name(project)
        obj = {
            'taskid': taskid,
            'url': url,
            'result': result,
            'updatetime': time.time(),
        }
        return self.database[collection_name].update(
            {'taskid': taskid}, {"$set": self._stringify(obj)}, upsert=True
        )
    ##
    # we have one2many relationship sometimes, add by qiulimao@2016.05.21
    ##




    def asave(self,project,taskid,url,result):
        """
        db.book.update({'user':'body'}, {'$addToSet':{books:{'$each':['心经','楞严经','阿弥陀佛经','金刚经']}});
        """
        collection_name = self._collection_name(project)
        #extraid = result.get("__extraid__")
        #refer = result.get("__refer__")
        # use meta to describle result
        # meta = result.pop("meta",{})

        # obj = {
        #     'taskid': taskid,
        #     'extraid':extraid if extraid else "__main__",
        #     'refer':refer if refer else "__self__",
        #     'url': url,
        #     'result':result,
        #     'updatetime': time.time(),
        # }
        obj = self.desc_result_with_meta(project,taskid,url,result)

        return self.database[collection_name].update({'taskid': obj['taskid'],'extraid':obj['extraid']}, {"$set":obj}, upsert=True)                  

    def select(self, project, fields=None, offset=0, limit=0):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        results = self.database[collection_name].find({}, fields, skip=offset, limit=limit).sort("updatetime",pymongo.DESCENDING)
        for result in results:
            yield self._parse(result)
    ##
    # select by condition
    ##
    def select_by(self,project,condition={},offset=0,limit=0):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        results = self.database[collection_name].find(condition, skip=offset, limit=limit).sort("updatetime",pymongo.DESCENDING)
        for result in results:
            yield self._parse(result)


    def count_by(self,project,condition={}):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        return self.database[collection_name].find(condition).count()
    
    def remove(self,project):
        """
            remove all the results in result database 
        """
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        return self.database[collection_name].remove()

    def size(self,project):
        """
            return the size of result database 
        """
        return self.count(project)


    ##
    # ------------------------------------------------------------------------
    ##
    def count(self, project):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        return self.database[collection_name].count()

    def get(self, project, taskid, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        collection_name = self._collection_name(project)
        ret = self.database[collection_name].find_one({'taskid': taskid}, fields)
        if not ret:
            return ret
        return self._parse(ret)

    def ensure_index(self,collection_name):
        # 因为result 的索引实际上的taskid，所以这里建taskid的索引
        self.database[collection_name].create_index([
                                  ("taskid", pymongo.ASCENDING),
                                  ("extraid", pymongo.ASCENDING)
                                ])
        self.database[collection_name].create_index('updatetime')
        
        self.database[collection_name].create_index([
                                    ('refer',pymongo.DESCENDING),
                                    ("updatetime",pymongo.DESCENDING)
                                    ])
