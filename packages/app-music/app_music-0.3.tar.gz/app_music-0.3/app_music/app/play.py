#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""play
用于获取播放链接以及单曲信息。
"""

import traceback
import mq.mess as mess
from utils import logger
import utils.result as result
import utils.exception as exception
import utils.decorator as decorator
import vendor.aiting.music as aiting


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def music(params):
    """单曲信息
    :param:  params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "itemid": 9546550}, itemid为单曲id。
    :return: result.Result, 若请求成功，则返回success，否则抛出相应异常。
    """
    LOG.info('music service:')
    LOG.info('params is %s', params)
    try:
        if 'itemid' in params.keys():
            itemid = params['itemid']
        else:
            return result.ErrorResult(exception.NoItemIdError())
        text = {'itemid': itemid}
        res = aiting.GetMusicSync(text).get()
        if not res:
            return result.PlayResult(res='No Result.')
        return result.PlayResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def play(params):
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
                'memberin': '64C1E08BA58D9DED'}
        res = aiting.GetMusicFileSync(text).get()
        res2 = aiting.GetMusicSync(text).get()
        res3 = {'file': res, 'musicinfo': res2}
        info = params
        message = mess.SongHistoryList(method='add', info=info)
        return result.PlayResult(res=res3, message=message)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
