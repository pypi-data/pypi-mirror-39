#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-12 下午3:47
# @Author  : Enoch.Xiang
# @Site    : shanghai
# @File    : service
# @Contact : xiangwenzhuo@yeah.net
"""

import traceback
import database.definition as base
import database.operation as operation
import mq.mess as mess
import vendor.aiting.search as search
import vendor.aiting.others as others
import app.musicAI.musicAIAPI as rec
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception
import datetime

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def hottags(params):
    """热门标签"""
    LOG.info('hottags service:')
    LOG.info('params is %s', params)
    try:
        text = {'length': '40', 'offset': '0', 'categorycode': 'Genre_KV_Hot'}
        res = search.GetHotKeywordSync(text).get()
        res2 = res['response']['docs']['nodeLists']
        return result.SearchResult(res=res2)
    except Exception:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def associate(params):
    """关键词联想匹配"""
    LOG.info('associate service:')
    LOG.info('params is %s', params)
    try:
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
            text = {'start': '0', 'rows': '10', 'searchvalue': searchvalue}
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        res = search.GetSearchSuggestionSync(text).get()
        if 'facet_counts' in res.keys():
            res2 = res['facet_counts']['facet_fields']['name_auto']
        else:
            res2 = 'No Result'
        return result.SearchResult(res=res2)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def music(params):
    """单曲搜索"""
    LOG.info('music service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'pageSize' in params.keys():
            page_size = int(params['pageSize'])
        else:
            page_size = 50
        res = rec.searchItemAPI(searchvalue, vin, uid, pageSize=page_size)
        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(res=res, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def artist(params):
    """歌手搜索"""
    LOG.info('artist service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'pageSize' in params.keys():
            page_size = int(params['pageSize'])
        else:
            page_size = 50
        res = rec.searchArtistAI(searchvalue, vin, uid, pageSize=page_size)
        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(res=res, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def album(params):
    """专辑搜索"""
    LOG.info('album service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'pageSize' in params.keys():
            page_size = int(params['pageSize'])
        else:
            page_size = 50
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        res = rec.searchAlbumAI(searchvalue, vin, uid, pageSize=page_size)
        if not res:
            res = 'No Result'
        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(res=res, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def list(params):
    """歌单搜索"""
    LOG.info('list service:')
    LOG.info('params is %s', params)
    try:
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        text = {'start': '0', 'rows': '50', 'searchvalue': searchvalue}
        res = others.SearchPlaylistSync(text).get()
        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(res=res, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def combine(params):
    """综合搜索"""
    LOG.info('list service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        if 'searchvalue' in params.keys():
            searchvalue = params['searchvalue']
        else:
            return result.ErrorResult(exception.NoKeyWordError())
        if 'pageSize' in params.keys():
            page_size = int(params['pageSize'])
        else:
            page_size = 50
        if 'uid' in params.keys():
            uid = params['uid']
        else:
            uid = None
        rec_music = rec.searchItemAPI(searchvalue, vin, uid, pageSize=page_size)
        rec_album = rec.searchAlbumAI(searchvalue, vin, uid, pageSize=page_size)
        rec_artist = rec.searchArtistAI(searchvalue, vin, uid, pageSize=page_size)
        res = {'music': rec_music, 'album': rec_album, 'artist': rec_artist}
        info = params
        message = mess.SearchWordsHistory(method='add', info=info)
        return result.SearchResult(res=res, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def gethistory(params):
    """获取搜索记录"""
    LOG.info('gethistory service:')
    LOG.info('params is %s', params)
    try:
        vin = params['vin']
        uid = params['uid']
        conn = base.Connect()
        his = operation.SearchWordHistory(vin, uid, conn=conn)
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(720)
        res = his.get(start_time, end_time)
        conn.close()
        return result.SearchResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def clearhistory(params):
    """清空搜索记录"""
    LOG.info('delhistory service:')
    LOG.info('params is %s', params)
    try:
        # info = params
        # message = mess.SearchWordsHistory(method='clear', info=info)
        # res = 'Success.'
        # return result.SearchResult(res=res, message=message)
        vin = params['vin']
        uid = params['uid']
        conn = base.Connect()
        his = operation.SearchWordHistory(vin, uid, conn=conn)
        res = his.clear()
        conn.close()
        if res:
            return result.SearchResult(res='Success.')
        return result.ErrorResult(exception.SQLConnectError())
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
