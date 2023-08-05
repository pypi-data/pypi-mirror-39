#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-3 上午9:33
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : playhistory
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import datetime

import database.definition as definition
import database.operation as operation

import utils.logger as logger
import utils.result as result
import utils.exception as exception
import utils.decorator as decorator

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def get(params):
    """获取播放历史记录
    :params: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8},
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('get playhistory service:')
    LOG.info('params is %s', params)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(720)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        historylist = operation.SongHistoryList(vin, uid, conn).get(start_time,
                                                                    end_time)
        conn.close()
        return result.PlayHistoryResult(res=historylist)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clear(params):
    """清空历史记录"""
    LOG.info('playhistory service:')
    LOG.info('params is %s', params)

    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        historylist = operation.SongHistoryList(vin, uid, conn).clear()
        conn.close()
        if historylist:
            return result.PlayHistoryResult(res='Success.')
        else:
            return result.ErrorResult(exception.SQLConnectError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
