#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:11
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : freshmusic
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 6.1.1 异步请求新歌速递歌曲列表
class GetFreshMusicListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=30
        offset=0
        categorycode=ST_SongList_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?length=30&offset=0
        &categorycode=ST_SongList_Newest
        """
        super(GetFreshMusicListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
# {'responseHeader': {'errorinfo': ' categoryid Invalid .', 'status': '5001'}}


# 6.1.2 同步请求新歌速递歌曲列表
class GetFreshMusicListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=30
        offset=0
        categorycode=ST_SongList_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?length=30&offset=0
        &categorycode=ST_SongList_Newest
        """
        super(GetFreshMusicListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
# {'responseHeader': {'errorinfo': ' categoryid Invalid .', 'status': '5001'}}


# 6.2.1 异步请求热门歌曲列表
class GetHotMusicListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=30
        offset=0
        categorycode=ST_SongList_Hotest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?length=30&offset=0
        &categorycode=ST_SongList_Hotest
        """
        super(GetHotMusicListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
# {'responseHeader': {'errorinfo': ' categoryid Invalid .', 'status': '5001'}}


# 6.2.2 同步请求热门歌曲列表
class GetHotMusicListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=30
        offset=0
        categorycode=ST_SongList_Hotest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?length=30&offset=0
        &categorycode=ST_SongList_Hotest
        """
        super(GetHotMusicListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
# {'responseHeader': {'errorinfo': ' categoryid Invalid .', 'status': '5001'}}
