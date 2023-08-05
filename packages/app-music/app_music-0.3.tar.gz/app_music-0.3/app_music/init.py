#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""@init
用于生成推荐列表，包括荣威推荐与每日推荐。
推荐列表生成后放入缓存中，以方便后续快速调用。
"""
import app.musicAI.musicAIAPI as rec
import redis
import json
import database.operation as operation
import database.definition as definition

Connection = definition.Connect()
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Root1q2w')
cache = redis.Redis(connection_pool=pool)

def getvin():
    """getvin
    获取历史记录内所有vin码
    :return: vin list
    """
    vin = []
    b = operation.UserHistoryBase(Connection)
    d = b.getvin()
    g = d.cursor._rows
    h = len(g)
    i = 0
    while i < h:
        vin.append(g[i][0])
        i = i + 1
    return vin

def getuid():
    """getuid
    获取历史记录内所有uid
    :return: uid list
    """
    uid = []
    b = operation.UserHistoryBase(Connection)
    d = b.getuid()
    g = d.cursor._rows
    h = len(g)
    i = 0
    while i < h:
        uid.append(g[i][0])
        i = i + 1
    return uid

def dailyrec():
    """dailyrec
    每日推荐
    :return: None
    """
    res = rec.dailysonglist()
    res2 = json.dumps(res)
    
    cache.set('dailyrec', res2)

def roewerec():
    """roewerec
    荣威推荐
    :return:
    """
    vinlist = getvin()
    uidlist = getuid()
    for vin in vinlist:
        uid = None
        a = rec.roewerecommend(vin, uid=None)
        b = json.dumps(a)
        cache.hset(uid, vin, b)
        print('vin=%s,uid=%s' % (vin, uid))
        print(b)
    for uid in uidlist:
        vin = 'XXXXXXXXXXXXXX'
        c = rec.roewerecommend(vin, uid=uid)
        d = json.dumps(c)
        print('vin=%s,uid=%s' % (vin, uid))
        print(d)
        cache.hset(uid, vin, d)
    e = rec.roewerecommend(vin=None, uid=None)
    f = json.dumps(e)
    cache.hset('uid=None', 'vin=None', f)

def update():
    dailyrec()
    roewerec()

