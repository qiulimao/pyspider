FROM cmfatih/phantomjs
MAINTAINER binux <roy@binux.me>

# install python
RUN apt-get update && \
        apt-get install -y python python-dev python-distribute python-pip && \
        apt-get install -y libcurl4-openssl-dev libxml2-dev libxslt1-dev python-lxml python-mysqldb libpq-dev

# install requirements
RUN pip install http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.3.zip#md5=710479afc4f7895207c8f96f91eb5385
ADD requirements.txt /opt/weblocust/requirements.txt
RUN pip install -r /opt/weblocust/requirements.txt
RUN pip install -U pip

# add all repo
ADD ./ /opt/weblocust

# run test
WORKDIR /opt/weblocust
RUN pip install -e .[all]

VOLUME ["/opt/weblocust"]
ENTRYPOINT ["weblocust"]

EXPOSE 5000 23333 24444 25555
