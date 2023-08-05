#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-3 上午10:18
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : recommend
# @Contact : xiangwenzhuo@yeah.net
"""

import traceback
import json
import vendor.aiting.playlist as playlist
import app.musicAI.musicAIAPI as rec
import redis
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Root1q2w')
CACHE = redis.Redis(connection_pool=POOL)

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def dailysonglist(params):
    """每日推荐"""
    LOG.info('dailysonglist service:')
    LOG.info('params is %s', params)
    try:
        res = CACHE.get('dailyrec')
        res2 = json.loads(res)
        return result.RecommandResult(res=res2)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def list(params):
    """歌单推荐"""
    LOG.info('list service')
    LOG.info('params is %s', params)
    try:
        text = {'length': '20', 'offset': '0', 'categorycode': 'Genre_SongList'}
        res = playlist.GetPlayListSync(text).get()
        return result.RecommandResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def roewe(params):
    """荣威推荐"""
    LOG.info('roewe service')
    LOG.info('params is %s', params)
    try:
        uid = params['uid']
        vin = params['vin']
        res = CACHE.hget(uid, vin)
        if res is None:
            res3 = CACHE.hget('uid=None', 'vin=None')
            res2 = json.loads(res3)
        else:
            res2 = json.loads(res)
        return result.RecommandResult(res=res2)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def combine(params):
    """综合推荐"""
    LOG.info('combine recommend service')
    LOG.info('params is %s', params)
    try:
        text = {'length': '20', 'offset': '0', 'categorycode': 'Genre_SongList'}
        daily_songs = rec.dailysonglist()
        rec_list = playlist.GetPlayListSync(text).get()
        res = {'dailysongs': daily_songs, 'list': rec_list}
        return result.RecommandResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
