#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-10-19 16:23:55
# Modified on 2016-11-01 20:07:33

from __future__ import unicode_literals

from flask import render_template, request, json
from flask import Response
from .app import app
from weblocust.libs import result_dump


@app.route('/results')
def result():
    resultdb = app.config['resultdb']
    project = request.args.get('project')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 20))

    count = resultdb.count(project)
    results = list(resultdb.select(project, offset=offset, limit=limit))

    return render_template(
        "result.html", count=count, results=results,
        result_formater=result_dump.result_formater,
        project=project, offset=offset, limit=limit, json=json
    )

# chrome may add / automaticly,thus causing 404 Error
@app.route('/result-list/<project>/<int:item_per_page>/<int:page>',methods=['GET', ])
@app.route('/result-list/<project>/<int:item_per_page>/<int:page>/',methods=['GET', ])
def crawleddata(project,item_per_page,page):
    resultdb = app.config['resultdb']
    #project = request.args.get('project')
    #offset = int(request.args.get('offset', 0))
    offset = int(item_per_page)*int(page-1)
    limit = int(item_per_page)

    count = resultdb.count(project)
    results = list(resultdb.select(project, offset=offset, limit=limit))
    #print count,project,results
    reply = {
        "project":project,
        "count":count,
        "results":results,
    }
    #print "ccccc"
    return json.dumps(reply),200,{'Content-Type': 'application/json'}

@app.route('/result-list/<project>/<refer>/<int:item_per_page>/<int:page>/',methods=['GET', ])
def showdata(project,item_per_page,page,refer):
    # refer:__self__  :不是外键，不是别人的一部分
    # extraid:__main__:不是一页当中产生的多个结果之一
    resultdb = app.config['resultdb']

    offset = int(item_per_page)*int(page-1)
    limit = int(item_per_page)

    count = resultdb.count_by(project,condition={"refer":refer})
    #print offset
    #resultdb.select_by(project,offset,limit,{"refer":refer}))
    results = list(resultdb.select_by(project,offset=offset,limit=limit,condition={"refer":refer}))
    #results = []

    reply = {
        "project":project,
        "count":count,
        "results":results,
    }
    return json.dumps(reply),200,{'Content-Type': 'application/json'}

@app.route('/results/dump/<project>.<_format>')
def dump_result(project, _format):
    resultdb = app.config['resultdb']
    # force update project list
    resultdb.get(project, 'any')
    if project not in resultdb.projects:
        return "no such project.", 404

    offset = int(request.args.get('offset', 0)) or None
    limit = int(request.args.get('limit', 0)) or None
    results = resultdb.select(project, offset=offset, limit=limit)

    if _format == 'json':
        valid = request.args.get('style', 'rows') == 'full'
        return Response(result_dump.dump_as_json(results, valid),
                        mimetype='application/json')
    elif _format == 'txt':
        return Response(result_dump.dump_as_txt(results),
                        mimetype='text/plain')
    elif _format == 'csv':
        return Response(result_dump.dump_as_csv(results),
                        mimetype='text/csv')
