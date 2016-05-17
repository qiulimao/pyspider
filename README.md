pyspider [![Build Status]][Travis CI] [![Coverage Status]][Coverage] [![Try]][Demo]
========

A Powerful Spider(Web Crawler) System in Python. **[TRY IT NOW!][Demo]**

- Write script in Python
- Powerful WebUI with script editor, task monitor, project manager and result viewer
- [MySQL](https://www.mysql.com/), [MongoDB](https://www.mongodb.org/), [Redis](http://redis.io/), [SQLite](https://www.sqlite.org/), [Elasticsearch](https://www.elastic.co/products/elasticsearch); [PostgreSQL](http://www.postgresql.org/) with [SQLAlchemy](http://www.sqlalchemy.org/) as database backend
- [RabbitMQ](http://www.rabbitmq.com/), [Beanstalk](http://kr.github.com/beanstalkd/), [Redis](http://redis.io/) and [Kombu](http://kombu.readthedocs.org/) as message queue
- Task priority, retry, periodical, recrawl by age, etc...
- Distributed architecture, Crawl Javascript pages, Python 2&3, etc...

Tutorial: [http://docs.pyspider.org/en/latest/tutorial/](http://docs.pyspider.org/en/latest/tutorial/)  
Documentation: [http://docs.pyspider.org/](http://docs.pyspider.org/)  
Release notes: [https://github.com/binux/pyspider/releases](https://github.com/binux/pyspider/releases)  

Sample Code 
-----------

```python
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://scrapy.org/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        """ you can use response.xpath now,just like scrapy,
            It also support extract,just like scrapy's extrace,but you need to 
            from pyspider.libs.response import Response
            Response.extract(response.xpath("//a"))
            this static method will help you extract content of <a>
        """
        for url in response.xpath("//a[starts-with(./@href,'http://')]/@href"):
            self.crawl(each.url, callback=self.detail_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
```

And the web center
------------------

[![Demo][Demo Img]][Demo]


Installation
------------

* you need to run `git clone https://github.com/qiulimao/pyspider.git` then `$python setup.py install`
* run command `pyspider`, visit [http://localhost:5000/](http://localhost:5000/)

Quickstart: [http://docs.pyspider.org/en/latest/Quickstart/](http://docs.pyspider.org/en/latest/Quickstart/)

Contribute
----------

* Use Angularjs to rebuild the ui module
* more resonable way to save data in mongodb
* extra method on parsing the html
* parameters optimized


TODO
----

### next

- [ ] read more source code
- [ ] make better ui
- [ ] better user authentic


### more

- [x] edit script with vim via [WebDAV](http://en.wikipedia.org/wiki/WebDAV)
- [x] binux is realy COW B!!!!


License
-------
Licensed under the Apache License, Version 2.0


[Build Status]:         https://img.shields.io/travis/binux/pyspider/master.svg?style=flat
[Travis CI]:            https://travis-ci.org/binux/pyspider
[Coverage Status]:      https://img.shields.io/coveralls/binux/pyspider.svg?branch=master&style=flat
[Coverage]:             https://coveralls.io/r/binux/pyspider
[Try]:                  https://img.shields.io/badge/try-pyspider-blue.svg?style=flat
[Demo]:                 http://demo.pyspider.org/
[Demo Img]:             http://www.getqiu.com/static/image/pyspider-angularjs.png
[Issue]:                https://github.com/binux/pyspider/issues
[User Group]:           https://groups.google.com/group/pyspider-users
