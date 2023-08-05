#! usr/bin/env python
# coding = utf-8


def getplaylist():
    """
    @api {post} /music/playlist/getplaylist 获取用户歌单
    @apiVersion 1.0.0
    @apiGroup Playlist
    @apiDescription 获取用户歌单

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
    {
        "data": [
            {
                "playlistid": 1,
                "playlistname": "我的列表",
                "imageS": null,
                "imageM": null,
                "imageL": null
            }
        ]
    }

    """


def getplaylistcontent():
    """
    @api {post} /music/playlist/getplaylistcontent 获取用户歌单内容
    @apiVersion 1.0.0
    @apiGroup Playlist
    @apiDescription 获取用户歌单内容

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} itemid 单曲编号
    @apiSuccess (Success) {Object} translatename 翻译名称

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "itemid": 9546550,
                "translatename": "Be Your Light (电视剧「隧道」片尾曲)"
            }
        ]
    }

    @apiError (Error) 31006 No playlist id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No playlist id in the request params!"
    }

    """


def add():
    """
    @api {post} /music/playlist/add 增加单曲
    @apiVersion 1.0.0
    @apiGroup Playlist
    @apiDescription 增加单曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} playlistid 播放列表编号
    @apiParam (Body) {String} itemid 单曲编号

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Received"
    }

    @apiError (Error) 31006 No playlist id in the request params!
    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response1:
    {
        "data": "No playlist id in the request params!"
    }

    @apiErrorExample {json} Error-Response2:
    {
        "data": "No item id in the request params!"
    }
    """


def delete():
    """
    @api {post} /music/playlist/delete 删除单曲
    @apiVersion 1.0.0
    @apiGroup Playlist
    @apiDescription 删除单曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} playlistid 播放列表编号
    @apiParam (Body) {String} itemid 单曲编号

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Received"
    }

    @apiError (Error) 31006 No playlist id in the request params!
    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response1:
    {
        "data": "No playlist id in the request params!"
    }

    @apiErrorExample {json} Error-Response2:
    {
        "data": "No item id in the request params!"
    }

    """


def create():
    """
    @api {post} /music/playlist/create 创建用户歌单
    @apiVersion 1.0.0
    @apiGroup Playlist
    @apiDescription 创建用户歌单

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} playlistname 播放列表名称

    @apiSuccess (Success) {Object} playlistid 播放列表编号

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "playlistid": 230
        }
    }

    @apiError (Error) 31012 No playlist id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No playlistname in the request params!"
    }

    """