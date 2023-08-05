#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main
主函数，定义各子服务的Handler。

"""
from urllib.request import urlopen
from json import load
import tornado.web as web
import server.handler as handler
import tornado.ioloop as ioloop
from tornado.options import options, define
from kazoo.client import KazooClient
from utils import logger
import mq.client as mq_client
import config.zookeeper as config
from init import update

LOG = logger.get_logger(__name__)
IP = load(urlopen('http://ip-api.com/json'))['query']
define('port', default=8887, type=int, help='Server port')
define('bind', default='0.0.0.0', type=str, help='Server bind')
define('zk_connect',
       default=config.zookeeper_host,
       type=str,
       help='zookeeper connect')

ZK = KazooClient(hosts=options.zk_connect)


def zk_stats():
    """zk_stats
    检测zookeeper连接状态，如果连接断开，将尝试重连。
    """
    if ZK.state == 'LOST':
        LOG.info('zookeeper state:%s' % ZK.state)
        ZK.start()


if __name__ == "__main__":
    TestHandler = handler.CommonHandler
    SearchHandler = handler.RoeweMusicSearchHandler
    CollectHandler = handler.RoeweMusicCollectHandler
    PlayHandler = handler.RoeweMusicPlayHandler
    PlayListHandler = handler.RoeweMusicPlayListHandler
    PlayHistoryHandler = handler.RoeweMusicPlayHistoryHandler
    MoreInfoHandler = handler.RoeweMusicMoreInfoHandler
    RecommendHandler = handler.RoeweMusicRecommendHandler
    ApeListHandler = handler.RoeweMusicApeListHandler
    handlers = [(r'/music/test/(.*)', TestHandler),
                (r'/music/collect/(.*)', CollectHandler),
                (r'/music/search/(.*)', SearchHandler),
                (r'/music/play/(.*)', PlayHandler),
                (r'/music/playlist/(.*)', PlayListHandler),
                (r'/music/playhistory/(.*)', PlayHistoryHandler),
                (r'/music/moreinfo/(.*)', MoreInfoHandler),
                (r'/music/recommend/(.*)', RecommendHandler),
                (r'/music/flaclist/(.*)', ApeListHandler)]
    app = web.Application(handlers)
    setattr(app, 'options', options)
    app.listen(options.port, address=options.bind)
    ZK.start()
    if ZK.exists('/roewe_server') is None:
        ZK.create('/roewe_server')
    if ZK.exists('/roewe_server/music') is None:
        ZK.create('/roewe_server/music')
    if ZK.exists('/roewe_server/music/%s:%s' % (IP, options.port)) is None:
        ZK.create(path='/roewe_server/music/%s:%s' % (IP, options.port), ephemeral=True)
    ioloop.PeriodicCallback(zk_stats, 100000).start()
    # ioloop.PeriodicCallback(update, 1000*60*60*24).start()
    main_loop = ioloop.IOLoop.instance()
    mq_conn = mq_client.PikaClient(main_loop)
    setattr(app, 'mq', mq_conn)
    main_loop.start()
