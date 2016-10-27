#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-02-23 00:19:06
# Modified on 2016-10-26 20:46:20


import sys
import time
import socket
import inspect
import datetime
import traceback
from flask import render_template, request, json
#from flask.ext import login
import flask_login as login 
from weblocust.libs import utils, sample_handler, dataurl
from weblocust.libs.response import rebuild_response
from weblocust.processor.project_module import ProjectManager, ProjectFinder
from .app import app

default_task = {
    'taskid': 'data:,on_start',
    'project': '',
    'url': 'data:,on_start',
    'process': {
        'callback': 'on_start',
    },
}
default_script = inspect.getsource(sample_handler)


@app.route("/debug/clear/taskdb/<project>",methods=['GET','POST'])
def clear_taskdb(project):
    """
        clear all the tasks in taskdb
    """
    taskdb = app.config['taskdb']
    resultdb = app.config['resultdb']
    taskdb.remove(project)
    return json.dumps({"taskdbsize":taskdb.size(project),"resultdbsize":resultdb.size(project)}),200,{'Content-Type':"application/json"}



@app.route("/debug/clear/resultdb/<project>",methods=['GET','POST'])
def clear_resultdb(project):
    """
        clear all the results in resultdb 
    """
    taskdb = app.config['taskdb']
    resultdb = app.config['resultdb']
    resultdb.remove(project)
    return json.dumps({"taskdbsize":taskdb.size(project),"resultdbsize":resultdb.size(project)}),200,{'Content-Type':"application/json"}

def get_project_info(project):
    """
    """
    taskdb = app.config['taskdb']
    resultdb = app.config['resultdb']
    result = {'taskdbsize':taskdb.size(project),'resultdbsize':resultdb.size(project)}
    return json.dumps(result),200,{'Content-Type':'application/json'}


@app.route("/debug/info/<project>",methods=['GET'])
def project_info(project):
    """
        project infomation
    """
    taskdb = app.config['taskdb']
    resultdb = app.config['resultdb']
    result = {'taskdbsize':taskdb.size(project),'resultdbsize':resultdb.size(project)}
    return json.dumps(result),200,{'Content-Type':'application/json'}


@app.route('/debug/<project>', methods=['GET', 'POST'])
def debug(project):
    """
        project-name:news_163_com
        start-urls:http://news.163.com
        script-mode:script    
    """
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    if info:
        script = info['script']
    else:
        script = (default_script
                  .replace('__DATE__', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                  .replace('__PROJECT_NAME__', project)
                  .replace('__START_URL__', request.values.get('start-urls') or '__START_URL__'))

    taskid = request.args.get('taskid')
    if taskid:
        taskdb = app.config['taskdb']
        task = taskdb.get_task(
            project, taskid, ['taskid', 'project', 'url', 'fetch', 'process'])
    else:
        task = default_task

    default_task['project'] = project
    return render_template("debug.html", task=task, script=script, project_name=project)

@app.route("/debug/create-project",methods=["POST"])
def create_project():
    project_name = request.form.get("project-name")
    #debug(project_name)
    return json.dumps({"ok":1,"project_name":project_name}),200,{'Content-Type': 'application/json'}

@app.before_first_request
def enable_projects_import():
    sys.meta_path.append(ProjectFinder(app.config['projectdb']))


@app.route('/debug/<project>/run', methods=['POST', ])
def run(project):
    start_time = time.time()
    try:
        task = utils.decode_unicode_obj(json.loads(request.form['task']))
    except Exception:
        result = {
            'fetch_result': "",
            'logs': u'task json error',
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), \
            200, {'Content-Type': 'application/json'}

    project_info = {
        'name': project,
        'status': 'DEBUG',
        'script': request.form['script'],
    }

    if request.form.get('webdav_mode') == 'true':
        projectdb = app.config['projectdb']
        info = projectdb.get(project, fields=['name', 'script'])
        if not info:
            result = {
                'fetch_result': "",
                'logs': u' in wevdav mode, cannot load script',
                'follows': [],
                'messages': [],
                'result': None,
                'time': time.time() - start_time,
            }
            return json.dumps(utils.unicode_obj(result)), \
                200, {'Content-Type': 'application/json'}
        project_info['script'] = info['script']

    fetch_result = {}
    try:
        fetch_result = app.config['fetch'](task)
        response = rebuild_response(fetch_result)
        module = ProjectManager.build_module(project_info, {
            'debugger': True
        })
        ret = module['instance'].run_task(module['module'], task, response)
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': fetch_result,
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
    else:
        result = {
            'fetch_result': fetch_result,
            'logs': ret.logstr(),
            'follows': ret.follows,
            'messages': ret.messages,
            'result': ret.result,
            'time': time.time() - start_time,
        }
        result['fetch_result']['content'] = response.text
        if (response.headers.get('content-type', '').startswith('image')):
            result['fetch_result']['dataurl'] = dataurl.encode(
                response.content, response.headers['content-type'])

    try:
        # binary data can't encode to JSON, encode result as unicode obj
        # before send it to frontend
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}
    except Exception:
        type, value, tb = sys.exc_info()
        tb = utils.hide_me(tb, globals())
        logs = ''.join(traceback.format_exception(type, value, tb))
        result = {
            'fetch_result': "",
            'logs': logs,
            'follows': [],
            'messages': [],
            'result': None,
            'time': time.time() - start_time,
        }
        return json.dumps(utils.unicode_obj(result)), 200, {'Content-Type': 'application/json'}


@app.route('/debug/<project>/save', methods=['POST', ])
def save(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    script = request.form['script']
    project_info = projectdb.get(project, fields=['name', 'status', 'group'])
    if project_info and 'lock' in projectdb.split_group(project_info.get('group')) \
            and not login.current_user.is_active():
        return app.login_response

    if project_info:
        # 做更新
        info = {
            'script': script,
        }
        if project_info.get('status') in ('DEBUG', 'RUNNING', ):
            info['status'] = 'CHECKING'
        projectdb.update(project, info)
    else:
        # 创建
        info = {
            'name': project,
            'script': script,
            'status': 'TODO',
            'rate': app.config.get('max_rate', 1),
            'burst': app.config.get('max_burst', 3),
        }
        projectdb.insert(project, info)
        ##
        # we need to ensure_index when new project created
        ##
        taskdb = app.config["taskdb"]
        resultdb = app.config['resultdb']
        taskdb.ensure_index(project)
        resultdb.ensure_index(project)

    rpc = app.config['scheduler_rpc']
    if rpc is not None:
        try:
            rpc.update_project()
        except socket.error as e:
            app.logger.warning('connect to scheduler rpc error: %r', e)
            return 'rpc error', 200

    return 'ok', 200


@app.route('/debug/<project>/get')
def get_script(project):
    projectdb = app.config['projectdb']
    if not projectdb.verify_project_name(project):
        return 'project name is not allowed!', 400
    info = projectdb.get(project, fields=['name', 'script'])
    return json.dumps(utils.unicode_obj(info)), \
        200, {'Content-Type': 'application/json'}


@app.route('/helper.js')
def resizer_js():
    host = request.headers['Host']
    return render_template("helper.js", host=host), 200, {'Content-Type': 'application/javascript'}


@app.route('/helper.html')
def resizer_html():
    height = request.args.get('height')
    script = request.args.get('script', '')
    return render_template("helper.html", height=height, script=script)
