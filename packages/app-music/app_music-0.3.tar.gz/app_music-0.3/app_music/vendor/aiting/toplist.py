#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:14
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : toplist
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 7.1.1 异步请求榜单分类
class GetTopListCategoryAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=Group_RankList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=Group_RankList
        """
        super(GetTopListCategoryAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 7.1.2 同步请求榜单分类
class GetTopListCategorySync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=Group_RankList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=Group_RankList
        """
        super(GetTopListCategorySync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 7.2.1 异步请求榜单描述列表
class GetTopListDescAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        size=3
        length=100
        offset=0
        categorycode=Genre_RankList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStationItem?size=3&length=100&offset=0
        &categorycode=Genre_RankList
        """
        super(GetTopListDescAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStationItem'


# 7.2.2 同步请求榜单描述列表
class GetTopListDescSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        size=3
        length=100
        offset=0
        categorycode=Genre_RankList
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStationItem?size=3&length=100&offset=0
        &categorycode=Genre_RankList
        """
        super(GetTopListDescSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStationItem'


# 7.3.1 根据榜单类型异步请求榜单音乐列表
class GetTopListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=10
        length=100
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=10&length=100&offset=0
        """
        super(GetTopListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'


# 7.3.2 根据榜单类型请求榜单音乐列表
class GetTopListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=10
        length=100
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=10&length=100&offset=0
        """
        super(GetTopListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
