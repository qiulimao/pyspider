#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-12-04 18:48:15
# Modified on 2016-11-01 20:07:33

import re
import six
import time
import json
import sqlalchemy.exc

from sqlalchemy import (create_engine, MetaData, Table, Column,Index,
                        String, Float, LargeBinary)
from sqlalchemy.engine.url import make_url
from weblocust.database.base.resultdb import ResultDB as BaseResultDB
from weblocust.libs import utils
from .sqlalchemybase import SplitTableMixin, result2dict

import logging

logger = logging.getLogger(__name__)

class ResultDB(SplitTableMixin, BaseResultDB):
    __tablename__ = ''

    def __init__(self, url):
        self.table = Table('__tablename__', MetaData(),
                           Column('taskid', String(64),nullable=False),
                           # 这个taskid不能是unique,所以不能是主键
                           Column('url', String(1024)),
                           Column('result', LargeBinary),
                           Column('updatetime', Float(32)),
                           Column('refer',String(64),default="__self__"),
                           Column('extraid',String(32),default="0"),
                           Index("taskid__extraid",'taskid','extraid'),
                           Index("refer__updatetime",'refer','updatetime'),
                           mysql_engine='InnoDB',
                           mysql_charset='utf8'
                           )

        self.url = make_url(url)
        if self.url.database:
            database = self.url.database
            self.url.database = None
            try:
                engine = create_engine(self.url, convert_unicode=True)
                engine.execute("CREATE DATABASE IF NOT EXISTS %s" % database)
            except sqlalchemy.exc.SQLAlchemyError:
                pass
            self.url.database = database
        self.engine = create_engine(url, convert_unicode=True)

        self._list_project()

    def _create_project(self, project):
        assert re.match(r'^\w+$', project) is not None
        if project in self.projects:
            return
        self.table.name = self._tablename(project)
        self.table.create(self.engine)

    @staticmethod
    def _parse(data):
        for key, value in list(six.iteritems(data)):
            if isinstance(value, six.binary_type):
                data[key] = utils.text(value)
        if 'result' in data:
            if isinstance(data['result'], bytearray):
                data['result'] = str(data['result'])
            data['result'] = json.loads(data['result'])
        return data

    @staticmethod
    def _stringify(data):
        if 'result' in data:
            data['result'] = utils.utf8(json.dumps(data['result']))
        
        if 'extraid' in data:
            data['extraid'] = str(data['extraid'])
        return data

    def save(self, project, taskid, url, result):
        if project not in self.projects:
            self._create_project(project)
            self._list_project()
        self.table.name = self._tablename(project)
        obj = {
            'taskid': taskid,
            'url': url,
            'result': result,
            'updatetime': time.time(),
        }
        if self.get(project, taskid, ('taskid', )):
            del obj['taskid']
            return self.engine.execute(self.table.update()
                                       .where(self.table.c.taskid == taskid)
                                       .values(**self._stringify(obj)))
        else:
            return self.engine.execute(self.table.insert()
                                       .values(**self._stringify(obj)))

    def select(self, project, fields=None, offset=0, limit=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        self.table.name = self._tablename(project)

        columns = [getattr(self.table.c, f, f) for f in fields] if fields else self.table.c
        for task in self.engine.execute(self.table.select()
                                        .with_only_columns(columns=columns)
                                        .order_by(self.table.c.updatetime.desc())
                                        .offset(offset).limit(limit)
                                        .execution_options(autocommit=True)):
            yield self._parse(result2dict(columns, task))

    def count(self, project):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return 0
        self.table.name = self._tablename(project)

        for count, in self.engine.execute(self.table.count()):
            return count

    def get(self, project, taskid, fields=None):
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        self.table.name = self._tablename(project)

        columns = [getattr(self.table.c, f, f) for f in fields] if fields else self.table.c
        for task in self.engine.execute(self.table.select()
                                        .with_only_columns(columns=columns)
                                        .where(self.table.c.taskid == taskid)
                                        .limit(1)):
            return self._parse(result2dict(columns, task))


# the flowing function is to support new ui interface and new function
# added by qiulimao@2016.11.01

    def asave(self, project, taskid, url, result):
        """
            advance save
        """
        if project not in self.projects:
            self._create_project(project)
            self._list_project()
        self.table.name = self._tablename(project)

        obj = self.desc_result_with_meta(project, taskid, url, result)

        # 这里用count来查看是否有重复记录,相当于执行一个upsert操作
        # 但是是不是应该用exists更好?
        existsItemCountProxy =  self.engine.execute(self.table.count()
                               .where(self.table.c.taskid==taskid)
                               .where(self.table.c.extraid==obj['extraid']))

        existsItemCount = existsItemCountProxy.fetchone()

        if existsItemCount[0] != 0L:

            del obj['taskid']
            extraid =  obj.pop("extraid")

            return self.engine.execute(self.table.update()
                                       .where(self.table.c.taskid == taskid)
                                       .where(self.table.c.extraid == extraid)
                                       .values(**self._stringify(obj)))
        else:

            return self.engine.execute(self.table.insert()
                                       .values(**self._stringify(obj)))



    def count_by(self,project,condition={}):
        """
            count the items by some condition.
        """
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return 0
        self.table.name = self._tablename(project)        
        refer = condition.get("refer","__self__")
        for count,in self.engine.execute(self.table.count().where(self.table.c.refer==refer)):
            return count

    

    def select_by(self,project,offset,limit,condition={}):
        """
            select_by conditon.webui module use this function
        """
        if project not in self.projects:
            self._list_project()
        if project not in self.projects:
            return
        
        refer = condition.get("refer","__self__")

        self.table.name = self._tablename(project)
        for one in self.engine.execute(self.table.select()
                                        .where(self.table.c.refer==refer)
                                        .order_by(self.table.c.updatetime.desc())
                                        .offset(offset).limit(limit)
                                        .execution_options(autocommit=True)):

            yield self._parse(result2dict(self.table.c,one))

    def remove(self,project):
        """
            remove all items in result db.
        """
        if project not in self.projects:
            self._create_project(project)
            self._list_project()
        self.table.name = self._tablename(project)

        self.engine.execute(self.table.delete())

    def size(self,project):
        """
            return the size of result.
        """
        return self.count(project)

    def ensure_index(self,project):
        """
            we had create indexes on table schema.
            so return true
        """
        return True
