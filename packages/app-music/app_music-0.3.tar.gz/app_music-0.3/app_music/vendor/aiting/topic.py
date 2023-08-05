#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:07
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : Topic
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 5.1.1 请求专题分类
class GetTopicCategoryAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Group_Subject
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=20&offset=0
        &categorycode=Group_Subject
        """
        super(GetTopicCategoryAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 5.1.2 请求专题分类
class GetTopicCategorySync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Group_Subject
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=20&offset=0
        &categorycode=Group_Subject
        """
        super(GetTopicCategorySync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'


# 5.2.1 请求专题列表
class GetTopicListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_Subject
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStation?length=20&offset=0
        &categorycode=Genre_Subject
        """
        super(GetTopicListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStation'


# 5.2.2 请求专题列表
class GetTopicListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_Subject
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryStation?length=20&offset=0
        &categorycode=Genre_Subject
        """
        super(GetTopicListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryStation'


# 5.3.1 请求专题
class GetTopicAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=2804
        length=100
        offset=0
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=2804&length=100&offset=0
        """
        super(GetTopicAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'


# 5.3.2 请求专题
class GetTopicSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=2804
        length=100
        offset=0
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryItem?categoryid=2804&length=100&offset=0
        """
        super(GetTopicSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryItem'
