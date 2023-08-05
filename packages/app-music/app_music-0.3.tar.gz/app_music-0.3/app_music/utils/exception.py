#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/9 11:07
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : expection
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""
BASE_CODE = 30000


class Common(Exception):
    _status_code = 200
    _status_info = 'Success.'

    @property
    def code(self):
        return self._status_code

    @property
    def info(self):
        return self._status_info

    def __str__(self):
        return repr(self._status_info)


class Success(Common):
    _status_code = 0
    _status_info = 'Success.'


class InternalError(Common):
    _status_code = BASE_CODE + 500
    _status_info = 'Internal fault.'


class GetTokenFailed(Common):
    _status_code = BASE_CODE + 501
    _status_info = 'Get token failed from vendor.'


class NoTimeStampError(Common):
    _status_code = BASE_CODE + 1001
    _status_info = 'No timestamp in the request params!'


class NoVinError(Common):
    _status_code = BASE_CODE + 1002
    _status_info = 'No vin in the request params!'


class NoKeyWordError(Common):
    _status_code = BASE_CODE + 1003
    _status_info = 'No keyword in the request params!'


class PikaConnectionError(Common):
    _status_code = BASE_CODE + 1004
    _status_info = 'RabbitMQ connected error!'


class NoTrackIdError(Common):
    _status_code = BASE_CODE + 1005
    _status_info = 'No track id in the request params!'


class NoPlayListIdError(Common):
    _status_code = BASE_CODE + 1006
    _status_info = 'No playlist id in the request params!'


class NoAlbumIdError(Common):
    _status_code = BASE_CODE + 1007
    _status_info = 'No album id in the request params!'


class WebHandlerError(Common):
    _status_code = BASE_CODE + 1008
    _status_info = 'Error in the handler!'


class SQLConnectError(Common):
    _status_code = BASE_CODE + 1009
    _status_info = 'Database connect error!'


class CacheConnectError(Common):
    _status_code = BASE_CODE + 1010
    _status_info = 'Cache connect error!'


class NoItemIdError(Common):
    _status_code = BASE_CODE + 1011
    _status_info = 'No item id in the request params!'


class NoPlayListNameError(Common):
    _status_code = BASE_CODE + 1012
    _status_info = 'No playlistname in the request params!'


class NoSelfListError(Common):
    _status_code = BASE_CODE + 1013
    _status_info = 'No selflist in the request params!'


class NoArtistIdError(Common):
    _status_code = BASE_CODE + 1014
    _status_info = 'No artist id in the request params!'


class NoCategoryIdIdError(Common):
    _status_code = BASE_CODE + 1015
    _status_info = 'No categoryid id in the request params!'


class NoUserIdIdError(Common):
    _status_code = BASE_CODE + 1016
    _status_info = 'No user id in the request params!'


class AitingServerError(Common):
    _status_code = BASE_CODE + 1017
    _status_info = 'Aiting Server Error!'


class NoListTypeError(Common):
    _status_code = BASE_CODE + 1018
    _status_info = 'No type in the request params!'


class UnSupportTypeError(Common):
    _status_code = BASE_CODE + 1019
    _status_info = 'UnSupport type in the request params!'


class ExceedCollectLimitError(Common):
    _status_code = BASE_CODE + 1020
    _status_info = 'Exceed the limit! Limitation is 500.'
