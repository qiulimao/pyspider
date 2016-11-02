Command Line
============

Global Config
-------------

You can get command help via `weblocust --help` and `weblocust all --help` for subcommand help.

global options work for all subcommands.

```
Usage: weblocust [OPTIONS] COMMAND [ARGS]...

  A powerful spider system in python.

Options:
  -c, --config FILENAME    a json file with default values for subcommands.
                           {“webui”: {“port”:5001}}
  --logging-config TEXT    logging config file for built-in python logging
                           module  [default: weblocust/weblocust/logging.conf]
  --debug                  debug mode
  --queue-maxsize INTEGER  maxsize of queue
  --taskdb TEXT            database url for taskdb, default: sqlite
  --projectdb TEXT         database url for projectdb, default: sqlite
  --resultdb TEXT          database url for resultdb, default: sqlite
  --message-queue TEXT     connection url to message queue, default: builtin
                           multiprocessing.Queue
  --amqp-url TEXT          [deprecated] amqp url for rabbitmq. please use
                           --message-queue instead.
  --beanstalk TEXT         [deprecated] beanstalk config for beanstalk queue.
                           please use --message-queue instead.
  --phantomjs-proxy TEXT   phantomjs proxy ip:port
  --data-path TEXT         data dir path
  --version                Show the version and exit.
  --help                   Show this message and exit.
```

#### --config

