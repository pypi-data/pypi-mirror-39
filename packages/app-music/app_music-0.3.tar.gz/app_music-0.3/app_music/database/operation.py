#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午8:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : data_base
# @Contact : guangze.yu@foxmail.com
"""

import database.definition as base
import datetime
import traceback
from sqlalchemy import desc
from utils.exception import SQLConnectError
import vendor.aiting.music as music
import vendor.aiting.playlist as playlistapi
import vendor.aiting.album as albumapi


CONN = base.Connect()


class Common(object):
    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        self._vin = vin
        self._uid = uid
        self._conn = conn


class SearchWordHistory(Common):

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(180)

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        super(SearchWordHistory, self).__init__(vin, uid, conn)

    def get(self,
            starttime=start_time,
            endtime=end_time, n=10):
        """

        :param starttime:
        :param endtime:
        :return:
        """
        try:
            if self._uid is None:
                query = "SELECT tb_searchword_history.keyword, " \
                        "group_concat(tb_searchword_history.time ORDER by " \
                        "tb_searchword_history.time DESC) from " \
                        "tb_searchword_history where " \
                        "tb_searchword_history.showinlist=1 " \
                        "and tb_searchword_history.time " \
                        "BETWEEN '%s'and'%s' and tb_searchword_history.uid " \
                        "is NULL AND tb_searchword_history.vin='%s' " \
                        "group by tb_searchword_history.keyword ORDER BY " \
                        "group_concat(tb_searchword_history.time " \
                        "ORDER by tb_searchword_history.time DESC) DESC " \
                        "LIMIT %s;"\
                        % (starttime, endtime, self._vin, n)
            else:
                query = "select tb_searchword_history.keyword, " \
                        "group_concat(tb_searchword_history.time ORDER by " \
                        "tb_searchword_history.time DESC) " \
                        "from tb_searchword_history where " \
                        "tb_searchword_history.showinlist=1 " \
                        "and tb_searchword_history.time BETWEEN " \
                        "'%s'and'%s' and tb_searchword_history.uid='%s' " \
                        "group by tb_searchword_history.keyword ORDER BY " \
                        "group_concat(tb_searchword_history.time " \
                        "ORDER by tb_searchword_history.time DESC) DESC " \
                        "LIMIT %s;"\
                        % (starttime, endtime, self._uid, n)
            print(query)
            data = self._conn.session.execute(query)
            out = [{'keyword': i[0]} for i in data]
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('get failre')
            return False

    def clear(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserSearchKeyWordHistory)
            data = query.filter_by(vin=self._vin,
                                   uid=self._uid,
                                   showinlist=True).all()
            for i in data:
                i.showinlist = False
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('clear failre')
            return False

    def add(self, timestamp, keyword):
        """

        :param timestamp:
        :param keyword:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            data = {'uid': self._uid,
                    'vin': self._vin,
                    'time': time_array,
                    'keyword': keyword,
                    'showinlist': True}
            add_item = (base.UserSearchKeyWordHistory(**data))
            self._conn.session.add(add_item)
            self._conn.commit()
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('add failre')
            return False


