#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/3 上午10:58
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : vendor
# @File    : app_music
# @Contact : guangze.yu@foxmail.com
"""

# aiting API config
import pymysql

conn = pymysql
db = pymysql.connect(host="rm-uf6lp85qe22m65cu6oo.mysql.rds.aliyuncs.com",
                     user="root",
                     password="Root1q2w",
                     db="db_music",
                     port=3306)
cur = db.cursor()
query = "select * from serverhost;"
cur.execute(query)
results = cur.fetchall()[0]

# API token config

oauth_consumer_key = 'SHMusicClient'
oauth_consumer_sig = 'EEEA591FB2F1422DE3C3AEAC95791BD2'
clientid = 'LinuxClient'
clientsecret = 'ZC001'

# local_token_url = 'https://csapi.tingmall.com/ContentServiceWS/OAuth/getAccessTokenSig?/'
local_token_url = 'http://localhost:8000/gettoken'
local_token_params = {"oauth_consumer_key": oauth_consumer_key, "oauth_consumer_sig": oauth_consumer_sig,
                      "clientid": clientid, "clientsecret": clientsecret}

remote_token_url = '%s/gettoken' % results[0]
