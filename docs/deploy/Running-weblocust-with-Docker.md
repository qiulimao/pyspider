```shell
# mysql
docker run --name mysql -d -v /data/mysql:/var/lib/mysql -e MYSQL_ALLOW_EMPTY_PASSWORD=yes mysql:latest
# rabbitmq
docker run --name rabbitmq -d rabbitmq:latest

# phantomjs
docker run --name phantomjs -d binux/weblocust:latest phantomjs

# result worker
docker run --name result_worker -m 128m -d --link mysql:mysql --link rabbitmq:rabbitmq binux/weblocust:latest result_worker
# processor, run multiple instance if needed.
docker run --name processor -m 256m -d --link mysql:mysql --link rabbitmq:rabbitmq binux/weblocust:latest processor
# fetcher, run multiple instance if needed.
docker run --name fetcher -m 256m -d --link phantomjs:phantomjs --link rabbitmq:rabbitmq binux/weblocust:latest fetcher --no-xmlrpc
# scheduler
docker run --name scheduler -d --link mysql:mysql --link rabbitmq:rabbitmq binux/weblocust:latest scheduler
# webui
docker run --name webui -m 256m -d -p 5000:5000 --link mysql:mysql --link rabbitmq:rabbitmq --link scheduler:scheduler --link phantomjs:phantomjs binux/weblocust:latest webui
```

or running with [Docker Compose](https://docs.docker.com/compose/) with `docker-compose.yml`:

NOTE: It's recommended to run mysql and rabbitmq outside compose as they may not been restarted with weblocust. You can find commands to start mysql and rabbitmq service above.

```
phantomjs:
  image: binux/weblocust:latest
  command: phantomjs
result:
  image: binux/weblocust:latest
  external_links:
    - mysql
    - rabbitmq
  command: result_worker
processor:
  image: binux/weblocust:latest
  external_links:
    - mysql
    - rabbitmq
  command: processor
fetcher:
  image: binux/weblocust:latest
  external_links:
    - rabbitmq
  links:
    - phantomjs
  command : fetcher
scheduler:
  image: binux/weblocust:latest
  external_links:
    - mysql
    - rabbitmq
  command: scheduler
webui:
  image: binux/weblocust:latest
  external_links:
    - mysql
    - rabbitmq
  links:
    - scheduler
    - phantomjs
  command: webui
  ports:
    - "5000:5000"
```

`docker-compose up`


