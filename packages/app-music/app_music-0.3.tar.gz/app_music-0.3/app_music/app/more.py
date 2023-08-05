#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""more
用于获取各分类的详细信息。
"""

import traceback
from utils import logger
import utils.result as result
import utils.exception as exception
import utils.decorator as decorator

import vendor.aiting.artist as artist
import vendor.aiting.playlist as playlist
import vendor.aiting.lyric as lyricapi
import vendor.aiting.others as others


LOG = logger.get_logger(__name__)
params_check = decorator.params_check


@params_check
def artistinfo(params):
    """请求音乐人信息
    :param: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "artistid":21821}, artistid为歌手编号。
    :return: result.Result, 若请求成功，则返回音乐人信息，否则抛出相应异常。
    """
    LOG.info('artistinfo service:')
    LOG.info('params is %s', params)
    try:
        if 'artistid' in params.keys():
            artistid = params['artistid']
        else:
            return result.ErrorResult(exception.NoArtistIdError())
        text = {'artistid': artistid, 'offset': '0', 'length': '20'}
        res = artist.GetArtistMusicListSync(text).get()
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def albuminfo(params):
    """专辑信息
    :param: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "albumid":578147}, albumid为专辑编号。
    :return: result.Result, 若请求成功，则返回专辑信息，否则抛出相应异常。
    """
    LOG.info('albuminfo service:')
    LOG.info('params is %s', params)
    try:
        if 'albumid' in params.keys():
            albumid = params['albumid']
        else:
            return result.ErrorResult(exception.NoAlbumIdError())
        text = {'albumid': albumid,
                'subitemtype': 'MP3-128K-FTD',
                'length': '50'}
        res = others.GetAlbumMusicByAlbumIdSync(text).get()
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def listinfo(params):
    """歌单信息
    :param: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "categoryid":13283}, categoryid为分类编号。
    :return: result.Result, 若请求成功，则返回分类信息，否则抛出相应异常。
    """
    LOG.info('listinfo service:')
    LOG.info('params is %s', params)
    try:
        if 'categoryid' in params.keys():
            categoryid = params['categoryid']
        else:
            return result.ErrorResult(exception.NoCategoryIdIdError())
        text = {'categoryid': categoryid, 'length': '100', 'offset': '0'}
        res = playlist.GetPlayListInfoSync(text).get()
        if not res:
            return result.MoreInfoResult(res='No result.')
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())


@params_check
def lyric(params):
    """歌词信息
    :param: params: dict, {"vin": "LSJA0123456789112",
    "uid": 123456, "timestamp":1529477063.8,
    "itemid": 9546550}, itemid为单曲id。
    :return: result.Result, 若请求成功，则返回歌词信息，否则抛出相应异常。
    """
    LOG.info('lyric service:')
    LOG.info('params is %s', params)
    try:
        if 'itemid' in params.keys():
            itemid = params['itemid']
        else:
            return result.ErrorResult(exception.NoItemIdError())
        text = {'subitemtype': 'LRC-LRC', 'itemid': itemid}
        res = lyricapi.GetLyricUrlSyncById(text).get()
        if not res:
            return result.MoreInfoResult(res='No result.')
        return result.MoreInfoResult(res=res)
    except:
        traceback.print_exc()
        return result.ErrorResult(exception.InternalError())
