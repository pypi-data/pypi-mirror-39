#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 18-1-11 上午9:16
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : base_init
# @Contact : guangze.yu@foxmail.com
"""
from sqlalchemy import create_engine, Boolean, DateTime
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config.mysql as cfg

BASE = declarative_base()


class Connect:
    """
    database connect:
    """
    def __init__(self, config=cfg.sqlconfig):
        self.engine = create_engine(config, encoding='utf-8')
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()

    def commit(self):
        """

        :return:
        """
        self.session.commit()

    def close(self):
        """

        :return:
        """
        self.session.close()

    def rollback(self):
        """

        :return:
        """
        self.session.rollback()

    def data_base_init(self):
        """

        :return:
        """
        # Base.metadata.drop_all(self.engine)
        BASE.metadata.create_all(self.engine)

    def data_base_add(self):
        """

        :return:
        """
        BASE.metadata.create_all(self.engine)


class UserSearchKeyWordHistory(BASE):
    """
    用户搜索历史数据表
    """
    __tablename__ = 'tb_searchword_history'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    keyword = Column(String(255), nullable=False)
    showinlist = Column(Boolean, nullable=False)


class UserSongHistoryList(BASE):
    """
    单曲历史列表
    """
    __tablename__ = 'tb_song_history'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    time = Column(DateTime, nullable=False)
    itemid = Column(Integer(), nullable=False)
    translatename = Column(String(255), nullable=True)
    artistid = Column(Integer(), nullable=True)
    artistname = Column(String(255), nullable=True)
    albumid = Column(Integer(), nullable=True)
    genre = Column(String(255), nullable=True)
    rating = Column(Integer(), nullable=True)
    modifiedtime = Column(DateTime, nullable=False)
    valid = Column(Boolean, nullable=False)


class Song(BASE):
    """
    单曲信息
    """
    __tablename__ = 'tb_song'
    itemid = Column(Integer(), primary_key=True, nullable=False)
    translatename = Column(String(255), nullable=True)

    artistid = Column(Integer(), nullable=True)
    artistname = Column(String(255), nullable=True)

    albumid = Column(Integer(), nullable=True)
    contentproviderid = Column(Integer(), nullable=True)
    genre = Column(String(255), nullable=True)
    rating = Column(Integer(), nullable=True)

    imagepathmapSmall = Column(String(1024), nullable=True)
    imagepathmapLarge = Column(String(1024), nullable=True)
    imagepathmapMiddle = Column(String(1024), nullable=True)


class UserCollectSong(BASE):
    """
    收藏单曲
    """
    __tablename__ = 'tb_user_collect_song'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    itemid = Column(Integer(), nullable=False)
    translatename = Column(String(255), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    artistname = Column(String(255), nullable=True)


class UserCollectPlayList(BASE):
    """
    收藏歌单
    """
    __tablename__ = 'tb_user_collect_playlist'
    index = Column(Integer(), primary_key=True, index=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    playlistid = Column(Integer(), nullable=False)
    playlistname = Column(String(255), nullable=True)
    imagepathmapSmall = Column(String(1024), nullable=True)
    imagepathmapMiddle = Column(String(1024), nullable=True)
    imagepathmapLarge = Column(String(1024), nullable=True)
    favorite = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    selflist = Column(Boolean, nullable=False)  # 是否为自建歌单
    type = Column(Integer(), nullable=True)


class UserPlayList(BASE):
    """
    用户歌单
    """
    __tablename__ = 'tb_user_playlist'
    playlistid = Column(Integer(), primary_key=True, index=True)
    playlistname = Column(String(255), nullable=True)
    uid = Column(Integer(), nullable=True)
    vin = Column(String(255), nullable=False)
    favorite = Column(Boolean, nullable=False)
    imageSmall = Column(String(1024), nullable=True)
    imageMiddle = Column(String(1024), nullable=True)
    imageLarge = Column(String(1024), nullable=True)
    createtime = Column(DateTime, nullable=False)
    modifiedtime = Column(DateTime, nullable=False)


class UserPlayListContent(BASE):
    """
    用户歌单内容
    """
    __tablename__ = 'tb_user_playlist_content'
    index = Column(Integer(), primary_key=True, index=True)
    playlistid = Column(Integer(), nullable=False)
    itemid = Column(Integer(), nullable=False)
    translatename = Column(String(255), nullable=True)
    valid = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
