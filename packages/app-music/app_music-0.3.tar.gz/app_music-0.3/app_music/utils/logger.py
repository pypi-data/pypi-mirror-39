#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-26 下午10:26
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : logger
# @Contact : guangze.yu@foxmail.com
"""

import sys
import logging
import logging.handlers as handlers


def get_logger(log_name):
    logger = logging.getLogger(log_name)
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d]'
                                  ' %(levelname)s %(message)s')
    file_handler = handlers.RotatingFileHandler("./log/%s.log" % log_name,
                                                maxBytes=10*1024*1024,
                                                backupCount=10)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
