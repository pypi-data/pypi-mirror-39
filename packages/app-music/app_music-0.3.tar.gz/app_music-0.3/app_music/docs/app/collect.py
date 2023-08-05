#! usr/bin/env python
# coding = utf-8


def getsong():
    """
    @api {post} /music/collect/getsong 获取收藏的单曲
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 获取收藏的单曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} itemid 单曲编号
    @apiSuccess (Success) {Object} translatename 翻译名称

    @apiSuccessExample {json} Success-Response:
    [
        {
            "itemid": 8955124,
            "translatename": "原上草 (《楚乔传》电视剧楚乔人物曲)"
        }
    ]

    """


def addsong():
    """
    @api {post} /music/collect/addsong 收藏单曲
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 收藏单曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} itemid 单曲编号

    @apiSuccessExample {json} Success-Response:
    "Success."

    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }
    """


def delsong():
    """
    @api {post} /music/collect/delsong 取消收藏单曲
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 取消收藏单曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} itemid 单曲编号

    @apiSuccessExample {json} Success-Response:
    "Success."

    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }
    """


def getlist():
    """
    @api {post} /music/collect/getlist 获取收藏的歌单
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 获取收藏的歌单

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} playlistid 播放列表编号
    @apiSuccess (Success) {Object} playlistname 播放列表名称
    @apiSuccess (Success) {Object} imageS 小尺寸图片
    @apiSuccess (Success) {Object} imageM 中等尺寸图片
    @apiSuccess (Success) {Object} imageL 大尺寸图片

    @apiSuccessExample {json} Success-Response:
    [
        {
            "playlistid": 13676,
            "playlistname": "那些被影视主题曲偏爱的歌手们",
            "imageS": "/station/001/13676-JPG-320X320-STATION.jpg",
            "imageM": "/station/001/13676-JPG-600X600-STATION.jpg",
            "imageL": "/station/001/13676-JPG-NXN-STATION.jpg"
        }
    ]

    """


def dellist():
    """
    @api {post} /music/collect/dellist 取消收藏歌单
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 取消收藏歌单

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} selflist 自建歌单
    @apiParam (Body) {String} playlistid 播放列表编号

    @apiSuccessExample {json} Success-Response:
    "Success."

    @apiError (Error) 31013 No selflist in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No selflist in the request params!"
    }
    """


def addlist():
    """
    @api {post} /music/collect/addlist 收藏歌单
    @apiVersion 1.0.0
    @apiGroup Collect
    @apiDescription 收藏歌单

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} selflist 自建列表
    @apiParam (Body) {String} playlistid 播放列表编号

    @apiSuccessExample {json} Success-Response:
    "Success."

    @apiError (Error) 31019 UnSupport type in the request params!
    @apiError (Error) 31006 No playlist id in the request params!

    @apiErrorExample {json} Error-Response1:
    {
        "data": "No type in the request params!"
    }
    @apiErrorExample {json} Error-Response2:
    {
        "data": "No playlist id in the request params!"
    }
    """