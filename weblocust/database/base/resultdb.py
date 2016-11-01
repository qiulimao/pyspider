#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-10-11 18:40:03
# Modified on 2016-11-01 20:07:33
import random 
import time
# result schema
{
    'result': {
        'taskid': str,  # new, not changeable
        'project': str,  # new, not changeable
        'url': str,  # new, not changeable
        'result': str,  # json string
        'updatetime': int,
    }
}


class ResultDB(object):
    """
    database for result
    """
    projects = set()  # projects in resultdb

    def save(self, project, taskid, url, result):
        raise NotImplementedError

    def select(self, project, fields=None, offset=0, limit=None):
        raise NotImplementedError

    def count(self, project):
        raise NotImplementedError

    def get(self, project, taskid, fields=None):
        raise NotImplementedError

    def drop(self, project):
        raise NotImplementedError

    def copy(self):
        '''
        database should be able to copy itself to create new connection

        it's implemented automatically by weblocust.database.connect_database
        if you are not create database connection via connect_database method,
        you should implement this
        '''
        raise NotImplementedError

# the flowing function is to support new ui interface and new function
# added by qiulimao@2016.11.01

    def desc_result_with_meta(self,project,taskid,url,result):
        """
            get meta infomation from result,then compose new result
        """
        meta = result.pop("meta",{})

        resultWithMeta = {
            'taskid':taskid,
            'extraid':meta.get("__extraid__",str(random.randrange(100000,999999))),
            'refer':meta.get("__refer__","__self__"),
            'url':url,
            'result':result,
            'updatetime':time.time(),}

        return resultWithMeta

    
    def size(self,project):
        raise NotImplementedError

    def remove(self,project):
        raise NotImplementedError

    def ensure_index(self,project):
        """
        """
        raise NotImplementedError

    def count_by(self,project,condition):
        
        raise NotImplementedError


    def select_by(self,project,offset,limit,condition):
        raise NotImplementedError