#! usr/bin/env python
# coding = utf-8


def artistinfo():
    """
    @api {post} /music/moreinfo/artistinfo 请求歌手信息
    @apiVersion 1.0.0
    @apiGroup More
    @apiDescription 请求歌手信息

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} artistid 歌手编号

    @apiSuccess (Success) {Object} response 响应
    @apiSuccess (Success) {String} response.start 开始
    @apiSuccess (Success) {String} response.docs 响应文档

    @apiSuccess (Success) {String} response.docs.datainfo 数据信息
    @apiSuccess (Success) {String} response.docs.datainfo.genre 流派类型
    @apiSuccess (Success) {String} response.docs.datainfo.bitrates 比特率
    @apiSuccess (Success) {String} response.docs.datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} response.docs.datainfo.label 标签
    @apiSuccess (Success) {String} response.docs.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} response.docs.datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} response.docs.datainfo.version 版本
    @apiSuccess (Success) {String} response.docs.datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} response.docs.datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} response.docs.datainfo.explicit 脏标
    @apiSuccess (Success) {String} response.docs.datainfo.description 描述
    @apiSuccess (Success) {String} response.docs.datainfo.name 名称
    @apiSuccess (Success) {String} response.docs.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} response.docs.datainfo.rating 收听总数
    @apiSuccess (Success) {String} response.docs.datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} response.docs.datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} response.docs.datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} response.docs.datainfo.priceCode 价格代号

    @apiSuccess (Success) {String} response.docs.artists 歌手列表
    @apiSuccess (Success) {String} response.docs.artists.genre 歌手流派类型
    @apiSuccess (Success) {String} response.docs.artists.region 歌手区域
    @apiSuccess (Success) {String} response.docs.artists.birthday 歌手生日
    @apiSuccess (Success) {String} response.docs.artists.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} response.docs.artists.translatename 歌手翻译名称
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} response.docs.artists.artistID 歌手编号
    @apiSuccess (Success) {String} response.docs.artists.description 歌手描述
    @apiSuccess (Success) {String} response.docs.artists.name 歌手名称
    @apiSuccess (Success) {String} response.docs.artists.gender 歌手性别
    @apiSuccess (Success) {String} response.docs.artists.rating 收听总数
    @apiSuccess (Success) {String} response.docs.artists.pinyinname 歌手拼音名称
    @apiSuccess (Success) {String} response.docs.artists.albumcount 歌手专辑数量

    @apiSuccess (Success) {String} response.docs.itemID 单曲编号列表

    @apiSuccess (Success) {String} response.docs.album 专辑列表
    @apiSuccess (Success) {String} response.docs.album.genre 专辑流派类型
    @apiSuccess (Success) {String} response.docs.album.cpInfo 专辑出版公司信息
    @apiSuccess (Success) {String} response.docs.album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpGroupName 专辑出版公司组名
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpGroupAltName 专辑出版公司组名更改名
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} response.docs.album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} response.docs.album.albumID 专辑编号
    @apiSuccess (Success) {String} response.docs.album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} response.docs.album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} response.docs.album.version 专辑版本
    @apiSuccess (Success) {String} response.docs.album.artists 专辑歌手
    @apiSuccess (Success) {String} response.docs.album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} response.docs.album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} response.docs.album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} response.docs.album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} response.docs.album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} response.docs.album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} response.docs.album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} response.docs.album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} response.docs.album.explicit 专辑脏标
    @apiSuccess (Success) {String} response.docs.album.albumPriceCode 专辑价格代号
    @apiSuccess (Success) {String} response.docs.album.description 专辑描述
    @apiSuccess (Success) {String} response.docs.album.name 专辑名称
    @apiSuccess (Success) {String} response.docs.album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} response.docs.album.rating 专辑收听总数
    @apiSuccess (Success) {String} response.docs.album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} response.docs.album.languagetype 专辑语言类型
    @apiSuccess (Success) {String} response.docs.itemType 单曲类型
    @apiSuccess (Success) {String} musicinfo.numFound 查找数

    @apiSuccess (Success) {Object} responseHeader 响应头
    @apiSuccess (Success) {String} responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} responseHeader.status 状态


    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "response": {
                "start": 0,
                "docs": [
                    {
                        "datainfo": {
                            "genre": "Pop",
                            "bitrates": [
                                "LRC-LRC",
                                "MP3-128K-FTD",
                                "MP3-192K-FTD",
                                "MP3-256K-FTD",
                                "MP3-320K-FTD"
                            ],
                            "releasedate": "2012-02-20",
                            "label": "海蝶音乐",
                            "exclusivity": 10,
                            "translatename": "唱响世界",
                            "version": "",
                            "duration": "04:39",
                            "side": 1,
                            "explicit": 0,
                            "description": "",
                            "name": "唱响世界",
                            "tracknumber": 1,
                            "rating": 42399,
                            "cpItemID": "GDOBX0920089_FTD",
                            "pinyinname": "Chang Xiang Shi Jie",
                            "languagetype": "MAN",
                            "priceCode": ""
                        },
                        "artists": [
                            {
                                "genre": "Pop",
                                "region": "SG",
                                "birthday": "1981-08-17",
                                "itemcount": 13,
                                "translatename": "Hong Jun Yang",
                                "imagePathMap": [
                                    {
                                        "value": "/artist/001/16121-JPG-240X240-ARTIST.jpg",
                                        "key": "JPG-240X240-ARTIST"
                                    }
                                ],
                                "artistID": 16121,
                                "description": "洪俊扬，1981年8月17日出生，毕业于新加坡国立大学(National University of Singapore)，2006年5月26日发行第一张专辑《独角兽》。2010年2月1日，洪俊扬与杜蕙甹举行婚礼。",
                                "name": "洪俊扬",
                                "gender": "Male",
                                "rating": 33882,
                                "pinyinname": "Hong Jun Yang",
                                "albumcount": 2
                            }
                        ],
                        "itemID": 66664,
                        "album": {
                            "genre": "Pop",
                            "cpInfo": [
                                {
                                    "contentProviderGroupID": 33,
                                    "cpGroupName": "海蝶音乐",
                                    "cpGroupAltName": "海蝶音乐",
                                    "cpName": "海蝶音乐",
                                    "cpCode": "海蝶音乐",
                                    "contentProviderID": 4456
                                }
                            ],
                            "albumID": 11399,
                            "releasedate": "2012-02-20",
                            "translatename": "海蝶夯之唱响世界",
                            "version": "",
                            "artists": [
                                {
                                    "artistname": "华语群星",
                                    "artistID": 94146,
                                    "artisttranslatename": "华语群星",
                                    "artistpinyinname": "Hua Yu Qun Xing"
                                }
                            ],
                            "totaltrack": 30,
                            "imagePathMap": [
                                {
                                    "value": "/album/001/11399-JPG-240X240-ALBUM.jpg",
                                    "key": "JPG-240X240-ALBUM"
                                }
                            ],
                            "explicit": 0,
                            "albumPriceCode": -1,
                            "name": "海蝶夯之唱响世界",
                            "totaldisk": 2,
                            "rating": 964491,
                            "pinyinname": "Hai Die Ben Zhi Chang Xiang Shi Jie",
                            "languagetype": "MAN"
                        },
                        "itemType": "FTD"
                    },
                ],
                "numFound": 2
            },
            "responseHeader": {
                "errorinfo": "",
                "status": "00"
            }
        }
    }

    @apiError (Error) 31014 No artist id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No artist id in the request params!"
    }
    """


