#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""

"""

import time
import utils.result as result
import utils.exception as exception


def params_check(func):
    """params_check
    用于检查输入参数的装饰器，若参数缺少vin码将抛出异常，
    若参数缺少uid，将把uid设置为None。
    目前，参数中的时间戳将自动替换为服务器本地时间戳，后续若对时间戳进行校验也可在此完成。

    """
    def wrapper(params):
        if 'vin' not in params:
            return result.ErrorResult(exception.NoVinError())
        if 'timestamp' not in params:
            return result.ErrorResult(exception.NoTimeStampError())
        params['timestamp'] = time.time()
        if 'uid' not in params:
            params['uid'] = None
        else:
            if not params['uid']:
                params['uid'] = None
            else:
                params['uid'] = int(params['uid'])
        return func(params)
    return wrapper
