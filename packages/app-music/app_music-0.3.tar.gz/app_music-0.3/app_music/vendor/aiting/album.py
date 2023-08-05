#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 9:52
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : album
# @Project : app_music 
# @Contact : guangze.yu@foxmail.com
"""
from vendor.aiting.common import Common


# 4.1.1 请求专辑列表
class GetAlbumListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Hotest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Hotest
        """
        super(GetAlbumListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'


# 4.1.2 请求专辑列表
class GetAlbumListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Hotest
        example:  https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Hotest
        """
        super(GetAlbumListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'


# 4.2.1 请求专辑内容
class GetAlbumAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        albumid=98920
        example:   https://csapi.tingmall.com/ContentServiceWS/
        AlbumInfo/getAlbumInfo?albumid=98920
        """
        super(GetAlbumAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AlbumInfo/getAlbumInfo'


# 4.2.2 请求专辑内容
class GetAlbumSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        albumid=98920
        example:   https://csapi.tingmall.com/ContentServiceWS/
        AlbumInfo/getAlbumInfo?albumid=98920
        """
        super(GetAlbumSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'AlbumInfo/getAlbumInfo'


# 4.3.1 请求新碟上架的专辑列表
class GetNewAlbumListAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Newest
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Newest
        """
        super(GetNewAlbumListAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'


# 4.3.2 请求新碟上架的专辑列表
class GetNewAlbumListSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Newest
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Newest
        """
        super(GetNewAlbumListSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'


# 4.4.1 请求专辑的分类列表
class GetAlbumCategoryAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Group_Album
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100
        &offset=0&categorycode=SS_Group_Album
        """
        super(GetAlbumCategoryAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 4.4.2 请求专辑的分类列表
class GetAlbumCategorySync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Group_Album
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryMenu?length=100&offset=0
        &categorycode=SS_Group_Album
        """
        super(GetAlbumCategorySync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryMenu'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 4.5.1 请求分类的专辑单列表
class GetAlbumNodelistAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Genre_AB_Recom
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryNodelist?length=100&offset=0
        &categorycode=SS_Genre_AB_Recom
        """
        super(GetAlbumNodelistAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryNodelist'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 4.5.2 请求分类的专辑单列表
class GetAlbumNodelistSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=100
        offset=0
        categorycode=SS_Genre_AB_Recom
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryNodelist?length=100&offset=0
        &categorycode=SS_Genre_AB_Recom
        """
        super(GetAlbumNodelistSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryNodelist'
# {'responseHeader': {'errorinfo': 'Result Not Found.', 'status': '101'}}


# 4.6.1 请求专辑单的专辑列表
class GetAlbumListAlbumAsync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Hotest
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Hotest
        """
        super(GetAlbumListAlbumAsync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'


# 4.6.2 请求专辑单的专辑列表
class GetAlbumListAlbumSync(Common):
    def __init__(self, param_dict):
        """Search music
        :param  a dict, contain searchvalue, rows, start
        length=20
        offset=0
        categorycode=NL_Album_Hotest
        example:   https://csapi.tingmall.com/ContentServiceWS/
        CategoryExInfo/getCategoryAlbum?length=20&offset=0
        &categorycode=NL_Album_Hotest
        """
        super(GetAlbumListAlbumSync, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'
