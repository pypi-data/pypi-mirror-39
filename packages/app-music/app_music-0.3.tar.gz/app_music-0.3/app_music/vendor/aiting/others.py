#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-26 上午10:19
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : main
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


class SearchAlbumSync(Common):
    def __init__(self, param_dict):
        '''
        allUrl Post: https://csapi.tingmall.com/ContentServiceWS/
        AlbumSearch/searchAlbum?
        headPost Post: oauth_token:sh5980809c318702f777802cdab678210c
        strPost Post: &start=0&rows=1&searchvalue=jay
        '''
        super(SearchAlbumSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AlbumSearch/searchAlbum'

class SearchPlaylistSync(Common):
    def __init__(self, param_dict):
        '''
        allUrl Post: https://csapi.tingmall.com/ContentServiceWS/
        PlaylistSearch/searchPlaylist?
        headPost Post: oauth_token:sh23ff19317e877cd746f5a60594bb2cda
        strPost Post: &start=0&rows=1&searchvalue=jay
        '''
        super(SearchPlaylistSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'PlaylistSearch/searchPlaylist'

class GetAlbumMusicByAlbumIdSync(Common):
    def __init__(self, param_dict):
        '''
        allUrl Post: https://csapi.tingmall.com/ContentServiceWS/
        ItemInfo/getAlbumItemBySubItemTypePaged?
        headPost Post: oauth_token:sh0a11b6f6af1a377952efd5a1fc5b734a
        strPost Post: &albumid=99529&subitemtype=MP3-128K-FTD&offset=0&length=1
        '''
        super(GetAlbumMusicByAlbumIdSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getAlbumItemBySubItemTypePaged'

#
# s = {'length':'25','artists':'刘德华,张学友'}
# a=  CreateRadioByName(s).get()
# print(a)
# s = {'categoryid': '10', 'length': '50', 'offset': '0'}
# a = GetTopListSync(s).get()
# print(a['response']['docs']['stationItems'])

# s = {'length':200,'offset':0,'categorycode':'Genre_SongList'}
# a = GetPlayListSync(s).get()
# print(a)
# for i in a['response']['docs']['stations']:
#     print(i)
#
# s = {'length':1,'offset':0,'categoryid':'13769'}
# a = GetPlayListInfoSync(s).get()
# print(a)

# s = {'itemid':'9537739','bit':'MP3-128K-FT'}
# a = GetMusicSync(s).get()
# print(a)

# s = {'start':'0', 'rows':'100', 'searchvalue':'jay'}
# a=  SearchAlbumSync(s).get()
# print(a)

# s = {'start':'0', 'rows':'100', 'searchvalue':'jay'}
# a=  SearchPlaylistSync(s).get()
# print(a)

# s = {'albumid':'99529','subitemtype':'MP3-128K-FTD','offset':'0','length':'100'}
# a=  GetAlbumMusicByAlbumIdSync(s).get()
# print(a)