def albuminfo():
    """
    @api {post} /music/moreinfo/albuminfo 专辑信息
    @apiVersion 1.0.0
    @apiGroup More
    @apiDescription 专辑信息

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} albumid 歌手编号

    @apiSuccess (Success) {Object} response 响应
    @apiSuccess (Success) {String} response.start 开始
    @apiSuccess (Success) {String} response.docs 响应文档

    @apiSuccess (Success) {String} response.docs.datainfo 数据信息
    @apiSuccess (Success) {String} response.docs.datainfo.genre 流派类型
    @apiSuccess (Success) {String} response.docs.datainfo.bitrates 比特率
    @apiSuccess (Success) {String} response.docs.datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} response.docs.datainfo.label 标签
    @apiSuccess (Success) {String} response.docs.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} response.docs.datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} response.docs.datainfo.version 版本
    @apiSuccess (Success) {String} response.docs.datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} response.docs.datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} response.docs.datainfo.explicit 脏标
    @apiSuccess (Success) {String} response.docs.datainfo.description 描述
    @apiSuccess (Success) {String} response.docs.datainfo.name 名称
    @apiSuccess (Success) {String} response.docs.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} response.docs.datainfo.rating 收听总数
    @apiSuccess (Success) {String} response.docs.datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} response.docs.datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} response.docs.datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} response.docs.datainfo.priceCode 价格代号

    @apiSuccess (Success) {String} response.docs.artists 歌手列表
    @apiSuccess (Success) {String} response.docs.artists.genre 歌手流派类型
    @apiSuccess (Success) {String} response.docs.artists.region 歌手区域
    @apiSuccess (Success) {String} response.docs.artists.birthday 歌手生日
    @apiSuccess (Success) {String} response.docs.artists.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} response.docs.artists.translatename 歌手翻译名称
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} response.docs.artists.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} response.docs.artists.artistID 歌手编号
    @apiSuccess (Success) {String} response.docs.artists.description 歌手描述
    @apiSuccess (Success) {String} response.docs.artists.name 歌手名称
    @apiSuccess (Success) {String} response.docs.artists.gender 歌手性别
    @apiSuccess (Success) {String} response.docs.artists.rating 歌手收听总数
    @apiSuccess (Success) {String} response.docs.artists.pinyinname 歌手拼音名称
    @apiSuccess (Success) {String} response.docs.artists.albumcount 歌手专辑数量

    @apiSuccess (Success) {String} response.docs.itemID 单曲编号

    @apiSuccess (Success) {String} response.docs.album 专辑列表
    @apiSuccess (Success) {String} response.docs.album.genre 专辑流派类型
    @apiSuccess (Success) {String} response.docs.album.cpInfo 专辑出版公司信息
    @apiSuccess (Success) {String} response.docs.album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpGroupName 专辑出版公司组名
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpGroupAltName 专辑出版公司组名更改名
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} response.docs.album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} response.docs.album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} response.docs.album.albumID 专辑专辑编号
    @apiSuccess (Success) {String} response.docs.album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} response.docs.album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} response.docs.album.version 专辑版本
    @apiSuccess (Success) {String} response.docs.album.artists 专辑歌手
    @apiSuccess (Success) {String} response.docs.album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} response.docs.album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} response.docs.album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} response.docs.album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} response.docs.album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} response.docs.album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} response.docs.album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} response.docs.album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} response.docs.album.explicit 专辑脏标
    @apiSuccess (Success) {String} response.docs.album.albumPriceCode 专辑专辑价格代号
    @apiSuccess (Success) {String} response.docs.album.description 专辑描述
    @apiSuccess (Success) {String} response.docs.album.name 专辑名称
    @apiSuccess (Success) {String} response.docs.album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} response.docs.album.rating 专辑收听总数
    @apiSuccess (Success) {String} response.docs.album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} response.docs.album.languagetype 专辑语言类型
    @apiSuccess (Success) {String} response.docs.itemType 单曲类型
    @apiSuccess (Success) {String} musicinfo.numFound 查找数

    @apiSuccess (Success) {Object} responseHeader 响应头
    @apiSuccess (Success) {String} responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} responseHeader.status 状态


    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "response": {
                "start": 0,
                "docs": [
                    {
                        "datainfo": {
                            "genre": "Pop",
                            "bitrates": [
                                "LRC-LRC",
                                "MP3-128K-FTD",
                                "MP3-192K-FTD",
                                "MP3-256K-FTD",
                                "MP3-320K-FTD"
                            ],
                            "releasedate": "2010-10-22",
                            "label": "杰威尔音乐",
                            "exclusivity": 1,
                            "translatename": "阿爸",
                            "version": "",
                            "duration": "04:28",
                            "side": 1,
                            "explicit": 0,
                            "description": "",
                            "name": "阿爸",
                            "tracknumber": 1,
                            "rating": 105681,
                            "cpItemID": "GDJVR1203201_FTD",
                            "pinyinname": "A Ba",
                            "languagetype": "TWN",
                            "priceCode": ""
                        },
                        "artists": [
                            {
                                "genre": "Pop",
                                "region": "TW",
                                "birthday": "1963-03-26",
                                "itemcount": 242,
                                "translatename": "Hung Jung",
                                "imagePathMap": [
                                    {
                                        "value": "/artist/004/46822-JPG-200X200-ARTIST.jpg",
                                        "key": "JPG-200X200-ARTIST"
                                    }
                                ],
                                "artistID": 46822,
                                "description": "洪荣宏，Hung,Jung(1963～)，中国台湾地区知名艺人、主持人和歌手，台语歌坛“低音歌王”洪一峰的长子。其闽南语歌曲脍炙人口，曾横扫台湾的各个角落，是在沈文程后较早的台语歌手，1991、1993、1996获得3次金曲奖最佳台语男歌手奖，是1990-2013年间获得金曲奖最佳台语男歌手奖次数最多的男歌手，1990年获得金曲奖最佳国语男歌手奖。为台语歌曲在台湾音乐界地位的确立有重要的贡献。\n洪荣宏发表声明已于2013年8月份与前妻陈施羽协议离婚。",
                                "name": "洪荣宏",
                                "gender": "Male",
                                "rating": 331611,
                                "pinyinname": "Hong Rong Hong",
                                "albumcount": 22
                            }
                        ],
                        "itemID": 488319,
                        "album": {
                            "genre": "Pop",
                            "cpInfo": [
                                {
                                    "contentProviderGroupID": 707,
                                    "cpGroupName": "杰威尔音乐",
                                    "cpGroupAltName": "杰威尔音乐",
                                    "cpName": "杰威尔音乐",
                                    "cpCode": "杰威尔音乐",
                                    "contentProviderID": 6157
                                }
                            ],
                            "albumID": 55090,
                            "releasedate": "2010-10-22",
                            "translatename": "阿爸",
                            "version": "",
                            "artists": [
                                {
                                    "artistname": "周杰伦",
                                    "artistID": 6478,
                                    "artisttranslatename": "Jay Chou",
                                    "artistpinyinname": "Zhou Jie Lun"
                                }
                            ],
                            "totaltrack": 1,
                            "imagePathMap": [
                                {
                                    "value": "/album/005/55090-JPG-240X240-ALBUM.jpg",
                                    "key": "JPG-240X240-ALBUM"
                                }
                            ],
                            "explicit": 0,
                            "albumPriceCode": -1,
                            "name": "阿爸",
                            "totaldisk": 1,
                            "rating": 62792,
                            "pinyinname": "A Ba",
                            "languagetype": "TWN"
                        },
                        "itemType": "FTD"
                    }
                ],
                "numFound": 1
            },
            "responseHeader": {
                "errorinfo": "",
                "status": "00"
            }
        }
    }

    @apiError (Error) 31007 No album id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No album id in the request params!"
    }
    """


