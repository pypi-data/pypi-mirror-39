#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/3 上午10:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : mysql
# @File    : app_music
# @Contact : guangze.yu@foxmail.com
"""

# SQL DateBase config
sql = 'mysql'
tools = 'pymysql'
usr = 'root'
password = 'Root1q2w'
host = 'rm-uf6lp85qe22m65cu6oo.mysql.rds.aliyuncs.com:3306'
db_name = 'db_music'
sqlconfig = '%s+%s://%s:%s@%s/%s?charset=utf8' % (sql, tools, usr, password,
                                                  host, db_name)