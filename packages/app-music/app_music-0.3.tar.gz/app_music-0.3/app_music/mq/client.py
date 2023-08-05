#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2018/2/28 9:39
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : client
# @Project : roewe_voice 
# @Contact : guangze.yu@foxmail.com
"""
import pika
import config.rabbitmq as cfg
from utils import logger


LOG = logger.get_logger(__name__)
HOST = cfg.pika_host
PORT = cfg.pika_port
USER = cfg.pika_username
PWD = cfg.pika_password


class PikaClient(object):
    """Class PikaClient
    A client for rabbitMQ using tornado ioloop.
    """
    def __init__(self, io_loop):
        print('PikaClient: __init__')
        self.io_loop = io_loop
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
        self.message_count = 0

    def connect(self):
        if self.connecting:
            return
        self.connecting = True
        cred = pika.PlainCredentials(USER, PWD)
        param = pika.ConnectionParameters(host=HOST,
                                          port=PORT,
                                          virtual_host='/',
                                          credentials=cred)
        self.connection = \
            pika.adapters.TornadoConnection(parameters=param,
                                            on_open_callback=self.on_connected,
                                            stop_ioloop_on_close=False)
        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        print('PikaClient: connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        print('PikaClient: Channel %s open, Declaring exchange' % channel)
        self.channel = channel

    def on_closed(self):
        print('PikaClient: rabbit connection closed')
        self.io_loop.stop()