class SongHistoryList(Common):

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(180)

    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:db_music@rm-uf6lp85qe22m65cu6oo.mysql.rds.aliyuncs.com
        :param uid:
        :param conn:
        """
        super(SongHistoryList, self).__init__(vin, uid, conn)

    def get(self, starttime, endtime, n=100):
        """

        :param starttime:
        :param endtime:
        :return:
        """
        try:
            if self._uid is None:
                query = "SELECT tb_song_history.itemid, " \
                        "tb_song_history.translatename, " \
                        "tb_song_history.artistname, " \
                        "tb_user_collect_song.favorite, " \
                        "group_concat(tb_song_history.time " \
                        "ORDER by tb_song_history.time DESC) from " \
                        "tb_song_history LEFT JOIN tb_user_collect_song " \
                        "on tb_song_history.itemid=tb_user_collect_song.itemid" \
                        " where tb_song_history.time BETWEEN '%s'and'%s' and " \
                        "tb_song_history.valid=1 AND " \
                        "tb_song_history.uid is NULL AND " \
                        "tb_song_history.vin='%s' group by " \
                        "tb_song_history.itemid ORDER BY " \
                        "group_concat(tb_song_history.time " \
                        "ORDER by tb_song_history.time DESC) DESC LIMIT %s;"\
                        % (starttime, endtime, self._vin, n)
            else:
                query = "select tb_song_history.itemid, " \
                        "tb_song_history.translatename," \
                        "tb_song_history.artistname, " \
                        "tb_user_collect_song.favorite, " \
                        "group_concat(tb_song_history.time " \
                        "ORDER by tb_song_history.time DESC) " \
                        "from tb_song_history LEFT JOIN tb_user_collect_song " \
                        "on tb_song_history.itemid=tb_user_collect_song.itemid" \
                        " where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid='%s' " \
                        "AND tb_song_history.valid=1 " \
                        "group by tb_song_history.itemid ORDER BY " \
                        "group_concat(tb_song_history.time " \
                        "ORDER by tb_song_history.time DESC) DESC LIMIT %s;"\
                        % (starttime, endtime, self._uid, n)
            print(query)
            data = self._conn.session.execute(query)
            out = [{'songId': i[0],
                    'title': i[1],
                    'artistName': i[2],
                    'isLiked': i[3] if i[3] else 0} for i in data]
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('get failre')
            return False

    def add(self, timestamp, itemid):
        """

        :param timestamp:
        :param itemid:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            song = self._conn.session.query(base.Song)\
                .filter_by(itemid=itemid).first()

            if song is None:
                s = {'itemid': itemid}
                songdata = music.GetMusicSync(s).get()['response']['docs'][0]
                translatename = songdata['datainfo']['translatename']
                artistid = songdata['artists'][0]['artistID']
                artistname = ''.join([i['name'] + ',' for i in songdata['artists']])
                albumid = songdata['album']['albumID']
                genre = songdata['datainfo']['genre']
                rating = songdata['datainfo']['rating']
                contentproviderid = \
                    songdata['album']['cpInfo'][0]['contentProviderID']
                image_small = songdata['album']['imagePathMap'][3]['value']
                image_middle = songdata['album']['imagePathMap'][4]['value']
                image_large = songdata['album']['imagePathMap'][2]['value']
                addsong = {'itemid': itemid,
                           'translatename': translatename,
                           'artistid': artistid,
                           'artistname': artistname,
                           'albumid': albumid,
                           'contentproviderid': contentproviderid,
                           'genre': genre,
                           'rating': rating,
                           'imagepathmapSmall': image_small,
                           'imagepathmapMiddle': image_middle,
                           'imagepathmapLarge': image_large}
                newsong = base.Song(**addsong)
                self._conn.session.add(newsong)
            else:
                translatename = song.translatename
                artistname = song.artistname
                artistid = song.artistid
                albumid = song.albumid
                genre = song.genre
                rating = song.rating

            data = {'uid': self._uid,
                    'vin': self._vin,
                    'time': time_array,
                    'itemid': itemid,
                    'translatename': translatename,
                    'artistid': artistid,
                    'artistname': artistname,
                    'albumid': albumid,
                    'genre': genre,
                    'rating': rating}
            add_item = (base.UserSongHistoryList(**data))
            self._conn.session.add(add_item)
            self._conn.commit()
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('add failre')
            return False

    def stat(self,
             starttime=start_time,
             endtime=end_time):
        """

        :param starttime:
        :param endtime:
        :return:
        """
        try:
            if self._uid is None:
                query = "SELECT tb_song_history.itemid," \
                        "count(tb_song_history.itemid)," \
                        "tb_song_history.translatename," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid " \
                        "is NULL AND tb_song_history.vin='%s' " \
                        "group by tb_song_history.itemid ORDER BY " \
                        "count(itemid) DESC;" % (starttime, endtime, self._vin)
            else:
                query = "SELECT tb_song_history.itemid," \
                        "count(tb_song_history.itemid)," \
                        "tb_song_history.translatename," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid=%s " \
                        "group by tb_song_history.itemid ORDER BY " \
                        "count(itemid) DESC;" % (starttime, endtime, self._uid)
            song_data = self._conn.session.execute(query)
            if song_data:
                song_out = [{'itemid': i[0],
                             'playnum': i[1],
                             'translatename': i[2],
                             'playtime': i[3]} for i in song_data]
            else:
                song_out = None

            if self._uid is None:
                query = "SELECT tb_song_history.albumid," \
                        "count(tb_song_history.albumid)," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid " \
                        "is NULL AND tb_song_history.vin='%s' " \
                        "group by tb_song_history.albumid ORDER BY " \
                        "count(albumid) DESC;" % (starttime, endtime, self._vin)
            else:
                query = "SELECT " \
                        "tb_song_history.albumid,count(tb_song_history.albumid)," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid=%s " \
                        "group by tb_song_history.albumid ORDER BY " \
                        "count(albumid) DESC;" % (starttime, endtime, self._uid)
            album_data = self._conn.session.execute(query)
            if album_data:
                album_out = [{'albumid': i[0],
                              'playnum': i[1],
                              'playtime': i[2]} for i in album_data]
            else:
                album_out = None
            if self._uid is None:
                query = "SELECT tb_song_history.artistid," \
                        "count(tb_song_history.artistid), " \
                        "tb_song_history.artistname," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid " \
                        "is NULL AND tb_song_history.vin='%s' " \
                        "group by tb_song_history.artistid ORDER BY " \
                        "count(artistid) DESC;" % (starttime, endtime, self._vin)
            else:
                query = "SELECT tb_song_history.artistid," \
                        "count(tb_song_history.artistid), " \
                        "tb_song_history.artistname," \
                        "group_concat(time ORDER by time DESC) " \
                        "from tb_song_history where tb_song_history.time " \
                        "BETWEEN '%s'and'%s' and tb_song_history.uid=%s " \
                        "group by tb_song_history.artistid ORDER BY " \
                        "count(artistid) DESC;" % (starttime, endtime, self._uid)

            artist_data = self._conn.session.execute(query)
            if artist_data:
                artist_out = [{'artistid': i[0],
                               'artistname': i[2],
                               'playnum': i[1],
                               'playtime': i[3]} for i in artist_data]
            else:
                artist_out = None

            out = {'song': song_out, 'album': album_out, 'artist': artist_out}
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('cancel failre')
            return False

    def clear(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserSongHistoryList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       valid=True).all()
                for i in data:
                    i.valid = False
            else:
                data = query.filter_by(uid=self._uid,
                                       valid=True).all()
                for i in data:
                    i.valid = False
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('clear failre')
            return False



