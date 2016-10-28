## 开发工具

在工程目录下提供了一个`./manange.py`的开发类工具,可以帮助开发人员解决一些琐碎的工作,你可以
运行`./manange.py --help` 查看全部的选项和使用帮助

```
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

  some tools to easy your developing job.

Options:
  --help  Show this message and exit.

Commands:
  mkdocs          make documents
  modifydate      change the modified date on all the file...
  newcontributor  new contributer to weblocust project
  newmodifydate   create modified date on py files
  rmdocs          remove the documents
```

### mkdocs 

这个自命令主要帮助您生成`html`格式的文档,生成后的文档默认的配置文件为`project`目录下的`mkdocs.yml`
文件.生成后的文档将放在您制定的`path`路径下(采用相对路径),默认为`./weblocust/webui/static/`,另外采用`mkdocs`生成的`html`文档
可能会有`google`字体.`mkdocs`命令已经采用`find`+`sed`帮您替换成了国内镜像
```                                                                                                     
Usage: manage.py mkdocs [OPTIONS]                                                                                                                              
                                                                                                                                                               
  make documents                                                                                                                                               
                                                                                                                                                               
Options:                                                                                                                                                       
  --path TEXT  place the docs to somewhere in relative path                                                                                                    
  --help       Show this message and exit.
```

### rmdocs 

和`mkdocs`相对应.这个命令用来删除文档

```                                                                                                          
Usage: manage.py rmdocs [OPTIONS]                                                                                                                                  
                                                                                                                                                                   
  remove the documents                                                                                                                                             
                                                                                                                                                                   
Options:                                                                                                                                                           
  --path TEXT                                                                                                                                                      
  --help       Show this message and exit. 
```

### newcontributor

如果您参与了`weblocust`的修改,您的名字应该出现在源代码的`list`上.这个命令可以在您修改过的文件上添加您的大名.
```                                                                                              
Usage: manage.py newcontributor [OPTIONS]                                                                                                                      
                                                                                                                                                               
  new contributer to weblocust project                                                                                                                         
                                                                                                                                                               
Options:                                                                                                                                                       
  --name TEXT        your name                                                                                                                                 
  --email TEXT       your email                                                                                                                                
  --website TEXT     your website                                                                                                                              
  --daysago INTEGER  modified time before now                                                                                                                  
  --help             Show this message and exit.  
```
这个命名会提示您填写相关的信息.其中需要注意的参数是`daysago`这个参数代表几天以前修改过的`.py`文件会加上您的名字.默认是`1`天以前.
比如您今天修改了`10`个文件,运行这个命令将在py文件开头将会变为类似下面的样子
```
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-03-05 00:11:49
```
目前这个命令考虑的方面不是特别完全,如果你今天从`github`上`clone`了`weblocust`库,
并且今天运行这条命名,那么所有的`py`文件都会被添加上这些信息.

### newmodifydate

你可以通过这条命令来向您当天修改过的文件添加日期,默认修改一天以内修改过的文件.
但是目前这个命名没有考虑到重复添加的问题.对于`weblocust`,这个命名我已经运行过了,所以后续不要在运行了,因为会添加重复.
直接运行`./manange.py modifydate`即可

```                                                                                                 
Usage: manage.py newcontributor [OPTIONS]                                                                                                                          
                                                                                                                                                                   
  new contributer to weblocust project                                                                                                                             
                                                                                                                                                                   
Options:                                                                                                                                                           
  --name TEXT        your name                                                                                                                                     
  --email TEXT       your email                                                                                                                                    
  --website TEXT     your website                                                                                                                                  
  --daysago INTEGER  modified time before now                                                                                                                      
  --help             Show this message and exit. 
```
运行之后，对应的文件会做相应的修改
```
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Created on 2014-03-05 00:11:49
# Modified on 2016-10-26 20:46:20
```

### modifydate

更改修改的日期.如果您已经添加了修改日期,那么可以运行这个命名修改更改日期.

```                                                                                                     
Usage: manage.py modifydate [OPTIONS]                                                                                                                              
                                                                                                                                                                   
  change the modified date on all the file which you have modified by in the                                                                                       
  past daysago to NOW()                                                                                                                                            
                                                                                                                                                                   
Options:                                                                                                                                                           
  --daysago INTEGER  modified time before now                                                                                                                      
  --help             Show this message and exit.  
```

### 最终效果

正确运行`newcontributor,newmodifydate,modifydate`命令最后在修改过的`py`文件中大概会是这个样子

```
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-03-05 00:11:49
# Modified on 2016-10-26 20:46:20
```