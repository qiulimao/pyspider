## cleaner
----------

`cleaner` 数据清洗的模块。当您采用`xpath`解析内容时，您可以采用这个模块。`pyquery`暂时不能使用这个清洗模块

假如当您通过xpath提取到的内容是这样的：

```python
    title = response.xpath("#title/text()")
    moive_description = response.xpath("#div[@id='description']/p/text()")
    comment = response.xpath("#div[@class='comment-container']/p[@class='cmt']/text()")
```

提取之后的结果是这样的：

```json

    {
        "title":[u"  让子弹飞 "],
        "movie_description":[u"  电影的导演   ",u"演员有：范冰冰.....",u"目前的评分是：9分",u"票价是:...."],
        "comment":[u" aljdf      ",u"lkajsld.....",u"alksjdf    alsdjflksadf "],
        
    }
```

但是您想要的效果是这样的：

```json

    {
        "title":u"让子弹飞",
        "movie_description":"电影的导演演员有：范冰冰.....目前的评分是：9分票价是:....",
        "comment":[u"aljdf",u"lkajsld.....",u"alksjdfalsdjflksadf"],
        
    }
```

您注意到，在您的结果当中有些不必要的空格，也有一些不太符合您的存储结构，您需要在数据上做一些调整。需要去除title字段多余的空格，电影的
描述需要链接成一段，不能是一个数组。coment当中还是保持数组格式，但是需要将每条评论的多余空格去除。
在之前我们先介绍 一部分`cleaner`。
## basic cleaners
---

###   JoinCleaner

将一个数据连成一个字符串。功能和python 字符串内置的`join`方法一样
另外，您可以使用 `set_serperator`方法设置字段之间的分隔符。
默认中间没有分隔符。如果您想设置为换行，在使用`JoinCleaner`之前调用`JoinCleaner.set_serperator('\n')`

> 输入是一个 `list` 或者 `tube`，输入是一个 `str`

###   TakeFirst

仅仅取数组当中的第一个元素。

>   输入是一个 `list` 或者 `tube`，输入是一个 这个`iteral`的第一个元素
    
###   StripBlankMoreThan2
    
将两个以上的空格替换为一个空格

>   输入必须是一个`str` 输入也是`str`
    
###   DoNothingCleaner
这个`cleaner`什么也不做，仅仅是为了占位。
>   输入任意，什么也不做，直接输出。

##  mapreduce clean
---
接下来介绍三个重要的方法：

###   mapclean

*    参数：

    *  resposne
    
        `callback`当中传入的`reponse`当然也可以是一个`response.xpath()`返回结果的一个元素。
        >   大多数时候 `response.xpath()`返回的是一个`list`

    * xpath_selector
    
        xpath的选择器

    * cleaners 
    
        `cleaner`部分介绍的一些`cleaner`，您也可以自定义`cleaner`（这是下一节的内容）
        `cleaners`必须是由`cleaner`组成的数组或者元组。
            
*    作用：

将每个`cleaner`依次作用在数组的**每个元素**上。返回作用结果。

*   例如:

```python
>>> xpath_selector = "#div[@class='comment-container']/p[@class='cmt']/text()"
#如果不采用mapclean
>>> response.xpath(xpath_selector)
[u" aljdf      ",u"lkajsld.....",u"alksjdf    alsdjflksadf "]
# 采用mapcleane
>>> mapclean(response,xpath_selector,(StripBlankMoreThan2,DoNothingCleaner))
[u"aljdf ",u"lkajsld.....",u"alksjdf alsdjflksadf "]

# 多添加了DoNothingCleaner主要是想告诉读者：cleaner可以连续放好几个。
```
    >   `mapclean` 当中的`cleaner`实际上是接收`xpath_selector`提取到的结果的数组的每一个**元素**作为输入对象


###   reduceclean

*   参数：

    *  resposne
    
        `callback`当中传入的`reponse`当然也可以是一个`response.xpath()`返回结果的一个元素。
        >   大多数时候 `response.xpath()`返回的是一个`list`

    * xpath_selector
    
        xpath的选择器

    * cleaners 
    
        `cleaner`部分介绍的一些`cleaner`，您也可以自定义`cleaner`（这是下一节的内容）
        `cleaners`必须是由`cleaner`组成的数组或者元组。
            
*   作用：

将每个`cleaner`依次作用在**整个数组**上。如果其中某个`cleaner`将数组改变成了一个字符串，而且这个`cleaner`后面如果还有cleaner那么后面这个`cleaner`接收到的输入将是这个字符串，不在是数组，返回作用结果。

*   例如:

```python
>>> xpath_selector = "#div[@id='description']/p/text()"
# 如果不采用mapclean
>>> response.xpath(xpath_selector)
[u"  电影的导演   ",u"演员有：范冰冰.....",u"目前的评分是：9分",u"票价是:...."]
# 采用reducecleane
>>> reduceclean(response,xpath_selector,(JoinCleaner,DoNothingCleaner))
u"   电影的导演     演员有：范冰冰.....目前的评分是：9分票价是:...."

# 多添加了DoNothingCleaner主要是想告诉读者：cleaner可以连续放好几个。
```

###   mapreduce

*   参数：
    *   response
    
        `callback`当中传入的`reponse`当然也可以是一个`response.xpath()`返回结果的一个元素。
        >   大多数时候 `response.xpath()`返回的是一个`list`    
        
    *   xpath_selector
    
        xpath的选择器
     
    *   mapcleaners
        
        元祖或者数组，数组当中的每个元素为`cleaner`类
        
    *   reducecleaners
    
        元祖或者数组，数组当中的每个元素为`cleaner`类
        
*   作用

先对提取到的结果`list`的**每一个元素**作用` mapcleaners`,然后再将结果给每个`reducecleaner`依次作用，最终输出结果。
    
*   例如

```python
>>> xpath_selector = "#div[@id='description']/p/text()"
#如果不采用mapclean
>>> response.xpath(xpath_selector)
[u"  电影的导演   ",u"演员有：范冰冰.....",u"目前的评分是：9分",u"票价是:...."]
#采用reducecleane
>>> mapreduce(response,xpath_selector,(StripBlankMoreThan2,),(JoinCleaner,DoNothingCleaner))
u" 电影的导演 演员有：范冰冰.....目前的评分是：9分票价是:...."

#多添加了DoNothingCleaner主要是想告诉读者：cleaner可以连续放好几个。
```

>   `StripBlankMoreThan2`先对`lis`t当中的每一个元素去除多余的空格，这一步为`map`，`map`的到的结果再给`reduce`，这里的`reduce` 为`(JoinCleaner,DoNothingCleaner)`，作用和前面的`reduceclean`类似
    


### 自定义cleaner

显然这几个内置的`cleaner`不能满足您的需求，但是您可以通过继承 `weblocust.libs.cleaners.BaseCleaner`,并实现`doapply`方法来定制您自己的`cleaner`

例如：
```python
from weblocust.libs.cleaners import BaseCleaner

class MyOwnCleaner(BaseCleaner):
    
    @classmethod
    def doapply(cls,raw_input):
        """
        do your clean job.
        raw_input 为原始你要处理的数据。
        如果在mapclean方法中，raw_input 是list中的一个元素
        在reduceclean方法中，raw_input 是整个一个list，或者被其它cleaner处理过后的数据。   
        """
        pass
        
```
>   `doapply`是一个`classmethod`！！！！