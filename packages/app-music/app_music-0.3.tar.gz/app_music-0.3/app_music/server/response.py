#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""response
用于处理服务响应，将结果封装为特定格式进行输出。
"""

class Response(object):
    def __init__(self, app_result, request_path, method):
        """

        :param app_result: utils.result.Result class. 服务返回结果。
        :param request_path: str, 请求路径
        :param method: str, 'POST' or 'get', 请求方法.
        """
        self._result = app_result
        self._path = request_path
        self._method = method

    @property
    def info(self):
        """

        :return: dict, 响应结果字典。
        """
        res_info = {'data': self._result.response}
        return res_info

    def __repr__(self):
        return self.info
