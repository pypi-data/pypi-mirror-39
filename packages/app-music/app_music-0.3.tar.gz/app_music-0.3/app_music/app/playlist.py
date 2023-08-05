#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-3 上午9:37
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : playlist
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import database.operation as operation
import database.definition as definition

from utils import logger
import utils.decorator as decorator
import utils.exception as exception
import utils.result as result
import mq.mess as mess


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def getplaylist(params):
    """获取用户歌单"""
    LOG.info('getplaylist service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        conn = definition.Connect()
        data = operation.UserPlaylist(vin, uid, conn).get()
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.PlayListResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getplaylistcontent(params):
    """获取用户歌单内容"""
    LOG.info('getplaylistcontent service:')
    LOG.info('params is %s', params)
    try:
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']
        else:
            return result.ErrorResult(exception.NoPlayListIdError())
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        data = operation.UserPlaylist(vin, uid, conn).getplaylistcontent(playlistid)
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.PlayListResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def add(params):
    """增加单曲"""
    LOG.info('add service:')
    LOG.info('params is %s', params)
    try:
        if 'playlistid' not in params.keys():
            return result.ErrorResult(exception.NoPlayListIdError())
        if 'itemid' in params.keys():
            info = params
            message = mess.UserPlaylist(method='add', info=info)
            return result.PlayListResult(res='Received', message=message)
        return result.ErrorResult(exception.NoItemIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delete(params):
    """删除单曲"""
    LOG.info('collect service:')
    LOG.info('params is %s', params)
    try:
        if 'playlistid' not in params.keys():
            return result.ErrorResult(exception.NoPlayListIdError())
        if 'itemid' in params.keys():
            info = params
            message = mess.UserPlaylist(method='cancel', info=info)
            return result.PlayListResult(res='Received', message=message)
        return result.ErrorResult(exception.NoItemIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def create(params):
    """创建用户歌单"""
    LOG.info('get collect service:')
    LOG.info('params is %s', params)
    try:
        if 'playlistname' in params.keys():
            playlistname = params['playlistname']
        else:
            return result.ErrorResult(exception.NoPlayListNameError())
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        data = operation.UserPlaylist(vin, uid, conn).create(playlistname)
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.PlayListResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
