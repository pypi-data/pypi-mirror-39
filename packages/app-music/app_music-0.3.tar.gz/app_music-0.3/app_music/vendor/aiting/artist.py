#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 9:07
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : artist
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 3.1.1请求（热门）音乐人列表
class GetHotArtistListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=50
        offset=0
        categorycode=NL_Artist_HotAll
        example: https://csapi.tingmall.com/ContentServiceWS/CategoryExInfo/
        getCategoryArtist?length=50&offset=0&categorycode=NL_Artist_HotAll
        """
        super(GetHotArtistListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryArtist'


# 3.1.2请求（热门）音乐人列表
class GetHotArtistListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=50
        offset=0
        categorycode=NL_Artist_HotAll
        example: https://csapi.tingmall.com/ContentServiceWS/CategoryExInfo/
        getCategoryArtist?length=50&offset=0&categorycode=NL_Artist_HotAll
        """
        super(GetHotArtistListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryArtist'


# 3.2.1请求音乐人信息(地域)
class GetArtistListInAreaAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        gender=FEMALE
        liteversion=N
        region=MAN
        offset=0
        length=3000
        example: https://csapi.tingmall.com/ContentServiceWS/ArtistInfo/
        getArtistInfoFiltered?gender=FEMALE&liteversion=N&region=MAN&offset=0
        &length=3000
        """
        super(GetArtistListInAreaAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ArtistInfo/getArtistInfoFiltered'


# 3.2.2请求音乐人信息
class GetArtistSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        artistid=31
        example: https://csapi.tingmall.com/ContentServiceWS/ArtistInfo/
        getArtistInfo?artistid=31
        """
        super(GetArtistSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ArtistInfo/getArtistInfo'


# 3.3.1 请求音乐人专辑
class GetArtistAlbumListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemtype=FTD
        length=100
        artistid=91468
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/AlbumInfo/
        getArtistAlbum?itemtype=FTD&length=100&artistid=91468&offset=0
        """
        super(GetArtistAlbumListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AlbumInfo/getArtistAlbum'


# 3.3.2 请求音乐人专辑
class GetArtistAlbumListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemtype=FTD
        length=100
        artistid=91468
        offset=0
        example:  https://csapi.tingmall.com/ContentServiceWS/AlbumInfo/
        getArtistAlbum?itemtype=FTD&length=100&artistid=91468&offset=0
        """
        super(GetArtistAlbumListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AlbumInfo/getArtistAlbum'


# 3.4.1 请求音乐人歌曲
class GetArtistMusicListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        subitemtype=MP3-128K-FTD
        artistid=7208
        offset=0
        length=5
        example:  https://csapi.tingmall.com/ContentServiceWS/ItemInfo/
        getArtistItemBySubItemTypePaged?subitemtype=MP3-128K-FTD&artistid=7208
        &offset=0&length=5
        """
        super(GetArtistMusicListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getArtistItemBySubItemTypePaged'


# 3.4.2 请求音乐人歌曲
class GetArtistMusicListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        subitemtype=MP3-128K-FTD
        artistid=7208
        offset=0
        length=5
        example:  https://csapi.tingmall.com/ContentServiceWS/ItemInfo/
        getArtistItemBySubItemTypePaged?subitemtype=MP3-128K-FTD&artistid=7208
        &offset=0&length=5
        """
        super(GetArtistMusicListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getArtistItemBySubItemTypePaged'


# 3.5.1 请求最新音乐人列表
class GetNewArtistListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=10
        offset=0
        categorycode=NL_Artist_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryArtist?length=10&offset=0&
        categorycode=NL_Artist_Newest
        """
        super(GetNewArtistListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryArtist'


# 3.5.2 请求最新音乐人列表
class GetNewArtistListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=10
        offset=0
        categorycode=NL_Artist_Newest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryArtist?length=10&offset=0
        &categorycode=NL_Artist_Newest
        """
        super(GetNewArtistListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryArtist'
