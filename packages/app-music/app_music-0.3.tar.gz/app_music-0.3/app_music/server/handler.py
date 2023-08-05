#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 17-12-21 上午7:57
# @Author  : guangze.yu
# @Site    : shanghai
# @File    : main_server
# @Contact : guangze.yu@foxmail.com
"""

import traceback
import json
import tornado.web as web
import tornado.gen as gen
import tornado.concurrent as concurrent
import server.response as res
import utils.result as result
from utils import logger
from utils.exception import WebHandlerError

LOG = logger.get_logger(__name__)


class CommonHandler(web.RequestHandler):
    """
    common handler for the request.
    """
    mod = __import__('app.test', globals(), locals(), ['object'], 0)
    executor = concurrent.futures.ThreadPoolExecutor(200)

    @web.asynchronous
    @gen.coroutine
    def post(self, service):
        """

        :param service:
        :return:
        """
        path = self.request.path
        LOG.info('request path:%s', path)
        LOG.info('request ip:%s', self.request.remote_ip)
        vin = self.request.headers.get_list('Vin')[0]
        uid = self.request.headers.get_list('User_id')[0]
        timestamp = self.request.headers.get_list('Timestamp')[0]
        try:
            self.pika_connect()
        except:
            traceback.print_exc()
            LOG.info('Rabbitmq connect failure.')
        try:
            body_params = self.request.body
            if body_params.decode('utf-8'):
                params = json.loads(body_params.decode('utf-8'))
            else:
                params = {}
            if vin:
                params['vin'] = vin
            if uid:
                params['uid'] = uid
            if timestamp:
                params['timestamp'] = timestamp
            LOG.info('request params:%s', params)
            app_result = yield self.async_fun(service, params)
        except:
            traceback.print_exc()
            app_result = result.ErrorResult(WebHandlerError())
        return_info = res.Response(app_result, path, 'POST').info
        message = app_result.message
        self.set_header("Content-Type", "application/json")
        self.set_header("Status_code", app_result.status_code)
        self.set_header("Status_info", app_result.status_info)
        self.write(return_info)
        self.finish()
        if message is not None:
            self.application.mq.channel.queue_declare(callback=None,
                                                      queue='music',
                                                      durable=True)
            self.application.mq.channel.basic_publish(exchange='',
                                                      routing_key='music',
                                                      body=json.dumps(message))

    def pika_connect(self):
        """

        :return:
        """
        self.application.mq.connect()

    @concurrent.run_on_executor
    def async_fun(self, service, params):
        """

        :param service:
        :param params:
        :return:
        """
        func = getattr(self.mod, service)
        return func(params)


class RoeweMusicSearchHandler(CommonHandler):
    """
    RoeweMusicSearchHandler
    """
    mod = __import__('app.search', globals(), locals(), ['object'], 0)


class RoeweMusicCollectHandler(CommonHandler):
    """
    RoeweMusicCollectHandler
    """
    mod = __import__('app.collect', globals(), locals(), ['object'], 0)


class RoeweMusicPlayHistoryHandler(CommonHandler):
    """
    RoeweMusicPlayHistoryHandler
    """
    mod = __import__('app.playhistory', globals(), locals(), ['object'], 0)


class RoeweMusicPlayListHandler(CommonHandler):
    """
    RoeweMusicPlayListHandler
    """
    mod = __import__('app.playlist', globals(), locals(), ['object'], 0)


class RoeweMusicPlayHandler(CommonHandler):
    """
    RoeweMusicPlayHandler
    """
    mod = __import__('app.play', globals(), locals(), ['object'], 0)


class RoeweMusicMoreInfoHandler(CommonHandler):
    """
    RoeweMusicMoreInfoHandler
    """
    mod = __import__('app.more', globals(), locals(), ['object'], 0)


class RoeweMusicRecommendHandler(CommonHandler):
    """
    RoeweMusicRecommendHandler
    """
    mod = __import__('app.recommend', globals(), locals(), ['object'], 0)


class RoeweMusicApeListHandler(CommonHandler):
    """
    RoeweMusicRecommendHandler
    """
    mod = __import__('app.apelist', globals(), locals(), ['object'], 0)
