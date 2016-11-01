weblocust Tutorial
=================

> The best way to learn how to scrap is learning how to make it.

* [Level 1: HTML and CSS Selector](HTML-and-CSS-Selector)
* [Level 2: AJAX and More HTTP](AJAX-and-more-HTTP)
* [Level 3: Render with PhantomJS](Render-with-PhantomJS)
* [Level 4: Data Cleaner](Data-Cleaner)

If you have problem using weblocust, [user group](https:#groups.google.com/group/weblocust-users) is a place for discussing.

Note:

* 上面的4个level学习之前建议先了解`pyquery`和`xpath`
* `weblocust`采用`pyquery`和`xpath`解析网页内容。如果您需要对网页当中的`dom`做修改之后再存如数据库，或者您非常熟悉使用`jquery`推荐您使用`pyquery`.
* 其它场景推荐使用`xpath`。

##  关于xpath和pyquery
---

如果您对`xpath`不是很熟悉，那么推荐您阅读 [w3school的xpath教程](http:#www.w3school.com.cn/xpath/)。
如果您对`pyquery`不熟悉,可以参见 [pyquery官方网站](https://pythonhosted.org/pyquery/)

### 来看下面这个使用`pyquery`和`xpath`的例子
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
        self.crawl('http:#scrapy.org/', callback=self.index_page)

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
        
```
对于以上的 `index_page`方法，您也可以采用`xpath`,这样写：

```python
    ......
    
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each_link in response.xpath("#a/@href"):
            self.crawl(each_link, callback=self.detail_page)    
            
    ......
    
```

