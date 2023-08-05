# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:19:35 2018

@author: zsj
"""
import vendor.aiting.freshmusic as freshmusic
import vendor.aiting.playlist as playlist
import vendor.aiting.album as album


####API#########################################################################
def getPlayListSync(categorycode='Genre_SongList', length=100, offset=0):
    '''
    获取歌单列表
    '''
    s = {'length': str(length),
         'offset': str(offset),
         'categorycode': categorycode
         }
    a = playlist.GetPlayListSync(s).get()
    return a


# t=getPlayListSync(length=20,offset=0,categorycode='Genre_SongList')

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

def getFreshMusicListSync(categoryid='10', length=100, offset=0):
    '''
    请求新歌速递歌曲列表
    '''
    s = {'length': str(length),
         'offset': str(offset),
         'categoryid': categoryid
         }
    a = freshmusic.GetFreshMusicListSync(s).get()
    return a


def getHotMusicListSync(categoryid='4375', length=100, offset=0):
    '''
    请求热门歌曲列表
    '''
    s = {'length': str(length),
         'offset': str(offset),
         'categoryid': categoryid
         }
    a = freshmusic.GetHotMusicListSync(s).get()
    return a


def getNewAlbumListSync(categorycode='NL_Album_Newest', length=20, offset=0):
    '''
    请求新碟上架的专辑列表
    '''
    s = {'length': str(length),
         'offset': str(offset),
         'categorycode': categorycode
         }
    a = album.GetNewAlbumListSync(s).get()
    return a


def getAlbumSync(albumid):
    '''
    请求专辑内容
    '''
    s = {'albumid': albumid
         }
    a = album.GetAlbumSync(s).get()
    return a


###############################################################################
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


def getNewSonglist(length=20, offset=0):
    '''
    获取新歌歌单详情
    歌单categoryid='7851'
    '''
    s = getPlayListInfoSync(categoryid='7851', length=length, offset=offset)
    s = s.get('response')
    s = s.get('docs')
    s = s.get('stationItems')
    return s


def getNewSonglistLite(length=20, offset=0):
    '''
    获取新歌歌单简要版
    '''
    temp = getNewSonglist(length=length, offset=offset)
    temp = list(map(getItemArtistAlbum, temp))
    return temp
    ###############################################################################