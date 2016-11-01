Working with Results
====================
Downloading and viewing your data from WebUI is convenient, but may not suitable for computer.

Working with ResultDB
---------------------
Although resultdb is only designed for result preview, not suitable for large scale storage. But if you want to grab data from resultdb, there are some simple snippets using database API that can help you to connect and select the data.

```
from weblocust.database import connect_database
resultdb = connect_database("<your resutldb connection url>")
for project in resultdb.projects:
    for result in resultdb.select(project):
        assert result['taskid']
        assert result['url']
        assert result['result']
```

The `result['result']` is the object submitted by `return` statement from your script.

Working with ResultWorker
-------------------------
In product environment, you may want to connect weblocust to your system / post-processing pipeline, rather than store it into resultdb. It's highly recommended to override ResultWorker.

```
from weblocust.result import ResultWorker

Class MyResultWorker(ResultWorker):
    def on_result(self, task, result):
        assert task['taskid']
        assert task['project']
        assert task['url']
        assert result
        # your processing code goes here
```

`result` is the object submitted by `return` statement from your script.

You can put this script (e.g., `my_result_worker.py`) at the folder where you launch weblocust. Add argument for `result_worker` subcommand:

`weblocust result_worker --result-cls=my_result_worker.MyResultWorker`

Or

```
{
  ...
  "result_worker": {
    "result_cls": "my_result_worker.MyResultWorker"
  }
  ...
}
```

if you are using config file. [Please refer to Deployment](/Deployment)

Design Your Own Database Schema
-------------------------------
The results stored in database is encoded as JSON for compatibility. It's highly recommended to design your own database, and override the ResultWorker described above.

TIPS about Results
-------------------
#### Want to return more than one result in callback?
As resultdb de-duplicate results by taskid(url), the latest will overwrite previous results.

One workaround is using `send_message` API to make a `fake` taskid for each result.

```
def detail_page(self, response):
    for li in response.doc('li'):
        self.send_message(self.project_name, {
            ...
        }, url=response.url+"#"+li('a.product-sku').text())

def on_message(self, project, msg):
    return msg
```

See Also: [apis/self.send_message](/apis/self.send_message)

### 更好的解决一对多的关系

因为我们有很多时候会遇到要采集评论，论坛等内容，`weblocust`当中的这些方法不是那么奏效。
在`weblocust`当中你可以轻松的处理这类关系,`weblocust`在`result`当中引入这`meat`这个个变量：

`meta`变量当中包含:

*   `__refer__`

    `__refer__`是指这条结果的父`id`，比如您采集的对象是新闻，那么评论的`__refer__`可以设置为新闻主题内容的`id`.
    有点类似于关系型数据库当中的`ForeignKey`.
    
*   `__extraid__`

    `__extraid__`是指如果你设置了`__refer__`，实际上这条记录在在数据库当中的`resultid`,可能是一样的。
    比如都是`md5(url)`获得当前结果的`id`,那么我们可以给这个记录加一个`__extraid__`实现区分。如果不加这条属性，那么只有最后一条记录才能被记录。
    
>   默认 `__refer__='__self__'`  ;   `__extraid__=a_random_number`.


### 灵活的存储每条记录

在实际当中，可能每一个页面都会对应有结果输出，但是他们的结构却不近相同。您也可能需要把结果存到`mysql`当中。这时你可以提供一个`on_result__callback`方法。

其中`callback`为 `crawl`的回调函数的函数名。当然，如果您本身就希望数据存在`mongodb`当中，那么您不用管理存储，`weblocust` will handle it for you!~

例如：
```python

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    def on_result__detail_page(self,result):
        """
            这里可以将result存入您的mysql数入库。
        """
        pass

```

>   我不是很推荐通过这种方式将数据存在数据库中。直接在`resultdb`（`mongodb`）当中导出结果到你想要的地方我觉得会更方便一些。

>   如果您非要用这种方式将结果写入您的关系型数据库中(`mysql`,`postgreslq`),请使用**ORM**,推荐使用`peewee`或者是`sqlalchemy`