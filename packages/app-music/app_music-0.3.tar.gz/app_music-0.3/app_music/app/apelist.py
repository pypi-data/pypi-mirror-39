#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/6/27 9:38
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : apelist
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import mq.mess as mess
import vendor.aiting.playlist as playlistapi
import vendor.aiting.music as aiting
from utils import logger
import utils.decorator as decorator
import utils.result as result
import utils.exception as exception

LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def playlist(params):
    """热门标签"""
    LOG.info('apelist service:')
    LOG.info('params is %s', params)
    try:
        text = {'categoryid': '436',
                'length': 50}
        res = playlistapi.GetPlayListInfoSync(text).get()
        res2 = res['response']['docs']['stationItems']
        return result.SearchResult(res=res2)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def playurl(params):
    """播放歌曲
    :param:  params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "itemid": 9546550}, itemid为单曲id。
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('play service:')
    LOG.info('params is %s', params)
    try:
        if 'itemid' in params.keys():
            itemid = params['itemid']
        else:
            return result.ErrorResult(exception.NoItemIdError())
        text = {'itemid': itemid,
                'dltype': 'Streaming',
                'subitemtype': 'FLAC-1000K-FTD'}
        res = aiting.GetMusicFileSync(text).get()
        res2 = aiting.GetMusicSync(text).get()
        res3 = {'file': res, 'musicinfo': res2}
        info = params
        message = mess.SongHistoryList(method='add', info=info)
        return result.PlayResult(res=res3, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
