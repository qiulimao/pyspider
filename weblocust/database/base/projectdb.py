#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-02-09 11:28:52
# Modified on 2016-10-26 20:46:20

import re

# NOTE: When get/get_all/check_update from database with default fields,
#       all following fields should be included in output dict.
{
    'project': {
        'name': str,
        'group': str,
        'status': str,
        'script': str,
        # 'config': str,
        'comments': str,
        # 'priority': int,
        'rate': int,
        'burst': int,
        'updatetime': int,
    }
}


class ProjectDB(object):
    status_str = [
        'TODO',
        'STOP',
        'CHECKING',
        'DEBUG',
        'RUNNING',
    ]

    def insert(self, name, obj={}):
        raise NotImplementedError

    def update(self, name, obj={}, **kwargs):
        raise NotImplementedError

    def get_all(self, fields=None):
        raise NotImplementedError

    def get(self, name, fields):
        raise NotImplementedError

    def drop(self, name):
        raise NotImplementedError

    def check_update(self, timestamp, fields=None):
        raise NotImplementedError

    def split_group(self, group, lower=True):
        return re.split("\W+", (group or '').lower())

    def verify_project_name(self, name):
        if len(name) > 64:
            return False
        if re.search(r"[^\w]", name):
            return False
        return True

    def copy(self):
        '''
        database should be able to copy itself to create new connection

        it's implemented automatically by weblocust.database.connect_database
        if you are not create database connection via connect_database method,
        you should implement this
        '''
        raise NotImplementedError
