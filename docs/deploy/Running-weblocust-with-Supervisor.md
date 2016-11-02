
# supervisor
supervisor 功能及其详细使用案例可以参见 [supervisor](http://supervisord.org/)
# supervisor 配置样例

```
# supervisor 核心配置文件如下:
# 如果采用supervisor,配置文件的位置需要做相应改变

[unix_http_server]
;file=/tmp/supervisor.sock   ; (the path to the socket file)
file=/var/runtime/supervisor.sock   ; (the path to the socket file)
;chmod=0700                 ; socket file mode (default 0700)
;chown=nobody:nogroup       ; socket file uid:gid owner
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))

[inet_http_server]         ; inet (TCP) server disabled by default
port=*:9001        ; (ip_address:port specifier, *:port for all iface)
;username=user              ; (default is no username (open server))
;password=123               ; (default is no password (open server))

[supervisord]
logfile=/var/runtimeLog/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10           ; (num of main logfile rotation backups;default 10)
loglevel=info                ; (log level;default info; others: debug,warn,trace)
pidfile=/var/runtime/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=false               ; (start in foreground if true;default false)
minfds=1024                  ; (min. avail startup file descriptors;default 1024)
minprocs=200                 ; (min. avail process descriptors;default 200)


; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/runtime/supervisor.sock ; use a unix:// URL  for a unix socket
;serverurl=http://0.0.0.0:9001 ; use an http:// url to specify an inet socket
;username=chris              ; should be same as http_username if set
;password=123                ; should be same as http_password if set
;prompt=mysupervisor         ; cmd line prompt (default "supervisor")
;history_file=~/.sc_history  ; use readline history if available


[program:weblocust_phantomjs]
;phantomjs_fetcher.js 这个文件可以由 "weblocust phantomsource" 获得
;command=/usr/app/phantomjs/bin/phantomjs --ssl-protocol=any --disk-cache=true /path/to/phantomjs_fetcher.js 25555
command=weblocust -c /path/toconfigurefile phantomjs 
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/phantomjs.log
stderr_logfile=/var/runtimeLog/weblocust/phantomjs_err.log
autostart=false                ; start at supervisord start (default: true)
priority=300                   ; the relative start priority (default 999)
;stopsignal=KILL               ; phantomjs need this signal to terminate
killasgroup=true               ; kill subprocess. thanks binux's suggestion @2016.11.01

[program:weblocust_scheduler]
;configurefile 可以由 "weblocust -mkconfig"获得
command=weblocust -c /path/to/configurefile scheduler
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/scheduler.log
stderr_logfile=/var/runtimeLog/weblocust/scheduler_err.log
autostart=false                ; start at supervisord start (default: true)
priority=301                   ; the relative start priority (default 999)

[program:weblocust_fetcher]
;configurefile 可以由 "weblocust -mkconfig"获得
command=weblocust -c /path/to/configurefile fetcher
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/fetcher.log
stderr_logfile=/var/runtimeLog/weblocust/fetcher_err.log

autostart=false                ; start at supervisord start (default: true)
priority=302                   ; the relative start priority (default 999)


[program:weblocust_processor]
;configurefile 可以由 "weblocust -mkconfig"获得
command=weblocust -c /path/to/configurefile processor
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/processor.log
stderr_logfile=/var/runtimeLog/weblocust/processor_err.log

autostart=false                ; start at supervisord start (default: true)
priority=303                   ; the relative start priority (default 999)

[program:weblocust_resultworker]
;configurefile 可以由 "weblocust -mkconfig"获得
command=weblocust -c /path/to/configurefile result_worker
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/result_worker.log
stderr_logfile=/var/runtimeLog/weblocust/result_worker_err.log

autostart=false                ; start at supervisord start (default: true)
priority=304                   ; the relative start priority (default 999)

[program:weblocust_webui]
;configurefile 可以由 "weblocust -mkconfig"获得
command=weblocust -c /path/to/configurefile webui
process_name=%(program_name)s  ; process_name expr (default %(program_name)s)
directory=/var/weblocust 
stdout_logfile=/var/runtimeLog/weblocust/webui.log
stderr_logfile=/var/runtimeLog/weblocust/webui_err.log

autostart=false                ; start at supervisord start (default: true)
priority=305                   ; the relative start priority (default 999)

[group:weblocust]
programs=weblocust_phantomjs,weblocust_scheduler,weblocust_fetcher,weblocust_processor,weblocust_resultworker,weblocust_webui
priority=400


```