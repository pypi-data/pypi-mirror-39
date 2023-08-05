#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/27 9:08
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : common
# @Project : app_music
# @Contact : guangze.yu@foxmail.com
"""

import requests
import json
from config.vendor import local_token_url, local_token_params, remote_token_url
from utils.exception import GetTokenFailed


class Oauth:
    def __init__(self):
        self._url = local_token_url
        res = json.loads(requests.get(self._url).content.decode('utf-8'))
        error_code = 0
        if error_code == 0:
            self.token = res['token_info']['token']
            # self.token = res['response']['docs']['access_token']
            print(self.token)
            self.memberid = res['token_info']['memberid']
            # self.memberid = '1F260D9130C6E4C8'
        else:
            raise GetTokenFailed


def get_token():
    token_info = Oauth()
    token = token_info.token
    memberid = token_info.memberid
    return token, memberid


class Common(object):
    def __init__(self, param_dict):
        token, memberid = get_token()
        self._access_token = token
        self._headers = {'oauth_token': self._access_token}
        self._http_body = param_dict
        self._http_body['memberid'] = memberid
        self._url = 'https://csapi.tingmall.com/ContentServiceWS/' \
                    'CategoryExInfo/getCategoryAlbum'

    def get(self):
        try:
            res = json.loads(
                requests.post(url=self._url, params=self._http_body,
                              headers=self._headers).content.decode('utf-8'))
            return res
        except:
            return "Aiting server stopped."
