weblocust
========

A Powerful Spider(Web Crawler) System in Python based on **pyspider**.

- Write script in Python
- more Powerful WebUI with script editor, task monitor, project manager and result viewer than weblocust
- [MongoDB](https://www.mongodb.org/), as database backend
- [RabbitMQ](http://www.rabbitmq.com/), [Beanstalk](http://kr.github.com/beanstalkd/), [Redis](http://redis.io/) and [Kombu](http://kombu.readthedocs.org/) as message queue
- Task priority, retry, periodical, recrawl by age, etc...
- Distributed architecture, Crawl Javascript pages, Python 2&3, etc...


release Note
-----------
虽然`pyspider`这个框架是一个国人写的。但是他在英国工作，英文牛逼。`pyspider`在`python`的爬虫方面不仅仅只在国内有名气。
在国外也有很多人使用。所以作者没有想过要专门写一份中文的文档。在他的博客当中有一些早期版本的介绍和使用。虽然现在更新得比较快，
但是使用方式上基本没怎么变。内部的结构可能有所改变。

`pyspider`作者昵称叫bunix,感觉作者很牛,很博学,。再此表示敬佩.
`weblocust` 是我根据我们的需求在`pyspider`上做了一些改进，使得更加符合我们的需求。`pyspider`原本支持很多`resultdb`
我仅仅在`mongodb` 作为`resultdb`之上做优化。如果您采用`mysql`存储，可能将不会有`weblocust`的新特性。

主要的改进：

*   `webui` 部分的改进。这部分实际上bunix已经做得很好了。为了有更好的操控体验和显示效果，我更改了这个模块的大部分内容。
*   原先的`js`,`css`等文件都放在云端，我将它放在了本地。我觉得虽然没网爬虫不能用，但是有些时候我们也需要浏览结果。
*   更改了`mongodb`存储`result`的结构。我觉`mongodb`的`schemaless`恰好解决爬虫字段变化大的问题，所以应该充分利用这样的特性，因此没有必要和`mysql`做统一。
*   对网页内容提取增加了`xpath`方法。
*   `response`对`scrapy`部分兼容,因为我觉得`scrapy`的`linkextractor`很好用，如果你运行的`python`版本是2.7，那你可以使用`scrapy`的`linkextractor`。
*   加入数据清洗模块`cleaner`.这个模块的实现方式受`scrapy`的启发。
*   提供`OnePageHasManyItem`,`OneItemHasManySubItem`的一站式解决方案。尤其适合博客的评论，论坛回帖等网页。
*   提供灵活的存储方式，目前`pyspider`一旦运行只能采取一种`result_worker`使得存储相当不灵活。`weblocust`当中您可以在任何一个结果当中定义自己的存储方式。
*   增加了一些开发者使用的小工具,比如自动在文件中生成修改时间,添加新的作者,自动部署文档等等
*   修复了一些bug

关于文档：
这份文档潜在的读者是中国人，所以文档就在bunix的文档之上修改。中文部分是我新加的,英文部分有少许修改或者添加。另外我将文档和代码中的`pyspider`都换成了`weblocust`并不是想掩盖`weblocust`
是基于`pyspider`,仅仅是为了统一工程命名.源代码当中`author`一栏始终留着`binux`的位置,我把自己加在了`contributor`一栏.

Sample Code 
-----------

```python
from weblocust.libs.base_handler import *
from weblocust.libs.useragent import IphoneSafari,LinuxChrome
from weblocust.libs.cleaners import  TakeFirst,JoinCleaner,StripBlankMoreThan2
from weblocust.libs.cleaners import  reduceclean,mapclean,mapreduce

class Handler(BaseHandler):
    crawl_config = {
      'headers': {'User-Agent': LinuxChrome},
      "cookie":"a=123",
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://scrapy.org/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
    def on_result__detail_page(self,result):
        """ you can save the results on your own demand """
        pass
```
WebUI
---------

![Demo Img]


Installation
you can install weblocust in 2 ways
------------
1.   the most convenient way `pip install weblocust` 
2.   install from source code `git clone https://github.com/qiulimao/weblocust.git` then `$python setup.py install`

then run `weblocust mkconfig` to generate simple configure file.

finally: run command `weblocust -c generatedfilename`, visit [http://localhost:5000/](http://localhost:5000/)

Contribute
----------


TODO
----

### next version
* keep in space




### more

- [x] edit script with vim via [WebDAV](http://en.wikipedia.org/wiki/WebDAV)


License
-------
Licensed under the Apache License, Version 2.0


[Demo Img]:             imgs/demo.png
[Issue]:                https://github.com/qiulimao/webocust/issues


[Demo Img]:             docs/imgs/demo.png
[Issue]:                https://github.com/qiulimao/webocust/issues

