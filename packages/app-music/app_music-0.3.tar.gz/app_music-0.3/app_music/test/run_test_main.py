#! usr/bin/env python
# coding = utf-8

"""
    生成单元测试报告
"""
import time

import unittest
#   https://github.com/huilansame/HTMLTestRunner_PY3
from test.HTMLTestRunner_Py3 import HTMLTestRunner

TEST_DIR = './app_test_gateway/'
# TEST_DIR = './app_test_main/'

#   discover 是一个自动化的过程，将目标路径下，自动匹配test*.py文件作为测试用例
DISCOVER = unittest.defaultTestLoader.discover(TEST_DIR, pattern='test*.py')

if __name__ == '__main__':

    NOW = time.strftime("%Y-%m-%d %H_%M_%S")
    if 'Gateway' in TEST_DIR:
        FILENAME = './report/' + '[Gateway]_' + NOW + '_result.html'
        FP = open(FILENAME, 'wb')
        #   HTMLTestRunner 生成实例
        RUNNER = HTMLTestRunner(stream=FP,
                                title='后排辅助者(app_music)[网关]测试报告',
                                description='用例执行情况：')
    else:
        FILENAME = './report/' + '[NotGateway]_' + NOW + '_result.html'
        FP = open(FILENAME, 'wb')
        #   HTMLTestRunner 生成实例
        RUNNER = HTMLTestRunner(stream=FP,
                                title='后排辅助者(app_music)[非网关]测试报告',
                                description='用例执行情况：')

    RUNNER.run(DISCOVER)
