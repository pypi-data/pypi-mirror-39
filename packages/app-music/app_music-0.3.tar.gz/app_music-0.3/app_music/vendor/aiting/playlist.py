#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:34
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : playlist
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 13.1.1 异步请求歌单分类
class GetPlaylistCategoryAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=Group_SongList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=Group_SongList
        """
        super(GetPlaylistCategoryAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 13.1.2 同步请求歌单分类
class GetPlaylistCategorySync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=Group_SongList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=Group_SongList
        """
        super(GetPlaylistCategorySync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 13.2.1 异步获取歌单列表
class GetPlayListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_SongList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStation?length=20&offset=0
        &categorycode=Genre_SongList
        """
        super(GetPlayListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStation'


# 13.2.2 同步获取歌单列表
class GetPlayListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_SongList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStation?length=20&offset=0
        &categorycode=Genre_SongList
        """
        super(GetPlayListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStation'


# 13.3.1 异步获取歌单详情
class GetPlayListInfoAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=8251
        length=100
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=8251&length=100&offset=0
        """
        super(GetPlayListInfoAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'


# 13.3.2 同步获取歌单详情
class GetPlayListInfoSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=8251
        length=100
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=8251&length=100&offset=0
        """
        super(GetPlayListInfoSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
