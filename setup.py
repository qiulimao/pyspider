#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<roy@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-11-24 22:27:45
# Modified on 2016-10-26 20:46:20


import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

import weblocust

install_requires = [
    'Flask>=0.10',
    'Jinja2>=2.7',
    'chardet>=2.2',
    'cssselect>=0.9',
    'lxml',
    'pycurl',
    'pyquery',
    'sqlalchemy',
    'pymongo',
    'mkdocs',
    'mongoengine',
    'requests>=2.2',
    'tornado>=3.2',
    'Flask-Login>=0.2.11',
    'u-msgpack-python>=1.6',
    'click>=3.3',
    'six>=1.5.0',
]
if sys.version_info < (3, 0):
    install_requires.extend([
        'wsgidav',
    ])

extras_require_all = [
    'mysql-connector-python>=1.2.2',
    'amqp>=1.3.0',
    'pymongo>=2.7.2',
    'SQLAlchemy>=0.9.7',
    'redis',
    'kombu',
    'psycopg2',
    'elasticsearch',
]
if sys.version_info < (3, 0):
    extras_require_all.extend([
        'pika>=0.9.14',
        'beanstalkc',
    ])


setup(
    name='weblocust',
    version=weblocust.__version__,

    description='A more Powerful Spider System in Python based on pyspider',
    long_description=long_description,

    url='https://github.com/qiulimao/weblocust',

    author='qiulimao',
    author_email='qiulimao@getqiu.com',

    license='Apache License, Version 2.0',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'License :: OSI Approved :: Apache Software License',

        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    keywords='scrapy crawler spider webui pyspider weblocust',

    packages=find_packages(exclude=['data', 'tests*']),

    install_requires=install_requires,

    extras_require={
        'all': extras_require_all,
        'test': [
            'unittest2>=0.5.1',
            'coverage',
            'httpbin',
            'pyproxy>=0.1.6',
            'easywebdav',
        ]
    },

    package_data={
        'weblocust': [
            'logging.conf',
            'fetcher/phantomjs_fetcher.js',
            'webui/static/*.css',
            'webui/static/*.js',
            'webui/static/*.less',
            'webui/static/css/*',
            'webui/static/js/*.js',
            'webui/static/js/core/*',
            'webui/static/templates/*.html',
            'webui/static/templates/index_part/*.html',
            'webui/static/image/*',
            'webui/static/fonts/*',
            'webui/templates/*'

        ],
    },

    entry_points={
        'console_scripts': [
            'weblocust=weblocust.run:main'
        ]
    },

    test_suite='tests.all_suite',
)