def listinfo():
    """
    @api {post} /music/moreinfo/listinfo 歌单信息
    @apiVersion 1.0.0
    @apiGroup More
    @apiDescription 歌单信息

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} categoryid 分类编号

    @apiSuccess (Success) {Object} response 响应
    @apiSuccess (Success) {String} response.start 开始
    @apiSuccess (Success) {String} response.docs 响应文档

    @apiSuccess (Success) {String} response.docs.total 歌曲总数
    @apiSuccess (Success) {String} response.docs.modifydate 修改日期
    @apiSuccess (Success) {String} response.docs.likeCount 喜欢次数
    @apiSuccess (Success) {String} response.docs.categoryID 分类编号
    @apiSuccess (Success) {String} response.docs.tag 标签
    @apiSuccess (Success) {String} response.docs.categoryType 分类类型
    @apiSuccess (Success) {String} response.docs.categoryCode 分类代号
    @apiSuccess (Success) {String} response.docs.havemore 剩余焦点图对象数
    @apiSuccess (Success) {String} response.docs.listenCount 试听次数
    @apiSuccess (Success) {String} response.docs.size 文件大小
    @apiSuccess (Success) {String} response.docs.author 作者
    @apiSuccess (Success) {String} response.docs.rank 等级
    @apiSuccess (Success) {String} response.docs.imagePathMap 图像路径图
    @apiSuccess (Success) {String} response.docs.imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} response.docs.imagePathMap.key 图像路径图键
    @apiSuccess (Success) {String} response.docs.description 描述
    @apiSuccess (Success) {String} response.docs.name 名称

    @apiSuccess (Success) {String} response.docs.stationItems 专辑单曲列表
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo 信息
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.genre 流派类型
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.bitrates 比特率
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.label 标签
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.version 版本
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.duration 歌曲时长
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.explicit 脏标
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.description 描述
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.name 名称
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.rating 收听总数
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.cpItemID 出版商单曲编号
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.pinyinname 拼音名称
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} response.docs.stationItems.datainfo.priceCode 价格代号

    @apiSuccess (Success) {String} response.docs.stationItems.artists 歌手列表
    @apiSuccess (Success) {String} response.docs.stationItems.artists.genre 歌手流派类型
    @apiSuccess (Success) {String} response.docs.stationItems.artists.region 歌手区域
    @apiSuccess (Success) {String} response.docs.stationItems.artists.birthday 歌手生日
    @apiSuccess (Success) {String} response.docs.stationItems.artists.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} response.docs.stationItems.artists.translatename 歌手翻译名称
    @apiSuccess (Success) {String} response.docs.stationItems.artists.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} response.docs.stationItems.artists.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} response.docs.stationItems.artists.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} response.docs.stationItems.artists.artistID 歌手编号
    @apiSuccess (Success) {String} response.docs.stationItems.artists.description 歌手描述
    @apiSuccess (Success) {String} response.docs.stationItems.artists.name 歌手名称
    @apiSuccess (Success) {String} response.docs.stationItems.artists.gender 歌手性别
    @apiSuccess (Success) {String} response.docs.stationItems.artists.rating 歌手收听总数
    @apiSuccess (Success) {String} response.docs.stationItems.artists.pinyinname 歌手拼音姓名
    @apiSuccess (Success) {String} response.docs.stationItems.artists.albumcount 歌手专辑数量

    @apiSuccess (Success) {String} response.docs.stationItems.itemID 单曲编号

    @apiSuccess (Success) {String} response.docs.stationItems.imagePath 图片路径

    @apiSuccess (Success) {String} response.docs.stationItems.description 描述

    @apiSuccess (Success) {String} response.docs.stationItems.album 专辑列表
    @apiSuccess (Success) {String} response.docs.stationItems.album.genre 专辑流派类型
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo 专辑出版商信息
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.cpGroupName 专辑出版公司组名
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.cpGroupAltName 专辑出版公司组名更改名
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} response.docs.stationItems.album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} response.docs.stationItems.album.albumID 专辑专辑编号
    @apiSuccess (Success) {String} response.docs.stationItems.album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} response.docs.stationItems.album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.version 专辑版本
    @apiSuccess (Success) {String} response.docs.stationItems.album.artists 专辑歌手
    @apiSuccess (Success) {String} response.docs.stationItems.album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} response.docs.stationItems.album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} response.docs.stationItems.album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} response.docs.stationItems.album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} response.docs.stationItems.album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} response.docs.stationItems.album.explicit 专辑排他性
    @apiSuccess (Success) {String} response.docs.stationItems.album.albumPriceCode 专辑价格代号
    @apiSuccess (Success) {String} response.docs.stationItems.album.description 专辑描述
    @apiSuccess (Success) {String} response.docs.stationItems.album.name 专辑名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} response.docs.stationItems.album.rating 专辑收听总数
    @apiSuccess (Success) {String} response.docs.stationItems.album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} response.docs.stationItems.album.languagetype 专辑语言类型

    @apiSuccess (Success) {String} response.docs.stationItems.itemType 单曲类型

    @apiSuccess (Success) {String} response.docs.offset 偏移量

    @apiSuccess (Success) {String} response.docs.favorivateCount 喜欢数量

    @apiSuccess (Success) {String} response.numFound 查找数量

    @apiSuccess (Success) {Object} responseHeader 响应头
    @apiSuccess (Success) {String} responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} responseHeader.status 状态


    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "response": {
                "start": 0,
                "docs": {
                    "total": 4,
                    "modifydate": "2018-06-22",
                    "likeCount": 1324,
                    "categoryID": 2,
                    "tag": "",
                    "categoryType": "CT_SUBJECT",
                    "categoryCode": "ST_Subject_2",
                    "havemore": 0,
                    "listenCount": 11734,
                    "size": 4,
                    "author": "爱听站长",
                    "rank": 3,
                    "imagePathMap": [
                        {
                            "value": "/station/000/2-JPG-320X320-STATION.jpg",
                            "key": "JPG-320X320-STATION"
                        }
                    ],
                    "description": "奥斯卡百年",
                    "name": "奥斯卡百年",
                    "stationItems": [
                        {
                            "datainfo": {
                                "genre": "Pop",
                                "bitrates": [
                                    "LRC-LRC",
                                    "MP3-128K-FTD",
                                    "MP3-192K-FTD",
                                    "MP3-256K-FTD",
                                    "MP3-320K-FTD"
                                ],
                                "releasedate": "2000-05-02",
                                "label": "Columbia",
                                "exclusivity": 1,
                                "translatename": "Things Have Changed",
                                "version": "",
                                "duration": "05:08",
                                "side": 1,
                                "explicit": 0,
                                "description": "",
                                "name": "Things Have Changed",
                                "tracknumber": 1,
                                "rating": 49569,
                                "cpItemID": "2202629_FTD",
                                "pinyinname": "Things Have Changed",
                                "languagetype": "ENG",
                                "priceCode": ""
                            },
                            "artists": [
                                {
                                    "genre": "Pop",
                                    "region": "US",
                                    "birthday": "1941-5-24",
                                    "itemcount": 4497,
                                    "translatename": "鲍勃·迪伦",
                                    "imagePathMap": [
                                        {
                                            "value": "/artist/000/2303-JPG-240X240-ARTIST.jpg",
                                            "key": "JPG-240X240-ARTIST"
                                        }
                                    ],
                                    "artistID": 2303,
                                    "description": "Bob Dylan 的原名是Robert Allen Zi-mmerman，1941年5月24日生于明尼苏达州的杜勒斯（Duluth），6 岁时全家移居到一个叫希宾（Hibbing）的靠近矿区的小镇上，少年时期的Dylan 只不过是一个喜爱音乐的平凡男孩，对乡村乐感兴趣。1961年1月，Bob Dylan从明尼苏达州立大学辍学，开始专心致力于歌唱工作，并来到纽约Cate Wha 民谣音乐城（Folk City）和煤气灯（Gaslight）等著名的表演场所演出。由于 Dylan的民谣歌曲受到知识分子的喜爱与",
                                    "name": "Bob Dylan",
                                    "gender": "Male",
                                    "rating": 1362949,
                                    "pinyinname": "Bob Dylan",
                                    "albumcount": 275
                                }
                            ],
                            "itemID": 721799,
                            "imagePath": "",
                            "description": "",
                            "album": {
                                "genre": "Pop",
                                "cpInfo": [
                                    {
                                        "contentProviderGroupID": 52,
                                        "cpGroupName": "索尼音乐",
                                        "cpGroupAltName": "索尼音乐",
                                        "cpName": "Columbia",
                                        "cpCode": "Columbia",
                                        "contentProviderID": 3755
                                    }
                                ],
                                "albumID": 73511,
                                "releasedate": "2000-05-02",
                                "translatename": "Best Of Bob Dylan, Vol. 2",
                                "version": "",
                                "artists": [
                                    {
                                        "artistname": "Bob Dylan",
                                        "artistID": 2303,
                                        "artisttranslatename": "鲍勃·迪伦",
                                        "artistpinyinname": "Bob Dylan"
                                    }
                                ],
                                "totaltrack": 17,
                                "imagePathMap": [
                                    {
                                        "value": "/album/007/73511-JPG-240X240-ALBUM.jpg",
                                        "key": "JPG-240X240-ALBUM"
                                    }
                                ],
                                "explicit": 0,
                                "albumPriceCode": -1,
                                "description": "",
                                "name": "Best Of Bob Dylan, Vol. 2",
                                "totaldisk": 1,
                                "rating": 45068,
                                "pinyinname": "Best Of Bob Dylan, Vol. 2",
                                "languagetype": "ENG"
                            },
                            "itemType": "FTD"
                        }
                    ],
                    "offset": 0,
                    "favorivateCount": 1296
                },
                "numFound": 1
            },
            "responseHeader": {
                "errorinfo": "",
                "status": "00"
            }
        }
    }

    @apiError (Error) 31015 No categoryid id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No categoryid id in the request params!"
    }
    """


