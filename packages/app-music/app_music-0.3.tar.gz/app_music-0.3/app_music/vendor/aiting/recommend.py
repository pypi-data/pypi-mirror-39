#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 10:37
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : recommend
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""

import requests
from vendor.aiting.common import Common


# 15.1.1
class CreateRadioByName(Common):
    def __init__(self, param_dict):
        """
        * @brief 首先注册
        https://csapi.tingmall.com/ContentServiceWS/Recommend/
        gnRegisterUser?memberid=0176E1A670D141205569BB40AF7AEF08
        然后创建
        https://csapi.tingmall.com/ContentServiceWS/Recommend/
        gnCreateRadio?length=25
        &artists=%E5%91%A8%E6%9D%B0%E4%BC%A6%2C%E5%BC%A0%E5%AD%A6%E5%8F%8B
        &memberid=0176E1A670D141205569BB40AF7AEF08
        :param param_dict:
        length:
        artists:
        tracks:
        """
        super(CreateRadioByName, self).__init__(param_dict)
        registUrl = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'Recommend/gnRegisterUser'
        res = requests.post(registUrl, params=self._http_body,
                            headers=self._headers).content.decode('utf-8')
        print(res)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'Recommend/gnCreateRadio'


class CreateRadioById(CreateRadioByName):
    def __init__(self, param_dict):
        """
        * @brief 首先注册
        https://csapi.tingmall.com/ContentServiceWS/Recommend/
        gnRegisterUser?memberid=5BEE31363BEF0699
        然后创建
        https://csapi.tingmall.com/ContentServiceWS/Recommend/
        gnCreateRadio?length=25
        &artists=%E5%91%A8%E6%9D%B0%E4%BC%A6%2C%E5%BC%A0%E5%AD%A6%E5%8F%8B
        &memberid=5BEE31363BEF0699
        * @param std::string artists 歌手名称(多个名称逗号分隔)
        * @param std::string trackIds 歌曲ID(多个名称逗号分隔)
        :param param_dict:
        """
        super(CreateRadioById, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'Recommend/gnCreateRadio'


class TuningRadio(Common):
    def __init__(self, param_dict):
        """
        * @name 15.3.1 gnTuningRadioSync 同步调节个性化歌单的匹配度
        * @brief https://csapi.tingmall.com/ContentServiceWS/Recommend/
        gnTuningRadio?popularity=500&playlistid=302272&similarity=300
        &memberid=0176E1A670D141205569BB40AF7AEF08
        popularity: 流行性 0-1000,值越大匹配度越高
        similarity: 相似性 0-1000,值越大匹配度越高
        playlistid:
        """
        super(TuningRadio, self).__init__(param_dict)
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'Recommend/gnTuningRadio'