Config file is a JSON file with config values for global options or subcommands (a sub-dict named after subcommand). [example](/deploy/#configjson)


if it is the first time to use `weblocust`,and you know nothing about configure,you can you `weblocust mkconfig` to generate configure file.

``` json
{
  "taskdb": "sqlalchemy+mysql+taskdb://username:password@host:port/taskdb",
  "projectdb": "sqlalchemy+mysql+projectdb://username:password@host:port/projectdb",
  "resultdb": "sqlalchemy+mysql+resultdb://username:password@host:port/resultdb",
  "message_queue": "amqp://username:password@host:port/%2F",
  "webui": {
    "username": "some_name",
    "password": "some_passwd",
    "need-auth": true
  }
}
```

#### --queue-maxsize

Queue size limit, 0 for not limit

#### --taskdb, --projectdb, --resultdb

```

mongodb:
    mongodb+type://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    more: http://docs.mongodb.org/manual/reference/connection-string/
sqlalchemy:
    sqlalchemy+postgresql/mysql+type://user:passwd@host:port/database
    sqlalchemy+mysql+mysqlconnector+type://user:passwd@host:port/database
    more: http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html
mysql:
    mysql+type://user:passwd@host:port/database
sqlite:
    # relative path
    sqlite+type:///path/to/database.db
    # absolute path
    sqlite+type:////path/to/database.db
    # memory database
    sqlite+type://    
local:
    local+projectdb://filepath,filepath
    
type:
    should be one of `taskdb`, `projectdb`, `resultdb`.
```


#### --message-queue

```
rabbitmq:
    amqp://username:password@host:5672/%2F
    see https://www.rabbitmq.com/uri-spec.html
beanstalk:
    beanstalk://host:11300/
redis:
    redis://host:6379/db
kombu:
    kombu+transport://userid:password@hostname:port/virtual_host
    see http://kombu.readthedocs.org/en/latest/userguide/connections.html#urls
builtin:
    None
```

#### --phantomjs-proxy

The phantomjs proxy address, you need a phantomjs installed and running phantomjs proxy with command: [`weblocust phantomjs`](#phantomjs).

#### --data-path

SQLite database and counter dump files saved path


mkconfig
---
```
Usage: weblocust mkconfig [OPTIONS]

  generate simple configure file

Options:
  --filename TEXT    configure file name
  --mongo-host TEXT  mongo host or ip
  --redis-host TEXT  redis host or ip
  --help             Show this message and exit.
```
generate configure file


all
---

```
Usage: weblocust all [OPTIONS]

  Run all the components in subprocess or thread

Options:
  --fetcher-num INTEGER         instance num of fetcher
  --processor-num INTEGER       instance num of processor
  --result-worker-num INTEGER   instance num of result worker
  --run-in [subprocess|thread]  run each components in thread or subprocess.
                                always using thread for windows.
  --help                        Show this message and exit.
```


one
---

```
Usage: weblocust one [OPTIONS] [SCRIPTS]...

  One mode not only means all-in-one, it runs every thing in one process
  over tornado.ioloop, for debug purpose

Options:
  -i, --interactive  enable interactive mode, you can choose crawl url.
  --phantomjs        enable phantomjs, will spawn a subprocess for phantomjs
  --help             Show this message and exit.
```

**NOTE: WebUI is not running in one mode.**

In `one` mode, results will be written to stdout by default. You can capture them via `weblocust one > result.txt`.

#### [SCRIPTS]

The script file path of projects. Project status is RUNNING, `rate` and `burst` can be set via script comments:

```
# rate: 1.0
# burst: 3
```

When SCRIPTS is set, `taskdb` and `resultdb` will use a in-memory sqlite db by default (can be overridden by global config `--taskdb`, `--resultdb`). on_start callback will be triggered on start.

#### -i, --interactive

With interactive mode, weblocust will start an interactive console asking what to do in next loop of process. In the console, you can use:

``` python
crawl(url, project=None, **kwargs)
    Crawl given url, same parameters as BaseHandler.crawl

    url - url or taskid, parameters will be used if in taskdb
    project - can be omitted if only one project exists.
    
quit_interactive()
    Quit interactive mode
    
quit_weblocust()
    Close weblocust
```

You can use `weblocust.libs.utils.python_console()` to open an interactive console in your script.

bench
-----

```
Usage: weblocust bench [OPTIONS]

  Run Benchmark test. In bench mode, in-memory sqlite database is used
  instead of on-disk sqlite database.

Options:
  --fetcher-num INTEGER         instance num of fetcher
  --processor-num INTEGER       instance num of processor
  --result-worker-num INTEGER   instance num of result worker
  --run-in [subprocess|thread]  run each components in thread or subprocess.
                                always using thread for windows.
  --total INTEGER               total url in test page
  --show INTEGER                show how many urls in a page
  --help                        Show this message and exit.
```


scheduler
---------

```
Usage: weblocust scheduler [OPTIONS]

  Run Scheduler, only one scheduler is allowed.

Options:
  --xmlrpc / --no-xmlrpc
  --xmlrpc-host TEXT
  --xmlrpc-port INTEGER
  --inqueue-limit INTEGER  size limit of task queue for each project, tasks
                           will been ignored when overflow
  --delete-time INTEGER    delete time before marked as delete
  --active-tasks INTEGER   active log size
  --loop-limit INTEGER     maximum number of tasks due with in a loop
  --scheduler-cls TEXT     scheduler class to be used.
  --help                   Show this message and exit.
```

#### --scheduler-cls

set this option to use customized Scheduler class

phantomjs
---------

```
Usage: run.py phantomjs [OPTIONS] [ARGS]...

  Run phantomjs fetcher if phantomjs is installed.

Options:
  --phantomjs-path TEXT  phantomjs path
  --port INTEGER         phantomjs port
  --auto-restart TEXT    auto restart phantomjs if crashed
  --help                 Show this message and exit.
```

#### ARGS

Addition args pass to phantomjs command line.

fetcher
-------

```
Usage: weblocust fetcher [OPTIONS]

  Run Fetcher.

Options:
  --xmlrpc / --no-xmlrpc
  --xmlrpc-host TEXT
  --xmlrpc-port INTEGER
  --poolsize INTEGER      max simultaneous fetches
  --proxy TEXT            proxy host:port
  --user-agent TEXT       user agent
  --timeout TEXT          default fetch timeout
  --fetcher-cls TEXT      Fetcher class to be used.
  --help                  Show this message and exit.
```

#### --proxy

Default proxy used by fetcher, can been override by `self.crawl` option. [DOC](apis/self.crawl/#fetch)


processor
---------

```
Usage: weblocust processor [OPTIONS]

  Run Processor.

Options:
  --processor-cls TEXT  Processor class to be used.
  --help                Show this message and exit.
```

result_worker
-------------

```
Usage: weblocust result_worker [OPTIONS]

  Run result worker.

Options:
  --result-cls TEXT  ResultWorker class to be used.
  --help             Show this message and exit.
```


webui
-----

```
Usage: weblocust webui [OPTIONS]

  Run WebUI

Options:
  --host TEXT            webui bind to host
  --port INTEGER         webui bind to host
  --cdn TEXT             js/css cdn server
  --scheduler-rpc TEXT   xmlrpc path of scheduler
  --fetcher-rpc TEXT     xmlrpc path of fetcher
  --max-rate FLOAT       max rate for each project
  --max-burst FLOAT      max burst for each project
  --username TEXT        username of lock -ed projects
  --password TEXT        password of lock -ed projects
  --need-auth            need username and password
  --webui-instance TEXT  webui Flask Application instance to be used.
  --help                 Show this message and exit.
```

#### --cdn

JS/CSS libs CDN service, URL must compatible with [cdnjs](https://cdnjs.com/)

#### --fercher-rpc

XML-RPC path URI for fetcher XMLRPC server. If not set, use a Fetcher instance.

#### --need-auth

If true, all pages require username and password specified via `--username` and `--password`.


phantomsource
---------

@Deprecated 

使用`supervisor`可以直接`weblocust phantomjs`命令启动`phantomjs`模块,
在`program`选项当中加入`killasgroup=true`.因为`phantomjs`代理是运行程序的子进程,不然无法结束,会出现`phantomjs`进程无法结束.

thanks binux @ 2016.11.01

```
Usage: run.py phantomsource [OPTIONS]

  get phantomjs source code if you want to run phantomjs seperately,you can
  get the related js code

Options:
  --help  Show this message and exit.

```
下面这条命令即可运行`phantomjs_proxy.js`,除了路径,不要再修改其它运行参数,除非你非常了解修改后的效果.
```bash
/path/to/phantomjs --ssl-protocol=any --disk-cache=true /path/to/phantomjs_proxy.js 25555
```