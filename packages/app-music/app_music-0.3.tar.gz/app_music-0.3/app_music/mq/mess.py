#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/3/12 14:11
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : mess
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""
import json


class MessBase(object):
    def __init__(self, mess_cls, method, info, level='C'):
        """

        :param mess_cls:
        :param method:
        :param info:
        :param level:
        """
        self._level = level
        self._class = mess_cls
        self._info = info
        self._method = method

    @property
    def message(self):
        return {'level': self._level,
                'class': self._class,
                'method': self._method,
                'info': self._info}

    def __repr__(self):
        return json.dumps(self.message)


class SearchWordsHistory(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(SearchWordsHistory, self).__init__(mess_cls='SearchWordHistory',
                                                 method=method,
                                                 info=info,
                                                 level='C')


class TracksHistoryList(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(TracksHistoryList, self).__init__(mess_cls='TracksHistoryList',
                                                method=method,
                                                info=info,
                                                level='C')


class CollectTrack(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(CollectTrack, self).__init__(mess_cls='CollectTrack',
                                           method=method,
                                           info=info,
                                           level='A')


class CollectPlayList(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(CollectPlayList, self).__init__(mess_cls='CollectPlayList',
                                              method=method,
                                              info=info,
                                              level='A')


class UserPlaylist(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(UserPlaylist, self).__init__(mess_cls='UserPlaylist',
                                           method=method,
                                           info=info,
                                           level='A')


class SongHistoryList(MessBase):
    def __init__(self, method, info):
        """

        :param method:
        :param info:
        """
        super(SongHistoryList, self).__init__(mess_cls='SongHistoryList',
                                              method=method,
                                              info=info,
                                              level='C')
