#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""collect
用于处理有关收藏的功能。
"""

import traceback
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

import database.operation as operation
import database.definition as definition


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def getsong(params):
    """获取收藏的单曲
    :params: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8}
    :return: result.Result, 返回所有收藏的单曲
    """
    LOG.info('get getsong service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        data = operation.CollectSong(vin, uid).get()
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addsong(params):
    """收藏单曲
    :params: params:dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "itemid":830074} itemid为收藏的单曲id.
    :return: result.Result, 若收藏成功，则返回success，否则抛出数据库异常。若缺少itemid
    关键字，则抛出缺少itemid异常。
    """
    LOG.info('addsong service:')
    LOG.info('params is %s', params)
    try:
        if 'itemid' in params.keys():
            itemid = params['itemid']
            uid = params['uid']
            vin = params['vin']
            timestamp = params['timestamp']
            conn = definition.Connect()
            collect = operation.CollectSong(vin, uid, conn).add(timestamp,
                                                                itemid)
            conn.close()
            if collect == "Success":
                return result.CollectResult(res='Success.')
            elif collect == "Spilled":
                return result.ErrorResult(exception.ExceedCollectLimitError())
            else:
                return result.ErrorResult(exception.SQLConnectError())
        return result.ErrorResult(exception.NoItemIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def delsong(params):
    """取消收藏单曲
    :params: params:dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "itemid":830074} itemid为拟取消收藏的单曲id.
    :return: result.Result, 若取消成功，则返回success，否则抛出数据库异常。若缺少itemid
    关键字，则抛出缺少itemid异常。
    """
    LOG.info('cancel collect service::')
    LOG.info('params is %s', params)
    try:
        if 'itemid' in params.keys():
            itemid = params['itemid']
            uid = params['uid']
            vin = params['vin']
            timestamp = params['timestamp']
            conn = definition.Connect()
            collect = operation.CollectSong(vin,
                                            uid,
                                            conn).cancel(timestamp,
                                                         itemid)
            conn.close()
            if collect:
                return result.CollectResult(res='Success.')
            return result.ErrorResult(exception.SQLConnectError())
        return result.ErrorResult(exception.NoItemIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def getlist(params):
    """获取收藏的歌单
    :params: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8}
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('getlist service:')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        conn = definition.Connect()
        data = operation.CollectPlayList(vin, uid, conn).get()
        conn.close()
        if data is False:
            return result.ErrorResult(exception.SQLConnectError())
        else:
            return result.CollectResult(res=data)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def dellist(params):
    """取消收藏歌单
    :params: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "playlistid":12,"selflist":True}, selflist用于判断是否为自建歌单，
    因为自建歌单id可能会与一般歌单id重复，加此字段加以区分。
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('dellist service:')
    LOG.info('params is %s', params)
    try:
        if 'type' in params.keys():
            listtype = int(params['type'])
            if listtype not in [1, 2, 3]:
                return result.ErrorResult(exception.UnSupportTypeError())
        else:
            return result.ErrorResult(exception.NoSelfListError())
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']

            uid = params['uid']
            vin = params['vin']
            timestamp = params['timestamp']
            conn = definition.Connect()
            collect = operation.CollectPlayList(vin,
                                                uid,
                                                conn).cancel(timestamp,
                                                             playlistid,
                                                             listtype)
            conn.close()
            if collect:
                return result.CollectResult(res='Success.')
            return result.ErrorResult(exception.SQLConnectError())
        return result.ErrorResult(exception.NoPlayListIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def addlist(params):
    """收藏歌单
    :params: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "playlistid":12,"selflist":True}, selflist用于判断是否为自建歌单，
    因为自建歌单id可能会与一般歌单id重复，加此字段加以区分。
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('addlist service:')
    LOG.info('params is %s', params)
    try:
        if 'type' in params.keys():
            typelist = int(params['type'])
            if typelist not in [1, 2, 3]:
                return result.ErrorResult(exception.UnSupportTypeError())
        else:
            return result.ErrorResult(exception.NoListTypeError())
        if 'playlistid' in params.keys():
            playlistid = params['playlistid']
            uid = params['uid']
            vin = params['vin']
            timestamp = params['timestamp']
            conn = definition.Connect()
            collect = operation.CollectPlayList(vin, uid, conn).add(timestamp,
                                                                    playlistid,
                                                                    typelist)
            conn.close()
            if collect:
                return result.CollectResult(res='Success.')
            return result.ErrorResult(exception.SQLConnectError())
        else:
            return result.ErrorResult(exception.NoPlayListIdError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
