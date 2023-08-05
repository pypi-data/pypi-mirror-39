#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:31
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : lyric
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 11.2.1 同步根据歌曲名和歌手名获取歌词URL
class GetLyricUrlSyncByName(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        liteversion=N
        artistname=%E6%9C%B4%E5%AE%9D%E8%93%9D
        length=1
        offset=0
        itemname=%EC%98%88%EB%BB%90%EC%A1%8C%EB%8B%A4
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemInfo/getItemInfoByName?liteversion=N
        &artistname=%E6%9C%B4%E5%AE%9D%E8%93%9D&length=1&offset=0
        &itemname=%EC%98%88%EB%BB%90%EC%A1%8C%EB%8B%A4
        """
        super(GetLyricUrlSyncByName, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getItemInfoByName'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 11.2.2 同步根据歌曲ID获取歌词URL
class GetLyricUrlSyncById(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        subitemtype=LRC-LRC
        itemid= + itemId
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ContentFileInfo/getLyricURL?subitemtype=LRC-LRC&itemid= + itemId
        """
        super(GetLyricUrlSyncById, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ContentFileInfo/getLyricURL'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}
