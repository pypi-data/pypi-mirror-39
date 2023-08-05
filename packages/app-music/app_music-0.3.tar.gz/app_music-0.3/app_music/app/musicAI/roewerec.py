# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 10:19:23 2018

@author: zsj
"""
import pandas as pd
import random
import threading

import vendor.aiting.recommend as recommend
import vendor.aiting.playlist as playlist
import database.operation as operation
import database.definition as definition


###推荐########################################################################
###############################################################################
def createRadioByName(artists, length=100):
    '''
    根据歌手名称、歌曲ID创建个性化歌单
    多个名称逗号分隔
    '''
    s = {'length': str(length),
         'artists': artists}
    a = recommend.CreateRadioByName(s).get()
    return a


# t=createRadioByName('张惠妹,林俊杰', length=100)

def createRadioById(trackids, length=100):
    '''
    根据歌曲ID创建个性化歌单
    多个ID逗号分隔
    '''
    s = {'length': str(length),
         'trackids': trackids}
    a = recommend.CreateRadioById(s).get()
    return a


# t=createRadioById('9571999', length=100)

def tuningRadio(playlistid, popularity=500, similarity=500):
    '''
    调节个性化歌单的匹配度
    值越大匹配度越高
    '''
    s = {'popularity': str(popularity),
         'playlistid': playlistid,
         'similarity': str(similarity)
         }
    a = recommend.TuningRadio(s).get()
    return a


# t=tuningRadio(popularity=500,playlistid='302272',similarity=300)

def getPlayListInfoSync(categoryid='7851', length=100, offset=0):
    '''
    获取歌单详情
    '''
    s = {'categoryid': categoryid,
         'length': str(length),
         'offset': str(offset)
         }
    a = playlist.GetPlayListInfoSync(s).get()
    return a


# t=getPlayListInfoSync(categoryid='8251',length=100,offset=0)

###############################################################################
def get_histlist(vin='AAAAAAAAAAAAAAAAA', uid=888888):
    '''
    获得用户播放历史
    '''
    Conn = definition.Connect()
    Histlist = operation.SongHistoryList(vin, uid, conn=Conn)
    userinfo = Histlist.stat()
    Conn.close()
    return userinfo


def userinfo(user_list):
    '''
    返回pd.DataFrame
    '''
    user_list = pd.DataFrame(user_list)
    user_list = user_list.fillna('')
    user_list = user_list.sort_values(by='playnum', ascending=False)
    return user_list


###############################################################################
def recRadio(artists='', tracks='', trackids='', length=100):
    '''
    创建个性化歌单
    '''
    s = {'length': str(length)}
    if artists != '':
        s['artists'] = artists
    if tracks != '':
        s['tracks'] = tracks
    if trackids != '':
        s['trackids'] = trackids
    a = recommend.CreateRadioByName(s).get()
    a = a.get('response', {})
    a = a.get('docs', {})
    a = a.get('stationItems', [])
    return a


def recRadioTuning(artists='', tracks='', trackids='', popularity=500, similarity=500, length=100):
    '''
    创建个性化歌单,并调整流行度和相似度
    '''
    s = {'length': str(length)}
    if artists != '':
        s['artists'] = artists
    if tracks != '':
        s['tracks'] = tracks
    if trackids != '':
        s['trackids'] = trackids
    playlistid = recommend.CreateRadioByName(s).get()
    playlistid = playlistid.get('response', {})
    playlistid = playlistid.get('docs', {})
    playlistid = playlistid.get('playListID', '')
    a = []
    if playlistid != '':
        a = tuningRadio(playlistid, popularity, similarity)
        a = a.get('response', {})
        a = a.get('docs', {})
        a = a.get('stationItems', [])
    return a


def getItemArtistAlbum(item):
    '''
    处理数据，按条整理。
    '''
    data = {}
    t = item.get('artists', [])
    data['artistID'] = ''
    data['artistname'] = ''
    for i in t:
        data['artistID'] = data['artistID'] + str(i.get('artistID', '')) + ','
        data['artistname'] = data['artistname'] + i.get('name') + ','
    data['artistID'] = data['artistID'].rstrip(',')
    data['artistname'] = data['artistname'].rstrip(',')
    data['itemID'] = item.get('itemID', '')
    t = item.get('album', {})
    data['albumID'] = t.get('albumID', '')
    imagepath = t.get('imagePathMap', {})
    for i in imagepath:
        data[i['key']] = i['value']
    data['albumname'] = t.get('name', '')
    data['itemname'] = item.get('datainfo', {}).get('name', '')

    return data


def recRadioLite(artists='', tracks='', trackids='', length=100):
    '''
    获取推荐歌曲简要版
    '''
    temp = recRadio(artists, tracks, trackids, length=100)
    temp = list(map(getItemArtistAlbum, temp))
    return temp


def recRadioLite_artist(artists='', length=20):
    return recRadioLite(artists=artists, length=length)


def recRadioLite_trackids(trackids='', length=20):
    return recRadioLite(trackids=trackids, length=length)


def getNewSonglist():
    '''
    获取新歌歌单详情
    歌单categoryid='7851'
    '''
    s = getPlayListInfoSync(categoryid='7851', length=100, offset=0)
    s = s.get('response')
    s = s.get('docs')
    s = s.get('stationItems')
    s = random.sample(s, 20)
    s = list(map(getItemArtistAlbum, s))
    return s


###############################################################################
def roewerec(vin='AAAAAAAAAAAAAAAAA', uid=888888, num=20):
    user = get_histlist(vin, uid)
    items_user = user.get('song', [])
    artists_user = user.get('artist', [])
    if len(items_user) == 0 and len(artists_user) == 0:
        return getNewSonglist()
    if len(items_user) >= 6:
        randomint = random.sample([i for i in range(3, len(items_user))], k=1)
        items_user = items_user[0:3] + items_user[randomint[0]:randomint[0] + 1]

    if len(artists_user) >= 6:
        randomint = random.sample([i for i in range(3, len(artists_user))], k=1)
        artists_user = artists_user[0:3] + artists_user[randomint[0]:randomint[0] + 1]

    itemids = []
    for i in items_user:
        itemid = str(i.get('itemid', ''))
        if itemid != '':
            itemids.append(itemid)

    artistnames = []
    for i in artists_user:
        artistname = str(i.get('artistname', ''))
        if artistname != '':
            artistnames.append(artistname)

    rec_list1 = [None for i in range(len(artistnames))]
    thread_list = []

    def multi_thread_artist(artistnames, itemids, i):
        rec_list1[i] = recRadioLite_artist(artists=artistnames[i])

    for i in range(len(artistnames)):
        t = threading.Thread(target=multi_thread_artist, args=(artistnames, itemids, i))
        t.setDaemon(True)
        thread_list.append(t)
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()

    rec_list2 = [None for i in range(len(itemids))]
    thread_list = []

    def multi_thread_item(itemids, i):
        rec_list2[i] = recRadioLite_trackids(trackids=itemids[i])

    for i in range(len(itemids)):
        t2 = threading.Thread(target=multi_thread_item, args=(itemids, i))
        t2.setDaemon(True)
        thread_list.append(t2)
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()

    reclist = []
    if len(rec_list1) == 4 and len(rec_list2) == 4:
        for i in rec_list1[0:3]:
            try:
                reclist = reclist + i
            except:
                pass
        for i in rec_list2[0:3]:
            try:
                reclist = reclist + i
            except:
                pass
        try:
            reclist = reclist + rec_list1[3]
            reclist = reclist + rec_list2[3]
        except:
            pass
    else:
        for i in rec_list1:
            try:
                reclist = reclist + i
            except:
                pass
        for i in rec_list2:
            try:
                reclist = reclist + i
            except:
                pass
    if isinstance(reclist, list) and len(reclist) > 0:
        try:
            reclist = pd.DataFrame(reclist)
            reclist = reclist.drop_duplicates(['itemID'])
            reclist = reclist.fillna('')
        except:
            pass
        try:
            reclist = reclist.to_dict('records')
        except:
            pass

    if len(reclist) > num:
        temp = random.sample(range(len(reclist)), num)
        temp.sort()
        return [reclist[i] for i in temp]
    else:
        return reclist