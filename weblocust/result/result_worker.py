#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
# Author: Binux<i@binux.me>
#         http://binux.me
#
# Contributor: qiulimao<qiulimao@getqiu.com>
#         http://www.getqiu.com
#
# Created on 2014-10-19 15:37:46
# Modified on 2016-11-01 20:07:33

import time
import json
import logging
from six.moves import queue as Queue
from inspect import isgeneratorfunction
from collections import Iterable

logger = logging.getLogger("result")


class ResultWorker(object):

    """
    do with result
    override this if needed.
    """

    def __init__(self, resultdb, inqueue):
        self.resultdb = resultdb
        self.inqueue = inqueue
        self._quit = False

    def on_result(self, task, result):
        '''Called every result'''
        if not result:
            return
        if 'taskid' in task and 'project' in task and 'url' in task:
            logger.info('result %s:%s %s -> %.30r' % (
                task['project'], task['taskid'], task['url'], result))

            return self.resultdb.save(
                project=task['project'],
                taskid=taskid,
                url=task['url'],
                result=result
            )
        else:
            logger.warning('result UNKNOW -> %.30r' % result)
            return

    def quit(self):
        self._quit = True

    def run(self):
        '''Run loop'''
        logger.info("result_worker starting...")

        while not self._quit:
            try:
                task, result = self.inqueue.get(timeout=1)
                self.on_result(task, result)
            except Queue.Empty as e:
                continue
            except KeyboardInterrupt:
                break
            except AssertionError as e:
                logger.error(e)
                continue
            except Exception as e:
                logger.exception(e)
                continue

        logger.info("result_worker exiting...")


class OneResultWorker(ResultWorker):
    '''Result Worker for one mode, write results to stdout'''
    def on_result(self, task, result):
        '''Called every result'''
        if not result:
            return
        if 'taskid' in task and 'project' in task and 'url' in task:
            logger.info('result %s:%s %s -> %.30r' % (
                task['project'], task['taskid'], task['url'], result))
            print(json.dumps({
                'taskid': task['taskid'],
                'project': task['project'],
                'url': task['url'],
                'result': result,
                'updatetime': time.time()
            }))
        else:
            logger.warning('result UNKNOW -> %.30r' % result)
            return

class AdvanceResultWorker(ResultWorker):

    def on_result(self,task,result):
        '''Called every result'''
        if not result:
            return
        if 'taskid' in task and 'project' in task and 'url' in task:
            logger.info('result %s:%s %s -> %.30r' % (
                task['project'], task['taskid'], task['url'], result))

            taskid = task["taskid"]

            # use advance save 
            return self.resultdb.asave(
                project=task['project'],
                taskid=taskid,
                url=task['url'],
                result=result
            )
        else:
            logger.warning('result UNKNOW -> %.30r' % result)
            return        