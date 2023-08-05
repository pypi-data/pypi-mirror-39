#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:16
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : search
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 8.1.1 异步请求搜索建议词
class GetSearchSuggestionAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=10
        searchvalue=%E6%97%A9
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/predictsearchItem?start=0&rows=10&searchvalue=%E6%97%A9
        """
        super(GetSearchSuggestionAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/predictsearchItem'
# {'responseHeader': {'errorinfo': 'Result not found', 'status': '101'}}


# 8.1.2 同步请求搜索建议词
class GetSearchSuggestionSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=10
        searchvalue=%E6%97%A9
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/predictsearchItem?start=0&rows=10&searchvalue=%E6%97%A9
        """
        super(GetSearchSuggestionSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/predictsearchItem'
# {'responseHeader': {'errorinfo': 'Result not found', 'status': '101'}}


# 8.2.1 异步请求搜索结果中文
class SearchMusicAsyncCN(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemtype=FTD
        start=0
        rows=20
        searchvalue=%E6%97%A9
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/searchItem?itemtype=FTD&start=0&rows=20&searchvalue=%E6%97%A9
        """
        super(SearchMusicAsyncCN, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/searchItem'


# 8.2.1 异步请求搜索结果英文或首字母或全拼
class SearchMusicAsyncEN(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemtype=FTD
        start=0
        rows=20
        searchvalue=zjl
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/searchItemPinyin?itemtype=FTD&start=0&rows=20&searchvalue=zjl
        """
        super(SearchMusicAsyncEN, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/searchItemPinyin'


# 8.2.2 同步请求搜索结果中文
class SearchMusicSyncCN(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=10
        searchvalue=%E6%97%A9
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/predictsearchItem?start=0&rows=10&searchvalue=%E6%97%A9
        """
        super(SearchMusicSyncCN, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/searchItem'


# 8.2.2 同步请求搜索结果英文或首字母或全拼
class SearchMusicSyncEN(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemtype=FTD
        start=0
        rows=10
        searchvalue=zjl
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemSearch/searchItemPinyin?itemtype=FTD&start=0&rows=20&searchvalue=zjl
        """
        super(SearchMusicSyncEN, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemSearch/searchItemPinyin'


# 8.3.1 异步获取歌手头像链接
class SearchArtistAvatarAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=1
        searchvalue=%E5%91%A8%E6%9D%B0%E4%BC%A6
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ArtistSearch/searchArtist?start=0&rows=1
        &searchvalue=%E5%91%A8%E6%9D%B0%E4%BC%A6
        """
        super(SearchArtistAvatarAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS' \
                    '/ArtistSearch/searchArtist'


# 8.3.2 同步获取歌手头像链接
class SearchArtistAvatarSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=1
        searchvalue=%E5%91%A8%E6%9D%B0%E4%BC%A6
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ArtistSearch/searchArtist?start=0&rows=1
        &searchvalue=%E5%91%A8%E6%9D%B0%E4%BC%A6
        """
        super(SearchArtistAvatarSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ArtistSearch/searchArtist'


# 8.4.1 根据用户输入的搜索词来获取歌曲，歌手及专辑的讯息。
class AggregateSearchAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=20
        searchvalue=%E5%91%A8
        example:  https://csapi.tingmall.com/ContentServiceWS/
        AggregateSearch/aggregateSearch?start=0&rows=20&searchvalue=%E5%91%A8
        """
        super(AggregateSearchAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AggregateSearch/aggregateSearch'
# {'responseHeader': {'errorinfo': 'Result not found', 'status': 101}}


# 8.4.2 根据用户输入的搜索词来获取歌曲，歌手及专辑的讯息。
class AggregateSearchSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        start=0
        rows=20
        searchvalue=%E5%91%A8
        example:  https://csapi.tingmall.com/ContentServiceWS/
        AggregateSearch/aggregateSearch?start=0&rows=20&searchvalue=%E5%91%A8
        """
        super(AggregateSearchSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AggregateSearch/aggregateSearch'
# {'responseHeader': {'errorinfo': 'Result not found', 'status': 101}}


# 8.5.1 取得热词搜索列表
class GetHotKeywordAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_KV_Hot
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryNodelist?length=20
        &offset=0&categorycode=Genre_KV_Hot
        """
        super(GetHotKeywordAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryNodelist'


# 8.5.2 取得热词搜索列表
class GetHotKeywordSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=Genre_KV_Hot
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryNodelist?length=20
        &offset=0&categorycode=Genre_KV_Hot
        """
        super(GetHotKeywordSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryNodelist'


# 8.6.1 取得热词对应内容
class GetHotResultAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=125
        length=50
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryKVItem?categoryid=125&length=50&offset=0
        """
        super(GetHotResultAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryKVItem'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 8.6.2 取得热词对应内容
class GetHotResultSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        categoryid=125
        length=50
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryKVItem?categoryid=125&length=50&offset=0
        """
        super(GetHotResultSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryKVItem'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}
