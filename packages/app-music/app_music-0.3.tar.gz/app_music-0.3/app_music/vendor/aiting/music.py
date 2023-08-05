#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:24
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : music
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 10.1.1 请求歌曲的详细信息
class GetMusicAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        liteversion=N
        itemid=1111
        bit=MP3-128K-FTD
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemInfo/getItemInfo?liteversion=N&itemid=1111&bit=MP3-128K-FTD
        """
        super(GetMusicAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getItemInfo'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 10.1.2 请求歌曲的详细信息
class GetMusicSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        liteversion=N
        itemid=1111
        bit=MP3-128K-FTD
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ItemInfo/getItemInfo?liteversion=N&itemid=1111&bit=MP3-128K-FTD
        """
        super(GetMusicSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ItemInfo/getItemInfo'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 10.1.3 获取歌曲的下载地址
class GetMusicFileAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemid=1525353
        subitemtype=MP3-128K-FTD
        memberid=64C1E08BA58D9DED
        dltype=Streaming
        example:  https://api.97ting.com/StreamingAndDownloadWS/
        confirmDownload?dltype=Streaming&itemid=1525353
        &subitemtype=MP3-128K-FTD&memberid=64C1E08BA58D9DED
        """
        super(GetMusicFileAsync, self).__init__(param_dict)
        self._url = ' https://csapi.tingmall.com/StreamingAndDownloadWS/' \
                    'confirmDownload'
# {'responseHeader': {'errorinfo': 'OAuth token expiried - 175.102.15.242',
# 'status': '1202'}}


# 10.1.4 获取歌曲的下载地址
class GetMusicFileSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        dltype=Streaming
        itemid=1525353
        subitemtype=MP3-128K-FTD
        memberid=64C1E08BA58D9DED
        example:  https://api.97ting.com/StreamingAndDownloadWS/
        confirmDownload?dltype=Streaming&itemid=1525353
        &subitemtype=MP3-128K-FTD&memberid=64C1E08BA58D9DED
        """
        super(GetMusicFileSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/StreamingAndDownloadWS/' \
                    'confirmDownload'
# {'responseHeader': {'errorinfo': 'OAuth token expiried - 175.102.15.242',
# 'status': '1202'}}


# 10.2.1 请求歌曲的分享信息#获取歌曲的分享信息同时包含歌曲的歌词地址
class ShareMusicSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemid=1111
        memberid=531D3F1F7389EDB95569BB40AF7AEF08
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ShareInfo/shareSong?itemid=1111
        &memberid=531D3F1F7389EDB95569BB40AF7AEF08
        """
        super(ShareMusicSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ShareInfo/shareSong'
# {'responseHeader': {'errorinfo': 'SH member not exist. [memberid]',
# 'status': '1102'}}


# 10.2.1 请求歌曲的分享信息#获取歌曲的歌词地址
class ShareMusicSyncLyric(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemid=1111
        subitemtype=LRC-LRC
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ContentFileInfo/getLyricURL?subitemtype=LRC-LRC&itemid=1111
        """
        super(ShareMusicSyncLyric, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ContentFileInfo/getLyricURL'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 10.2.2 请求歌曲的分享信息#获取歌曲的分享信息同时包含歌曲的歌词地址
class ShareMusicAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemid=1111
        memberid=531D3F1F7389EDB95569BB40AF7AEF08
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ShareInfo/shareSong?itemid=1111
        &memberid=531D3F1F7389EDB95569BB40AF7AEF08
        """
        super(ShareMusicAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ShareInfo/shareSong'
# {'responseHeader': {'errorinfo': 'SH member not exist. [memberid]',
# 'status': '1102'}}


# 10.2.2 请求歌曲的分享信息#获取歌曲的歌词地址
class ShareMusicAsyncLyric(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        itemid=1111
        subitemtype=LRC-LRC
        example:  https://csapi.tingmall.com/ContentServiceWS/
        ContentFileInfo/getLyricURL?subitemtype=LRC-LRC&itemid=1111
        """
        super(ShareMusicAsyncLyric, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'ContentFileInfo/getLyricURL'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}
