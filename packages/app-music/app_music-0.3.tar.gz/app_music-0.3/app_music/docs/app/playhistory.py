#! usr/bin/env python
# coding = utf-8


def get():
    """
    @api {post} /music/playhistory/get 获取播放历史记录
    @apiVersion 1.0.0
    @apiGroup Playhistory
    @apiDescription 获取播放历史记录

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} itemid 单曲编号
    @apiSuccess (Success) {Object} translatename 翻译名称
    @apiSuccess (Success) {Object} favorite 最爱

    @apiSuccessExample {json} Success-Response:
    [
        {
            "itemid": 1505006,
            "translatename": "Sam歌",
            "favorite": null
        }
    ]
    """


def clear():
    """
    @api {post} /music/playhistory/clear 清空历史记录
    @apiVersion 1.0.0
    @apiGroup Playhistory
    @apiDescription 清空历史记录

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccessExample {json} Success-Response:
    {
        "data": "Success."
    }

    """