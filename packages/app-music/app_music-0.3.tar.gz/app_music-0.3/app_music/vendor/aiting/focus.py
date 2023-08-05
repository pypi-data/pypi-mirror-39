#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:21
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : focus
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 9.1.1 异步请求焦点图分类表
class GetFocusCategoryAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Group_KV
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=SS_Group_KV
        """
        super(GetFocusCategoryAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 9.1.2 同步请求焦点图分类表
class GetFocusCategorySync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Group_KV
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=SS_Group_KV
        """
        super(GetFocusCategorySync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 9.2.2 同步请求焦点图分类描述
class GetFocusNodeSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Genre_KV_Recom
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryNodelist?length=100&offset=0
        &categorycode=SS_Genre_KV_Recom
        """
        super(GetFocusNodeSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryNodelist'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 9.3.1 异步请求焦点图详情
class GetFocusListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_KV_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryKVItem?length=20&offset=0
        &categorycode=NL_KV_Newest
        """
        super(GetFocusListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryKVItem'


# 9.3.2 同步请求焦点图详情
class GetFocusListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_KV_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryKVItem?length=20&offset=0
        &categorycode=NL_KV_Newest
        """
        super(GetFocusListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryKVItem'