def lyric():
    """
    @api {post} /music/moreinfo/lyric 歌词信息
    @apiVersion 1.0.0
    @apiGroup More
    @apiDescription 歌词信息

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} itemid 歌手编号

    @apiSuccess (Success) {Object} response 响应
    @apiSuccess (Success) {String} response.start 开始
    @apiSuccess (Success) {String} response.docs 响应文档
    @apiSuccess (Success) {String} response.docs.itemID 单曲编号
    @apiSuccess (Success) {String} response.docs.filenameext 文件名称后缀
    @apiSuccess (Success) {String} response.docs.subitemtype 子项类型
    @apiSuccess (Success) {String} response.docs.url 网址
    @apiSuccess (Success) {String} response.numFound 查找次数

    @apiSuccess (Success) {Object} responseHeader 响应头
    @apiSuccess (Success) {String} responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} responseHeader.status 状态

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "response": {
                "start": 0,
                "docs": {
                    "itemID": 9354103,
                    "filenameext": "lrc",
                    "subitemtype": "LRC-LRC",
                    "url": "http://lyric.97ting.com/lyric/09/354/9354103-LRC-LRC.lrc"
                },
                "numFound": 1
            },
            "responseHeader": {
                "errorinfo": "",
                "status": "00"
            }
        }
    }

    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }

    """