class CollectSong(Common):
    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        super(CollectSong, self).__init__(vin, uid, conn)

    def get(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserCollectSong)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).order_by(desc(base.UserCollectSong.time)).limit(500)
            else:
                data = query.filter_by(uid=self._uid, favorite=True).order_by(desc(base.UserCollectSong.time)).limit(500)
            if data:
                out = [{'songId': i.itemid,
                        'title': i.translatename,
                        'artistName': i.artistname} for i in data]
            else:
                out = []
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('cancel failre')
            return False

    def add(self, timestamp, itemid):
        """

        :param timestamp:
        :param itemid:
        :return:
        """
        if self._uid is None:
            collect_num = self._conn.session.query(base.UserCollectSong)\
                .filter_by(uid=self._uid,
                           vin=self._vin,
                           favorite=True).count()
        else:
            collect_num = self._conn.session.query(base.UserCollectSong)\
                .filter_by(uid=self._uid,
                           favorite=True).count()
        if collect_num > 500:
            return "Spilled"

        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectSong)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               itemid=itemid).first()
            else:
                collect = self._conn.session.query(base.UserCollectSong)\
                    .filter_by(uid=self._uid,
                               itemid=itemid).first()
            if collect is None:
                song = self._conn.session.query(base.Song)\
                    .filter_by(itemid=itemid).first()
                if song is None:
                    s = {'itemid': itemid}
                    songdata = music.GetMusicSync(s).get()['response']['docs'][0]
                    translatename = songdata['datainfo']['translatename']
                    artistname = ''.join(
                        [i['name'] + ',' for i in songdata['artists']])[:-1]
                else:
                    translatename = song.translatename
                    artistname = song.artistname
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'itemid': itemid,
                        'translatename': translatename,
                        'artistname': artistname,
                        'favorite': True,
                        'time': time_array}
                add_item = (base.UserCollectSong(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            return "Success"
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            return "Failure"

    def cancel(self, timestamp, itemid):
        """

        :param timestamp:
        :param itemid:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectSong)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               itemid=itemid).first()
            else:
                collect = self._conn.session.query(base.UserCollectSong)\
                    .filter_by(uid=self._uid, itemid=itemid).first()
            if collect is None:
                return "No song collected in the database."
            else:
                collect.favorite = False
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            return False


class CollectPlayList(Common):
    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        super(CollectPlayList, self).__init__(vin, uid, conn)

    def get(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserCollectPlayList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin,
                                       uid=self._uid,
                                       favorite=True).order_by(desc(base.UserCollectPlayList.time)).limit(500)
            else:
                data = query.filter_by(uid=self._uid, favorite=True).order_by(desc(base.UserCollectPlayList.time)).limit(500)
            print(data)
            if data:
                """type: 1,自建歌单 2,album 3,playlist(songset)"""
                out = [{'playlistid': i.playlistid,
                        'playlistname': i.playlistname,
                        'imageS': i.imagepathmapSmall,
                        'imageM': i.imagepathmapMiddle,
                        'imageL': i.imagepathmapLarge,
                        'type': i.type} for i in data]
            else:
                out = []
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            return False

    def add(self, timestamp, playlistid, listtype):
        """

        :param timestamp:
        :param playlistid:
        :param selflist:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               playlistid=playlistid,
                               type=listtype).first()
            else:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               playlistid=playlistid,
                               type=listtype).first()
            if collect is None:
                if listtype == 1:
                    if self._uid is None:
                        playlist = self._conn.session.query(base.UserPlayList)\
                            .filter_by(uid=self._uid,
                                       vin=self._vin,
                                       playlistid=playlistid).first()
                    else:
                        playlist = self._conn.session.query(base.UserPlayList)\
                            .filter_by(uid=self._uid,
                                       playlistid=playlistid).first()
                    if playlist is None:
                        return 'No %s in self playlist!' % playlistid
                    else:
                        image_small = playlist.image_smallmall
                        image_middle = playlist.image_middleiddle
                        image_large = playlist.image_largeagre
                        playlistname = playlist.playlistname

                elif listtype == 2:
                    s = {'length': 1, 'offset': 0, 'albumid': playlistid}
                    playlist = albumapi.GetAlbumSync(s).get()
                    image_small = playlist['response']['docs'][0]['imagePathMap'][0]['value']
                    image_middle = playlist['response']['docs'][0]['imagePathMap'][1]['value']
                    image_large = playlist['response']['docs'][0]['imagePathMap'][2]['value']
                    playlistname = playlist['response']['docs'][0]['name']

                elif listtype == 3:
                    s = {'length': 1, 'offset': 0, 'categoryid': playlistid}
                    playlist = playlistapi.GetPlayListInfoSync(s).get()
                    image_small = playlist['response']['docs']['imagePathMap'][0]['value']
                    image_middle = playlist['response']['docs']['imagePathMap'][1]['value']
                    image_large = playlist['response']['docs']['imagePathMap'][2]['value']
                    playlistname = playlist['response']['docs']['name']
                else:
                    return 'Unsupported list type.'
                data = {'uid': self._uid,
                        'vin': self._vin,
                        'playlistid': playlistid,
                        'playlistname': playlistname,
                        'imagepathmapSmall': image_small,
                        'imagepathmapMiddle': image_middle,
                        'imagepathmapLarge': image_large,
                        'favorite': True,
                        'time': time_array,
                        'type': listtype}
                add_item = (base.UserCollectPlayList(**data))
                self._conn.session.add(add_item)
            else:
                collect.favorite = True
                collect.vin = self._vin
                collect.time = time_array
            self._conn.commit()
            return True
        except SQLConnectError:
            self._conn.session.rollback()
            traceback.print_exc()
            return False

    def cancel(self, timestamp, playlistid, typelist):
        """

        :param timestamp:
        :param playlistid:
        :param selflist:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            if self._uid is None:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               vin=self._vin,
                               playlistid=playlistid,
                               type=typelist,
                               favorite=True).all()
            else:
                collect = self._conn.session.query(base.UserCollectPlayList)\
                    .filter_by(uid=self._uid,
                               playlistid=playlistid,
                               type=typelist,
                               favorite=True).all()
            if collect is None:
                return "No playlist collected in the database."
            else:
                for i in collect:
                    i.favorite = False
                    i.vin = self._vin
                    i.time = time_array
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('cancel failre')
            return False


class UserPlaylist(Common):
    def __init__(self, vin, uid=None, conn=CONN):
        """

        :param vin:
        :param uid:
        :param conn:
        """
        super(UserPlaylist, self).__init__(vin, uid, conn)

    def get(self):
        """

        :return:
        """
        try:
            query = self._conn.session.query(base.UserPlayList)
            if self._uid is None:
                data = query.filter_by(vin=self._vin, uid=self._uid).all()
            else:
                data = query.filter_by(uid=self._uid).all()
            out = [{'playlistid': i.playlistid,
                    'playlistname': i.playlistname,
                    'imageS': i.imageSmall,
                    'imageM': i.imageMiddle,
                    'imageL': i.imageLarge} for i in data]
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            return False

    def create(self, playlistname):
        """

        :param playlistname:
        :return:
        """
        try:
            data = {'playlistname': playlistname,
                    'vin': self._vin,
                    'uid': self._uid,
                    'createtime': datetime.datetime.now(),
                    'favorite': False}
            playlist = base.UserPlayList(**data)
            self._conn.session.add(playlist)
            self._conn.session.commit()
            return {'playlistid': playlist.playlistid}
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            return False

    def add(self, timestamp, playlistid, itemid):
        """

        :param timestamp:
        :param playlistid:
        :param itemid:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            playlist = self._conn.session.query(base.UserPlayList)\
                .filter_by(playlistid=playlistid).first()
            if playlist is None:
                return False
            playlistcontent = self._conn.session.query(base.UserPlayListContent).filter_by(playlistid=playlistid, itemid=itemid).first()
            if playlistcontent is None:
                song = self._conn.session.query(base.Song).filter_by(itemid=itemid).first()
                if song is None:
                    s = {'itemid': itemid}
                    songdata = music.GetMusicSync(s).get()['response']['docs'][0]
                    translatename = songdata['datainfo']['translatename']
                    artistid = songdata['artists'][0]['artistID']
                    artistname = songdata['artists'][0]['name']
                    albumid = songdata['album']['albumID']
                    genre = songdata['datainfo']['genre']
                    rating = songdata['datainfo']['rating']
                    contentproviderid = songdata['album']['cpinfo'][0]['contentProviderID']
                    image_small = songdata['ablum']['imagePathMap'][3]
                    image_middle = songdata['ablum']['imagePathMap'][4]
                    image_large = songdata['ablum']['imagePathMap'][2]
                    addsong = {'itemid': itemid,
                               'translatename': translatename,
                               'artistid': artistid,
                               'artistname': artistname,
                               'albumid': albumid,
                               'contentproviderid': contentproviderid,
                               'genre': genre,
                               'rating': rating,
                               'imagepathmapSmall': image_small,
                               'imagepathmapMiddle': image_middle,
                               'imagepathmapLarge': image_large}
                    newsong = base.Song(**addsong)
                    self._conn.session.add(newsong)
                else:
                    translatename = song.translatename
                    image_small = song.imagepathmapSmall
                    image_middle = song.imagepathmapMiddle
                    image_large = song.imagepathmapLarge
                valid = True
                data = {'playlistid': playlistid,
                        'itemid': itemid,
                        'translatename': translatename,
                        'valid': valid,
                        'time': time_array}
                additem = base.UserPlayListContent(**data)
                playlist.image_smallmall = image_small
                playlist.image_middleiddle = image_middle
                playlist.image_largeagre = image_large
                self._conn.session.add(additem)
            else:
                playlistcontent.valid = True
                playlistcontent.vin = self._vin
                playlistcontent.time = time_array
            playlist.modifiedtime = time_array
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('add failre')
            return False

    def cancel(self, timestamp, playlistid, itemid):
        """

        :param timestamp:
        :param playlistid:
        :param itemid:
        :return:
        """
        try:
            time_array = datetime.datetime.fromtimestamp(timestamp)
            playlist = self._conn.session.query(base.UserPlayList)\
                .filter_by(playlistid=playlistid).first()
            if playlist is None:
                return False
            playlistcontent = self._conn.session.query(base.UserPlayListContent) \
                .filter_by(playlistid=playlistid,
                           itemid=itemid).first()
            if playlistcontent is None:
                song = self._conn.session.query(base.Song)\
                    .filter_by(itemid=itemid).first()
                if song is None:
                    s = {'itemid': itemid}
                    songdata = music.GetMusicSync(s).get()['response']['docs'][0]
                    translatename = songdata['datainfo']['translatename']
                    artistid = songdata['artists'][0]['artistID']
                    artistname = songdata['artists'][0]['name']
                    albumid = songdata['album']['albumID']
                    genre = songdata['datainfo']['genre']
                    rating = songdata['datainfo']['rating']
                    contentproviderid = songdata['album']['cpinfo'][0]['contentProviderID']
                    image_small = songdata['ablum']['imagePathMap'][3]
                    image_middle = songdata['ablum']['imagePathMap'][4]
                    image_large = songdata['ablum']['imagePathMap'][2]
                    addsong = {'itemid': itemid,
                               'translatename': translatename,
                               'artistid': artistid,
                               'artistname': artistname,
                               'albumid': albumid,
                               'contentproviderid': contentproviderid,
                               'genre': genre,
                               'rating': rating,
                               'imagepathmapSmall': image_small,
                               'imagepathmapMiddle': image_middle,
                               'imagepathmapLarge': image_large}
                    newsong = base.Song(**addsong)
                    self._conn.session.add(newsong)
                else:
                    translatename = song.translatename
                valid = False
                data = {'playlistid': playlistid,
                        'itemid': itemid,
                        'translatename': translatename,
                        'valid': valid,
                        'time': time_array}
                additem = base.UserPlayListContent(**data)
                self._conn.session.add(additem)

            else:
                playlistcontent.valid = False
                playlistcontent.time = time_array
            playlist.modifiedtime = time_array
            self._conn.commit()
            return True
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('cancel failre')
            return False

    def getplaylistcontent(self, playlistid):
        """

        :param playlistid:
        :return:
        """
        try:
            query = self._conn.session.query(base.UserPlayListContent)
            data = query.filter_by(playlistid=playlistid, valid=True).order_by(base.UserPlayListContent.time.desc())
            if not data:
                out = 'No items in the playlist.'
            else:
                out = [{'itemid': i.itemid,
                        'translatename': i.translatename} for i in data]
            return out
        except:
            self._conn.session.rollback()
            traceback.print_exc()
            print('getplaylistcontent failre')
            return False


class UserHistoryBase(object):
    def __init__(self, conn=CONN):
        """

        :param conn:
        """
        self._conn = conn

    def getuid(self):
        """

        :return:
        """
        query = "SELECT DISTINCT tb_song_history.uid " \
                "from tb_song_history where tb_song_history.uid<>'';"
        uid = self._conn.session.execute(query)
        return uid

    def getvin(self):
        """

        :return:
        """
        query = "SELECT DISTINCT tb_song_history.vin " \
                "from tb_song_history where ISNULL(tb_song_history.uid);"
        vin = self._conn.session.execute(query)
        return vin
