#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-22 下午2:32
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : cache
# @Contact : guangze.yu@foxmail.com
"""

import database.operation as db
import redis
import json
import traceback
import datetime

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password='Root1q2w')
cache = redis.Redis(connection_pool=pool)


class Common(object):
    def __init__(self, vin, uid=None, conn=cache):
        self._vin = vin
        self._uid = uid
        self._conn = conn


class SearchWordHistory(Common):
    def __init__(self, vin, uid=None, conn=cache):
        super(SearchWordHistory, self).__init__(vin, uid, conn)

    def get(self):
        try:
            if self._uid is None:
                out = cache.hget(self._uid, 'SearchWordHistory')
            else:
                out = cache.hget(self._vin, 'SearchWordHistory')
            if out is None:
                dbout = db.SearchWordHistory(self._vin, self._uid)
                if dbout is None:
                    dbout = []
                cache.hset(self._uid, 'SearchWordHistory', json.dumps(dbout))
                info = dbout
            else:
                info = json.loads(out)
            return info
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def clear(self):
        try:
            if self._uid is None:
                info = cache.hget(self._vin, 'SearchWordHistory')
            else:
                info = cache.hget(self._uid, 'SearchWordHistory')
            if info is None or info == []:
                return True
            else:
                cache.hset(self._uid, 'SearchWordHistory', json.dumps([]))
                db.SearchWordHistory(self._vin, self._uid).clear()
                return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, keyword):
        try:
            db.SearchWordHistory(self._vin, self._uid).add(timestamp, keyword)
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            cacheinfo = cache.hget(uid, 'SearchWordHistory')
            if cacheinfo is None:
                cache.hset(uid, 'SearchWordHistory',
                           json.dumps([{'keyword': keyword}]))
                return True
            else:
                info = json.loads(cacheinfo)
                keywords = [i['keyword'] for i in info]
                try:
                    index = keywords.index(keyword)
                    info.__delitem__(index)
                    info.append({'keyword': keyword})
                    cache.hset(uid, 'SearchWordHistory', json.dumps(info))
                except:
                    info.append({'keyword': keyword})
                    cache.hset(uid, 'SearchWordHistory', json.dumps(info))
                return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class SongHistoryList(Common):
    def __init__(self, vin, uid=None, conn=cache):
        super(SongHistoryList, self).__init__(vin, uid, conn)

    def get(self, starttime=datetime.datetime.now()-datetime.timedelta(180),
            endtime=datetime.datetime.now()):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'SongHistoryList')
            if out is None:
                dbout = db.SongHistoryList(self._vin, self._uid)\
                    .get(starttime, endtime)
                if dbout is None or dbout == []:
                    dbout = []
                info = dbout
                cache.hset(uid, 'SongHistoryList', json.dumps(dbout))
                return info
            else:
                info = json.loads(out)
                return info
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, itemid):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            db.SongHistoryList(self._vin, self._uid).add(timestamp, itemid)
            info = db.SongHistoryList(self._vin, self._uid).get()
            cache.hset(uid, 'SongHistoryList', json.dumps(info))
            statinfo = db.SongHistoryList(self._vin, self._uid).stat()
            cache.hset(uid, 'SongHistoryListStat', json.dumps(statinfo))
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def stat(self,
             n=50,
             starttime=datetime.datetime.now()-datetime.timedelta(180),
             endtime=datetime.datetime.now()):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'SongHistoryListStat')
            if out is None:
                info = db.SongHistoryList(self._vin, self._uid)\
                    .stat(n, starttime, endtime)
                cache.hset(uid, 'SongHistoryListStat', json.dumps(info))
                return info
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectSong(Common):
    def __init__(self, vin, uid=None, conn=cache):
        super(CollectSong, self).__init__(vin, uid, conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'CollectSong')
            if out is None:
                dbout = db.CollectSong(self._vin, self._uid).get()
                cache.hset(uid, 'CollectSong', json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, itemid):
        try:
            db.CollectSong(self._vin, self._uid).add(timestamp, itemid)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self, timestamp, itemid):
        try:
            db.CollectSong(self._vin, self._uid).cancel(timestamp, itemid)
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class CollectPlayList(Common):
    def __init__(self, vin, uid=None, conn=cache):
        super(CollectPlayList, self).__init__(vin, uid, conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'CollectPlayList')
            if out is None:
                dbout = db.CollectPlayList(self._vin, self._uid).get()
                cache.hset(uid, 'CollectPlayList', json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def add(self, timestamp, playlistid, selflist=False):
        try:
            db.CollectPlayList(self._vin, self._uid)\
                .add(timestamp, playlistid, selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False

    def cancel(self, timestamp, playlistid, selflist=False):
        try:
            db.CollectPlayList(self._vin, self._uid)\
                .cancel(timestamp, playlistid, selflist)
            return True
        except:
            traceback.print_exc()
            print('cache failre')
            return False


class UserPlaylist(Common):
    def __init__(self, vin, uid=None, Conn=cache):
        super(UserPlaylist, self).__init__(vin, uid, Conn)

    def get(self):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'UserPlaylist')
            if out is None:
                dbout = db.UserPlaylist(self._vin, self._uid).get()
                cache.hset(uid, 'UserPlaylist', json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            return False

    def create(self, playlistname):
        try:
            db.UserPlaylist(self._vin, self._uid).create(playlistname)
            return True
        except:
            traceback.print_exc()
            return False

    def add(self, timestamp, playlistid, itemid):
        try:
            db.UserPlaylist(self._vin, self._uid)\
                .add(timestamp, playlistid, itemid)
            return True
        except:
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, playlistid, itemid):
        try:
            db.UserPlaylist(self._vin, self._uid)\
                .cancel(timestamp, playlistid, itemid)
            return True
        except:
            traceback.print_exc()
            print('cancel failre')
            return False

    def getplaylistcontent(self, playlistid):
        try:
            if self._uid is None:
                uid = self._vin
            else:
                uid = self._uid
            out = cache.hget(uid, 'UserPlaylistContent')
            if out is None:
                dbout = db.UserPlaylist(self._vin, self._uid).getplaylistcontent(playlistid)
                cache.hset(uid, 'UserPlaylistContent', json.dumps(dbout))
                return dbout
            else:
                return json.loads(out)
        except:
            traceback.print_exc()
            print('getplaylistcontent failre')
            return False
