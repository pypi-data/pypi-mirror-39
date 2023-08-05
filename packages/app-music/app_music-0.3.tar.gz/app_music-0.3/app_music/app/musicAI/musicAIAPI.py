# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 09:27:11 2018

@author: zsj
"""
import app.musicAI.aifunc as aifunc
import app.musicAI.songlist as sl
import app.musicAI.roewerec as rr


def searchItemAPI(searchvalue, vin, uid, pageSize):
    '''
    搜索歌曲（推荐）
    '''
    #    artists_user = [None for i in range(5)]
    #    artists_user[0] = {'artistName':'林俊杰', 'artistId':'16114', 'favorTimes':'210', 'playedTimes':'350'}
    #    artists_user[1] = {'artistName':'周杰伦', 'artistId':'6478', 'favorTimes':'200', 'playedTimes':'300'}
    #    artists_user[2] = {'artistName':'五月天', 'artistId':'9209', 'favorTimes':'190', 'playedTimes':'400'}
    #    artists_user[3] = {'artistName':'苏打绿', 'artistId':'16657', 'favorTimes':'180', 'playedTimes':'320'}
    #    artists_user[4] = {'artistName':'王菲', 'artistId':'7208', 'favorTimes':'170', 'playedTimes':'300'}
    #
    #    items_user = [None for i in range(5)]
    #    items_user[0] = {'itemName':'她说', 'itemId':'67705', 'favorTimes':'210', 'playedTimes':'350'}
    #    items_user[1] = {'itemName':'发如雪', 'itemId':'1066822', 'favorTimes':'200', 'playedTimes':'300'}
    #    items_user[2] = {'itemName':'私奔到月球', 'itemId':'73119', 'favorTimes':'190', 'playedTimes':'400'}
    #    items_user[3] = {'itemName':'小情歌', 'itemId':'1036947', 'favorTimes':'180', 'playedTimes':'320'}
    #    items_user[4] = {'itemName':'将爱', 'itemId':'1172046', 'favorTimes':'170', 'playedTimes':'300'}

    return aifunc.searchItemAIlite(searchvalue, vin, uid, pageSize)


def searchArtistAI(searchvalue, vin, uid, pageSize):
    '''
    搜索歌手（推荐）
    '''
    #    artists_user = [None for i in range(5)]
    #    artists_user[0] = {'artistName':'林俊杰', 'artistId':'16114', 'favorTimes':'210', 'playedTimes':'350'}
    #    artists_user[1] = {'artistName':'周杰伦', 'artistId':'6478', 'favorTimes':'200', 'playedTimes':'300'}
    #    artists_user[2] = {'artistName':'五月天', 'artistId':'9209', 'favorTimes':'190', 'playedTimes':'400'}
    #    artists_user[3] = {'artistName':'苏打绿', 'artistId':'16657', 'favorTimes':'180', 'playedTimes':'320'}
    #    artists_user[4] = {'artistName':'王菲', 'artistId':'7208', 'favorTimes':'170', 'playedTimes':'300'}

    return aifunc.searchArtistAIlite(searchvalue, vin, uid, pageSize)


def searchAlbumAI(searchvalue, vin, uid, pageSize):
    '''
    搜索专辑（推荐）
    '''
    #    artists_user = [None for i in range(5)]
    #    artists_user[0] = {'artistName':'林俊杰', 'artistId':'16114', 'favorTimes':'210', 'playedTimes':'350'}
    #    artists_user[1] = {'artistName':'周杰伦', 'artistId':'6478', 'favorTimes':'200', 'playedTimes':'300'}
    #    artists_user[2] = {'artistName':'五月天', 'artistId':'9209', 'favorTimes':'190', 'playedTimes':'400'}
    #    artists_user[3] = {'artistName':'苏打绿', 'artistId':'16657', 'favorTimes':'180', 'playedTimes':'320'}
    #    artists_user[4] = {'artistName':'王菲', 'artistId':'7208', 'favorTimes':'170', 'playedTimes':'300'}
    #
    #    albums_user = [None for i in range(5)]
    #    albums_user[0] = {'albumName':'她说', 'albumId':'11537', 'favorTimes':'210', 'playedTimes':'350'}
    #    albums_user[1] = {'albumName':'十一月的萧邦', 'albumId':'99529', 'favorTimes':'200', 'playedTimes':'300'}
    #    albums_user[2] = {'albumName':'离开地球表面Jump!The World 2007极限大碟', 'albumId':'12075', 'favorTimes':'190', 'playedTimes':'400'}
    #    albums_user[3] = {'albumName':'小宇宙', 'albumId':'95543', 'favorTimes':'180', 'playedTimes':'320'}
    #    albums_user[4] = {'albumName':'将爱', 'albumId':'107304', 'favorTimes':'170', 'playedTimes':'300'}

    return aifunc.searchAlbumAIlite(searchvalue, vin, uid, pageSize)


def dailysonglist():
    '''
    每日推荐
    '''
    return sl.getNewSonglist()


def roewerecommend(vin, uid, num=20):
    '''
    荣威推荐
    '''
    return rr.roewerec(vin, uid, num)
