#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/9 11:13
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : result
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""
import utils.exception as exception


class ResultBase(object):
    def __init__(self):
        self._status_code = None
        self._status_info = None
        self._response = None
        self._message = None

    @property
    def status_code(self):
        return self._status_code

    @property
    def status_info(self):
        return self._status_info

    @property
    def response(self):
        return self._response

    @property
    def message(self):
        if self._message is None:
            return self._message
        else:
            return self._message.message


class TestResult(ResultBase):
    def __init__(self, res, message=None):
        super(TestResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class ErrorResult(ResultBase):
    def __init__(self, error, message=None):
        super(ErrorResult, self).__init__()
        self._status_code = error.code
        self._status_info = error.info
        self._response = self._status_info
        self._message = message


class SearchResult(ResultBase):
    def __init__(self, res, message=None):
        super(SearchResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class CollectResult(ResultBase):
    def __init__(self, res, message=None):
        super(CollectResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class PlayResult(ResultBase):
    def __init__(self, res, message=None):
        super(PlayResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class PlayHistoryResult(ResultBase):
    def __init__(self, res, message=None):
        super(PlayHistoryResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class MoreInfoResult(ResultBase):
    def __init__(self, res, message=None):
        super(MoreInfoResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class PlayListResult(ResultBase):
    def __init__(self, res, message=None):
        super(PlayListResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message


class RecommandResult(ResultBase):
    def __init__(self, res, message=None):
        super(RecommandResult, self).__init__()
        self._status_code = exception.Success().code
        self._status_info = exception.Success().info
        self._response = res
        self._message = message
