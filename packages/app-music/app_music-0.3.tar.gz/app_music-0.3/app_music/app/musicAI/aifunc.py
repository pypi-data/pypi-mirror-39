# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 09:05:26 2018

@author: zsj
"""

import pandas as pd

import vendor.aiting.search as search
import vendor.aiting.others as others
import vendor.aiting.music as music
import vendor.aiting.artist as artist
import database.operation as data_base
import database.definition as definition


####搜索#######################################################################
def searchMusicAsyncCN(searchvalue, page=0, pageSize=20):
    '''
    搜索歌曲中文
    searchvalue：str
    '''
    s = {'start': str(page),
         'rows': str(pageSize),
         'itemtype': 'FTD',
         'searchvalue': searchvalue}
    a = search.SearchMusicAsyncCN(s).get()
    return a


# t=searchMusicAsyncCN('just the way you are', page=0, pageSize=100)

def searchMusicAsyncEN(searchvalue, page=0, pageSize=20):
    '''
    搜索歌曲英文、拼音、数字
    searchvalue：str
    '''
    s = {'start': str(page),
         'rows': str(pageSize),
         'itemtype': 'FTD',
         'searchvalue': searchvalue}
    a = search.SearchMusicAsyncEN(s).get()
    return a


# t=searchMusicAsyncEN('just the way you are', page=0, pageSize=100)

def searchArtistAvatarSync(searchvalue, page=0, pageSize=20):
    '''
    搜索歌手
    searchvalue：str
    '''
    s = {'start': str(page),
         'rows': str(pageSize),
         'searchvalue': searchvalue}
    a = search.SearchArtistAvatarSync(s).get()
    return a


# t=searchArtistAvatarSync('justin bieber', page=0, pageSize=20)

def aggregateSearchSync(searchvalue, page=0, pageSize=20):
    '''
    搜索歌曲、歌手、专辑
    searchvalue：str
    '''
    s = {'start': str(page),
         'rows': str(pageSize),
         'searchvalue': searchvalue}
    a = search.AggregateSearchSync(s).get()
    return a


# t=aggregateSearchSync('justin bieber', page=0, pageSize=20)

def searchAlbumSync(searchvalue, page=0, pageSize=20):
    '''
    搜索专辑
    searchvalue：str
    '''
    s = {'start': str(page),
         'rows': str(pageSize),
         'searchvalue': searchvalue}
    a = others.SearchAlbumSync(s).get()
    return a


# t=searchAlbumSync('justin bieber', page=0, pageSize=20)
###############################################################################
def getArtistMusicListSync(artistid, offset=0, length=20):
    '''
    请求歌手音乐
    searchvalue：str
    '''
    s = {'artistid': artistid,
         'offset': str(offset),
         'length': str(length)}
    a = artist.GetArtistMusicListSync(s).get()
    return a


###############################################################################
###音乐########################################################################
def getMusicSync(itemid, liteversion='N'):
    '''
    请求歌曲详细信息
    '''
    s = {'liteversion': liteversion,
         'itemid': itemid}
    a = music.GetMusicSync(s).get()
    return a


# t=getMusicSync(liteversion='N',itemid='67848',bit='MP3-128K-FTD')

####func#######################################################################
def judge_pure_english(keyword):
    '''
    判断是否为英文或拼音搜索（字母，数字，空格）
    返回bool
    '''
    return all(ord(c) < 128 for c in keyword)


def searchItem(searchvalue, page=0, pageSize=20):
    '''
    搜索歌曲
    searchvalue：str
    '''
    if judge_pure_english(searchvalue):
        items = searchMusicAsyncEN(searchvalue, page, pageSize)
    else:
        items = searchMusicAsyncCN(searchvalue, page, pageSize)
    items = items.get('response', {})
    items = items.get('docs', [])
    return items


def searchArtist(searchvalue, page=0, pageSize=20):
    '''
    搜索歌手
    searchvalue：str
    '''
    artists = searchArtistAvatarSync(searchvalue, page, pageSize)
    artists = artists.get('response', {})
    artists = artists.get('docs', [])
    return artists


def searchAlbum(searchvalue, page=0, pageSize=20):
   '''
   搜索专辑
   searchvalue：str
   '''
   albums = aggregateSearchSync(searchvalue, page, pageSize)
   albums = albums.get('response', {})
   albums = albums.get('docs', {})
   albums = albums.get('Albums', [])
   return albums

# def searchAlbum(searchvalue, page=0, pageSize=20):
#     '''
#     搜索专辑
#     searchvalue：str
#     '''
#     albums = searchAlbumSync(searchvalue, page, pageSize)
#     albums = albums.get('response', {})
#     albums = albums.get('docs', {})
#     return albums


###############################################################################

def get_histlist(vin='AAAAAAAAAAAAAAAAA', uid=888888):
    '''
    获得用户播放历史
    '''
    Conn = definition.Connect()
    Histlist = data_base.SongHistoryList(vin, uid, conn=Conn)
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


def delistobj(i):
    if isinstance(i, list) and len(i) > 0:
        return str(i[0])


def listobj(i):
    return [i]


def processlistobj(i):
    if isinstance(i, list) and len(i) > 0:
        string = ''
        for item in i:
            string = string + str(item) + ','
        string = string.rstrip(',')
        return string


###############################################################################
####搜索#######################################################################
def searchItemAI(searchvalue, vin, uid, pageSize=50):
    '''
    搜索歌曲（推荐）
    '''

    items = searchItem(searchvalue, page=0, pageSize=150)
    user = get_histlist(vin, uid)
    items_user = user.get('song', [])
    artists_user = user.get('artist', [])

    if len(items) > 0:
        items = pd.DataFrame(items)
        items = items.fillna('')
        items = items.sort_values(by='Rating', ascending=False)

        if len(items_user) > 0:
            items_user = userinfo(items_user)
            items_by_items = items[items['ItemID'].isin(list(items_user['itemid'].map(str)))]
        else:
            items_by_items = []

        if len(artists_user) > 0:
            items_by_artists = items.copy()
            items_by_artists['ArtistIDS'] = list(map(delistobj, list(items_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            items_by_artists = items_by_artists[
                items_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            items_by_artists = items_by_artists.drop(['ArtistIDS'], axis=1)

        else:
            items_by_artists = []

        new_items = items_by_items.append(items_by_artists)
        new_items = new_items.append(items)
        new_items = new_items.drop_duplicates(['ItemID'])
        new_items = new_items.to_dict('records')

        if len(new_items) > pageSize:
            return new_items[0:pageSize]
        else:
            return new_items
    else:
        return []


def searchArtistAI(searchvalue, vin, uid, pageSize=50):
    '''
    搜索歌手（推荐）
    '''

    artists = searchArtist(searchvalue, page=0, pageSize=200)
    user = get_histlist(vin, uid)
    artists_user = user.get('artist', [])

    if len(artists) > 0:
        artists = pd.DataFrame(artists)
        artists = artists.fillna('')
        artists = artists.sort_values(by='Rating', ascending=False)

        if len(artists_user) > 0:
            artists_by_artists = artists.copy()
            artists_by_artists['ArtistIDS'] = list(map(delistobj, list(artists_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            artists_by_artists = artists_by_artists[
                artists_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            artists_by_artists = artists_by_artists.drop(['ArtistIDS'], axis=1)

        else:
            artists_by_artists = []

        new_artists = artists_by_artists.append(artists_by_artists)
        new_artists = new_artists.append(artists)
        new_artists = new_artists.drop_duplicates(['ArtistID'])
        new_artists = new_artists.to_dict('records')
        if len(new_artists) > pageSize:
            return new_artists[0:pageSize]
        else:
            return new_artists
    else:
        return []


def searchAlbumAI(searchvalue, vin, uid, pageSize=50):
    '''
    搜索专辑（推荐）
    '''

    albums = searchAlbum(searchvalue, page=0, pageSize=200)
    user = get_histlist(vin, uid)
    albums_user = user.get('album', [])
    artists_user = user.get('artist', [])

    if len(albums) > 0:
        albums = pd.DataFrame(albums)
        albums = albums.fillna('')
        # albums = albums.drop(['ArtistAttribute'], axis = 1) #如果使用aggregateSearchSync()获得albums需要加上此句
        albums = albums.sort_values(by='Rating', ascending=False)

        if len(albums_user) > 0:
            albums_user = userinfo(albums_user)
            albums_by_albums = albums[albums['AlbumID'].isin(list(albums_user['albumid'].map(str)))]
        else:
            albums_by_albums = []

        if len(artists_user) > 0:
            albums_by_artists = albums.copy()
            albums_by_artists['ArtistIDS'] = list(map(delistobj, list(albums_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            albums_by_artists = albums_by_artists[
                albums_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            albums_by_artists = albums_by_artists.drop(['ArtistIDS'], axis=1)
        else:
            albums_by_artists = []

        new_albums = albums_by_albums.append(albums_by_artists)
        new_albums = new_albums.append(albums)
        new_albums = new_albums.drop_duplicates(['AlbumID'])
        new_albums = new_albums.to_dict('records')
        if len(new_albums) > pageSize:
            return new_albums[0:pageSize]
        else:
            return new_albums
    else:
        return []


###############################################################################
####搜索后删除多余内容#######################################################################
def searchItemAIlite(searchvalue, vin, uid, pageSize=50):
    '''
    搜索歌曲（推荐）
    '''

    items = searchItem(searchvalue, page=0, pageSize=100)
    user = get_histlist(vin, uid)
    items_user = user.get('song', [])
    artists_user = user.get('artist', [])

    if len(items) > 0:
        items = pd.DataFrame(items)
        items = items.fillna('')
        items = items.sort_values(by='Rating', ascending=False)

        if len(items_user) > 0:
            items_user = userinfo(items_user)
            items_by_items = items[items['ItemID'].isin(list(items_user['itemid'].map(str)))]
        else:
            items_by_items = []

        if len(artists_user) > 0:
            items_by_artists = items.copy()
            items_by_artists['ArtistIDS'] = list(map(delistobj, list(items_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            items_by_artists = items_by_artists[
                items_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            items_by_artists = items_by_artists.drop(['ArtistIDS'], axis=1)
        else:
            items_by_artists = []

        if len(items_by_items) > 0:
            if len(items_by_artists) > 0:
                new_items = items_by_items.append(items_by_artists)
                new_items = new_items.append(items)
            else:
                new_items = items_by_items.append(items)
        elif len(items_by_artists) > 0:
            new_items = items_by_artists.append(items)
        else:
            new_items = items

        new_items = new_items.drop_duplicates(['ItemID'])

        colnames = list(new_items.columns)
        coltodel = ['Attribute',
                    'Bitrate',
                    'CPItemID',
                    'CPName',
                    'Exclusivity',
                    'ISRC',
                    'NameKey',
                    'PinyinFCAll',
                    'PinyinName',
                    '_version_']
        for i in coltodel:
            if i in colnames:
                new_items = new_items.drop([i], axis=1)

        new_items = new_items.to_dict('records')

        if len(new_items) > pageSize:
            return new_items[0:pageSize]
        else:
            return new_items
    else:
        return []


def searchArtistAIlite(searchvalue, vin, uid, pageSize=50):
    '''
    搜索歌手（推荐）
    '''

    artists = searchArtist(searchvalue, page=0, pageSize=200)
    user = get_histlist(vin, uid)
    artists_user = user.get('artist', [])

    if len(artists) > 0:
        artists = pd.DataFrame(artists)
        artists = artists.fillna('')
        artists = artists.sort_values(by='Rating', ascending=False)

        if len(artists_user) > 0:
            artists_by_artists = artists.copy()
            artists_by_artists['ArtistIDS'] = list(map(delistobj, list(artists_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            artists_by_artists = artists_by_artists[
                artists_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            artists_by_artists = artists_by_artists.drop(['ArtistIDS'], axis=1)
        else:
            artists_by_artists = []

        if len(artists_by_artists) > 0:
            new_artists = artists_by_artists.append(artists)
        else:
            new_artists = artists

        new_artists = new_artists.drop_duplicates(['ArtistID'])

        colnames = list(new_artists.columns)
        coltodel = ['NameKey',
                    'PinyinName',
                    '_version_']
        for i in coltodel:
            if i in colnames:
                new_artists = new_artists.drop([i], axis=1)
        if 'Attribute' in colnames:
            new_artists_attr = pd.DataFrame(list(new_artists['Attribute']))
            new_artists_attr = new_artists_attr.fillna('')
            colnames = list(new_artists_attr.columns)
            #            coltodel = [ 'AlternateDescription',
            #                         'AlternateHeadline',
            #                         'Blog',
            #                         'Description',
            #                         'Headline',
            #                         'Keyword',
            #                         'Url']
            coltoadd = ['AlbumCount',
                        'Birthday',
                        'Blood',
                        'Country',
                        'Height',
                        'Horoscope',
                        'ItemCount',
                        'JPG-1000X1000-ARTIST',
                        'JPG-200X200-ARTIST',
                        'JPG-240X240-ARTIST',
                        'JPG-320X320-ARTIST',
                        'JPG-600X600-ARTIST',
                        'Weight']
            for i in coltoadd:
                if i in colnames:
                    new_artists[i] = new_artists_attr[i]
            new_artists = new_artists.drop(['Attribute'], axis=1)

        new_artists = new_artists.to_dict('records')
        if len(new_artists) > pageSize:
            return new_artists[0:pageSize]
        else:
            return new_artists
    else:
        return []


def searchAlbumAIlite(searchvalue, vin, uid, pageSize=50):
    '''
    搜索专辑（推荐）
    '''

    albums = searchAlbum(searchvalue, page=0, pageSize=200)
    user = get_histlist(vin, uid)
    albums_user = user.get('album', [])
    artists_user = user.get('artist', [])

    if len(albums) > 0:
        albums = pd.DataFrame(albums)
        albums = albums.fillna('')
        albums = albums.drop(['ArtistAttribute'], axis=1)
        albums = albums.sort_values(by='Rating', ascending=False)

        if len(albums_user) > 0:
            albums_user = userinfo(albums_user)
            albums_by_albums = albums[albums['AlbumID'].isin(list(albums_user['albumid'].map(str)))]
        else:
            albums_by_albums = []

        if len(artists_user) > 0:
            albums_by_artists = albums.copy()
            albums_by_artists['ArtistIDS'] = list(map(delistobj, list(albums_by_artists['ArtistID'])))
            artists_user = userinfo(artists_user)
            albums_by_artists = albums_by_artists[
                albums_by_artists['ArtistIDS'].isin(list(artists_user['artistid'].map(str)))]
            albums_by_artists = albums_by_artists.drop(['ArtistIDS'], axis=1)
        else:
            albums_by_artists = []

        if len(albums_by_albums) > 0:
            if len(albums_by_artists) > 0:
                new_albums = albums_by_albums.append(albums_by_artists)
                new_albums = new_albums.append(albums)
            else:
                new_albums = albums_by_albums.append(albums)
        elif len(albums_by_artists) > 0:
            new_albums = albums_by_artists.append(albums)
        else:
            new_albums = albums

        colnames = list(new_albums.columns)
        coltodel = ['NameKey',
                    'PinyinName',
                    'UPC',
                    '_version_']
        for i in coltodel:
            if i in colnames:
                new_albums = new_albums.drop([i], axis=1)
        if 'Attribute' in colnames:
            new_albums_attr = pd.DataFrame(list(new_albums['Attribute']))
            new_albums_attr = new_albums_attr.fillna('')
            colnames = list(new_albums_attr.columns)
            coltoadd = ['JPG-1000X1000-ALBUM',
                        'JPG-240X240-ALBUM',
                        'JPG-320X320-ALBUM',
                        'JPG-600X600-ALBUM',
                        'NoOfTracks']
            for i in coltoadd:
                if i in colnames:
                    new_albums[i] = new_albums_attr[i]
            new_albums = new_albums.drop(['Attribute'], axis=1)

        new_albums = new_albums.drop_duplicates(['AlbumID'])
        new_albums = new_albums.to_dict('records')
        if len(new_albums) > pageSize:
            return new_albums[0:pageSize]
        else:
            return new_albums
    else:
        return []