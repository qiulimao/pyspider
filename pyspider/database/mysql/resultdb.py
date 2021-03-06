#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-10-13 22:02:57
# Modified on 2016-11-02 14:52:53

import re
import six
import time
import json
import mysql.connector

from pyspider.libs import utils
from pyspider.database.base.resultdb import ResultDB as BaseResultDB
from pyspider.database.basedb import BaseDB
from .mysqlbase import MySQLMixin, SplitTableMixin


class ResultDB(MySQLMixin, SplitTableMixin, BaseResultDB, BaseDB):
    __tablename__ = ''

    def __init__(self, host='localhost', port=3306, database='resultdb',
                 user='root', passwd=None):
        self.database_name = database
        self.conn = mysql.connector.connect(user=user, password=passwd,
                                            host=host, port=port, autocommit=True)
        if database not in [x[0] for x in self._execute('show databases')]:
            self._execute('CREATE DATABASE %s' % self.escape(database))
        self.conn.database = database
        self._list_project()

    def _create_project(self, project):
        assert re.match(r'^\w+$', project) is not None
        tablename = self._tablename(project)
        if tablename in [x[0] for x in self._execute('show tables')]:
            return
        # 原先的的primary key是taskid，但是taskid是一个md5值，作为主键，因为innodb采用的聚集索引原因，会导致性能问题。
        # 所以这里新创建一个id字段，作为主键。
        # 并且目前taskid并不唯一
        # 不要每次都创建表，所以加上了IF NOT EXISTS
        self._execute('''CREATE TABLE IF NOT EXISTS %s (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `taskid` varchar(64),
            `url` varchar(1024),
            `extraid` varchar(32),
            `refer` varchar(64),
            `result` MEDIUMBLOB,
            `updatetime` double(16, 4),
            PRIMARY KEY (`id`),
            KEY `taskid__extraid` (`taskid`,`extraid`),
            KEY `refer__updatetime` (`refer`,`updatetime`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 CHARSET=utf8''' % self.escape(tablename))

    def _parse(self, data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, (bytearray, six.binary_type)):
                data[key] = utils.text(value)
        if 'result' in data:
            data['result'] = json.loads(data['result'])
        return data

    def _stringify(self, data):
        if 'result' in data:
            data['result'] = json.dumps(data['result'])
        return data

    def save(self, project, taskid, url, result):
        tablename = self._tablename(project)
        if project not in self.projects:
            self._create_project(project)
            self._list_project()
        obj = {
            'taskid': taskid,
            'url': url,
            'result': result,
            'updatetime': time.time(),
        }
        return self._replace(tablename, **self._stringify(obj))

    def select(self, project, fields=None, offset=0, limit=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)

        for task in self._select2dic(tablename, what=fields, order='updatetime DESC',
                                     offset=offset, limit=limit):
            yield self._parse(task)

    def count(self, project):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return 0
        tablename = self._tablename(project)
        for count, in self._execute("SELECT count(1) FROM %s" % self.escape(tablename)):
            return count

    def get(self, project, taskid, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)
        where = "`taskid` = %s" % self.placeholder
        for task in self._select2dic(tablename, what=fields,
                                     where=where, where_values=(taskid, )):
            return self._parse(task)

# the flowing function is to support new ui interface and new function
# added by qiulimao@2016.11.01  
  
    def size(self,project):
        
        return self.count(project)

    def remove(self,project):
        """
            remove all 
        """
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)        
        self._execute("DELETE FROM %s WHERE 1>0" % self.escape(tablename))

    def ensure_index(self,project):
        return True


    def asave(self, project, taskid, url, result):
        tablename = self._tablename(project)
        if project not in self.projects:
            self._create_project(project)
            self._list_project()

        obj = self.desc_result_with_meta(project,taskid,url,result)

        return self._replace(tablename, **self._stringify(obj))



    def count_by(self,project,condition={}):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return 0
        tablename = self._tablename(project)
        refer = condition.get("refer","__self__")

        for count, in self._execute(
            "SELECT count(1) FROM %s where `refer`='%s'" % (self.escape(tablename),refer)):

            return count

    def select_by(self,project,offset,limit,condition={}):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        tablename = self._tablename(project)
        refer = condition.get("refer","__self__")

        # mysql 和 sqlite的符号不一样,mysql是 '%s' 而sqlite 是'?'
        where = "`refer`=%s" % self.placeholder
        for task in self._select2dic(tablename,order='updatetime DESC',
                                     where=where,offset=offset, 
                                     limit=limit,where_values=[refer,]):
            yield self._parse(task)      