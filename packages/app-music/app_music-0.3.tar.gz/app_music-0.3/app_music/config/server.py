#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/4 下午1:17
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : app_main
# @File    : app_music
# @Contact : guangze.yu@foxmail.com
"""

from urllib.request import urlopen
from json import load


IP = load(urlopen('http://ip-api.com/json'))['query']
PORT = 8887