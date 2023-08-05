#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : test
# @Contact : guangze.yu@foxmail.com
"""
import time
import utils.logger as logger
import utils.result as result
import database.operation as database
import database.definition as base

LOG = logger.get_logger(__name__)


def sleepout(params):
    """

    :param params:
    :return:
    """
    print(params)
    LOG.info('Params:%s', params)
    time.sleep(1)
    return result.TestResult(res='Hello!')


def sqltest(params):
    """

    :param params:
    :return: 
    """
    LOG.info('test service')
    LOG.info('params is %s', params)
    conn = base.Connect()
    data = database.SongHistoryList(vin='LSJA1234567890100', conn=conn)
    out = data.stat()
    conn.close()
    return result.TestResult(res=out)
