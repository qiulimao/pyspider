#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-02-09 10:53:19
# Modified on 2016-10-26 20:46:20

import os
import unittest2 as unittest

all_suite = unittest.TestLoader().discover(os.path.dirname(__file__), "test_*.py")
