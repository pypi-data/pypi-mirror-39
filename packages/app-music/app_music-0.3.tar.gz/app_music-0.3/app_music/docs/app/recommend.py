#! usr/bin/env python
# coding = utf-8


def dailysonglist():
    """
    @api {post} /music/recommend/dailysonglist 每日推荐
    @apiVersion 1.0.0
    @apiGroup Recommend
    @apiDescription 每日推荐

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} datainfo 数据详情
    @apiSuccess (Success) {String} datainfo.genre 流派类型
    @apiSuccess (Success) {String} datainfo.bitrates 比特率
    @apiSuccess (Success) {String} datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} datainfo.label 标签
    @apiSuccess (Success) {String} datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} datainfo.version 版本
    @apiSuccess (Success) {String} datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} datainfo.explicit 脏标
    @apiSuccess (Success) {String} datainfo.description 描述
    @apiSuccess (Success) {String} datainfo.name 歌曲名
    @apiSuccess (Success) {String} datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} datainfo.rating 评分
    @apiSuccess (Success) {String} datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} datainfo.priceCode 价格代号

    @apiSuccess (Success) {Object} artists 歌手列表
    @apiSuccess (Success) {String} artist.genre 歌手流派类型
    @apiSuccess (Success) {String} artist.region 歌手区域
    @apiSuccess (Success) {String} artist.birthday 歌手生日
    @apiSuccess (Success) {String} artist.temcount 歌手单曲数量
    @apiSuccess (Success) {String} artist.translatename 歌手翻译名称
    @apiSuccess (Success) {String} artist.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} artist.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} artist.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} artist.artistID 歌手编号
    @apiSuccess (Success) {String} artist.description 歌手描述
    @apiSuccess (Success) {String} artist.name 歌手名称
    @apiSuccess (Success) {String} artist.gender 歌手性别
    @apiSuccess (Success) {String} artist.rating 歌手收听总数
    @apiSuccess (Success) {String} artist.pinyinname 歌手拼音名称
    @apiSuccess (Success) {String} artist.albumcount 歌手专辑数量

    @apiSuccess (Success) {Object} itemID 单曲编号

    @apiSuccess (Success) {Object} album 专辑列表
    @apiSuccess (Success) {String} album.genre 专辑流派类型
    @apiSuccess (Success) {String} album.cpInfo 专辑出版公司信息
    @apiSuccess (Success) {String} album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} album.cpInfo.cpGroupName 专辑出版公司组名？
    @apiSuccess (Success) {String} album.cpInfo.cpGroupAltName 专辑出版公司组名更改名？
    @apiSuccess (Success) {String} album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} album.albumID 专辑专辑编号
    @apiSuccess (Success) {String} album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} album.version 专辑版本
    @apiSuccess (Success) {String} album.artists 专辑歌手
    @apiSuccess (Success) {String} album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} album.explicit 专辑脏标
    @apiSuccess (Success) {String} album.albumPriceCode 专辑价格代号
    @apiSuccess (Success) {String} album.name 专辑名称
    @apiSuccess (Success) {String} album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} album.rating 专辑收听总数
    @apiSuccess (Success) {String} album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} album.languagetype 专辑语言类型

    @apiSuccess (Success) {Object} itemType 单曲类型

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "datainfo": {
                    "genre": "Pop",
                    "bitrates": [
                        "FLAC-1000K-FTD",
                        "LRC-LRC",
                        "MP3-128K-FTD",
                        "MP3-192K-FTD",
                        "MP3-256K-FTD",
                        "MP3-320K-FTD"
                    ],
                    "releasedate": "2017-10-11",
                    "label": "黄色石头",
                    "exclusivity": 1,
                    "translatename": "今天雨，可是我们在一起",
                    "version": "",
                    "duration": "03:51",
                    "side": 1,
                    "explicit": 0,
                    "description": "",
                    "name": "今天雨，可是我们在一起",
                    "tracknumber": 1,
                    "rating": 367518,
                    "cpItemID": "kwm17101110091_FTD",
                    "pinyinname": "Jin Tian Yu，Ke Shi Wo Men Zai Yi Qi",
                    "languagetype": "MAN",
                    "priceCode": ""
                },
                "artists": [
                    {
                        "genre": "Pop",
                        "region": "CN",
                        "birthday": "1984-03-10",
                        "itemcount": 16,
                        "translatename": "Chris Lee",
                        "imagePathMap": [
                            {
                                "value": "/artist/001/16038-JPG-200X200-ARTIST.jpg",
                                "key": "JPG-200X200-ARTIST"
                            }
                        ],
                        "artistID": 16038,
                        "description": "李宇春（Chris Lee），1984年3月10日出生于成都，中国流行女歌手、词曲创作人、电影演员、演唱会导演。    2005年，李宇春获得“超级女声”比赛全国总冠军，10月登上美国《时代周刊》封面。2006年发行首张个人专辑《皇后与梦想》，年终销量137万张，创立品牌演唱会“WhyMe”。2007年发行第二张专辑《我的》并首次开展全国巡演，凭此再登美国《时代周刊》。2008年发行概念专辑《少年中国》，获得MTV亚洲音乐大奖中国最受欢迎歌手奖。2009年发行创作专辑《李宇春》，入驻杜莎夫人蜡像馆，获得亚洲音乐节亚洲最佳歌手奖。2010年成立个人工作室。2011年发行创作专辑《会跳舞的文艺青年》，成为第一位获得香港十大中文金曲全国最佳女歌手奖的内地歌手。2012年举行疯狂世界巡演，获得韩国MAMA亚洲最佳歌手奖。2013年凭原创作品《再不疯狂我们就老了》获得EMA欧洲音乐大奖全球最佳艺人奖。2014年发行创作专辑《1987我不知会遇见你》，获得WMA世界音乐大奖大中华区最高销量奖和APEC杰出女性奖。2015年首登央视春晚独唱个人作品《蜀绣》。2016年与经济公司约满成为独立艺人。    李宇春涉足影视，主演了《十月围城》《龙门飞甲》《血滴子》《澳门风云3》，两度入围香港金像奖最佳原创电影歌曲，凭《十月围城》获得香港导演会最佳新演员金奖及亚洲电影大奖、香港金像奖、大众电影百花奖最佳新演员提名。2013年主演赖声川话剧《如梦之梦》。2014年担任戛纳电影节颁奖嘉宾。    李宇春是玉米爱心基金终身形象代言人。",
                        "name": "李宇春",
                        "gender": "Female",
                        "rating": 12950596,
                        "pinyinname": "Li Yu Chun",
                        "albumcount": 6
                    }
                ],
                "itemID": 9708704,
                "album": {
                    "genre": "Pop",
                    "cpInfo": [
                        {
                            "contentProviderGroupID": 304,
                            "cpGroupName": "QQ",
                            "cpGroupAltName": "QQ",
                            "cpName": "黄色石头",
                            "cpCode": "黄色石头",
                            "contentProviderID": 8781
                        }
                    ],
                    "albumID": 882238,
                    "releasedate": "2017-10-11",
                    "translatename": "今天雨，可是我们在一起",
                    "version": "",
                    "artists": [
                        {
                            "artistname": "李宇春",
                            "artistID": 16038,
                            "artisttranslatename": "Chris Lee",
                            "artistpinyinname": "Li Yu Chun"
                        }
                    ],
                    "totaltrack": 1,
                    "imagePathMap": [
                        {
                            "value": "/album/088/882238-JPG-240X240-ALBUM.jpg",
                            "key": "JPG-240X240-ALBUM"
                        }
                    ],
                    "explicit": 0,
                    "albumPriceCode": -1,
                    "description": "在童话作者的故事里，雨是有魔法的。它能让一整座花园的玫瑰，瞬间绽放。\n在摄影师的镜头里，雨是有情绪的。缤纷多彩的雨伞上，它特别活跃。忽明忽暗的街灯下，它格外忧伤。\n在画家的画笔下，雨是有颜色的。海洋上空的暴风雨是黑色，融化在池塘里的是绿色，掉入情人眼里滚落出来的是蓝色。\n在李宇春的新歌里，雨是有故事的。那些静静站在雨中听她唱歌的身影；那些坐满了一整个体育场的黄色雨衣；那些湿透了全身却不减半分明媚的笑容；那些滂沱大雨都浇不灭的热情和深情。十二年的歌手生涯里到底经历过多少次大雨小雨中的演出，数字或许真的记不清楚了。但是站在舞台正中央，站在聚光灯的簇拥下，每一次看到前方迷朦雨水中一双双不停挥舞的手，那一刻弥漫心中的感动，直到写进歌里才算平静。\n\n这是李宇春十二年第一次为她亲爱的歌迷朋友们写歌，她写下了一首动人的情歌：在这颗星球上 / 我和你最特别 / 今天下着雨 / 可是我们在一起。\n不煽情，不励志，不热血，不悲伤，唱出的每一个句子都是长久以来未曾说出的心里话：可是我们在一起！\n\n作为筹备良久且备受期待的2017李宇春全新创作专辑的重磅作品之一，《今天雨，可是我们在一起》由多次与Madonna、Janet Jackson，Chris Brown等著名流行歌手合作的美国鬼才创作组合NONFICTION担纲制作，李宇春填词和演唱。“我轻轻闭眼／随微风拂面／你淡淡的笑脸／一尘也不染”这首旋律轻快迷人的浪漫舞曲，过耳不忘且朗朗上口，从创作到编曲用心且小心地避开了流行歌曲的流行套路，用领先的制作理念赋予了作品的新颖和不俗。一贯不靠炫技喧宾夺主，而是真诚诠释情感的李宇春，这一次依然献上温润诚挚的演唱。让这首悦耳的情歌，甜蜜却丝毫不矫揉造作，自然朴实却能句句动人。\n\n在2017全新专辑的概念、风格仍深藏不露之时，作为新专辑的重要收录歌曲《今天雨，可是我们在一起》先以单曲形式先于专辑面世，看似不寻常的安排，却更能体现出这首单曲的特别之处。同时也令即将登场的2017全新专辑更具期待。\n《今天雨，可是我们在一起》，送给所有“在一起”的人。\n\n这同样也是一首唱给恋人们的情歌：想和你一起漫步梧桐树下/想和你一起淋湿头发/雨声虽掩盖许多甜蜜情话/却不灭心中小小的火花。歌中扑面而来的清新甜蜜，让每一个身处爱中的人忍不住就微笑了起来。",
                    "name": "今天雨，可是我们在一起",
                    "totaldisk": 1,
                    "rating": 367519,
                    "pinyinname": "Jin Tian Yu，Ke Shi Wo Men Zai Yi Qi",
                    "languagetype": "MAN"
                },
                "itemType": "FTD"
            }
        ]
    }
    """


def list():
    """
    @api {post} /music/recommend/list 歌单推荐
    @apiVersion 1.0.0
    @apiGroup Recommend
    @apiDescription 歌单推荐

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} response 响应
    @apiSuccess (Success) {String} response.start 开始
    @apiSuccess (Success) {String} response.docs 文档
    @apiSuccess (Success) {String} response.docs.total 歌曲总数
    @apiSuccess (Success) {String} response.docs.modifydate 修改日期
    @apiSuccess (Success) {String} response.docs.imagePathMap 图像路径图
    @apiSuccess (Success) {String} response.docs.imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} response.docs.imagePathMap.key 图像路径图键
    @apiSuccess (Success) {String} response.docs.categoryID 分类编号
    @apiSuccess (Success) {String} response.docs.stations 编曲
    @apiSuccess (Success) {String} response.docs.stations.modifydate 修改日期
    @apiSuccess (Success) {String} response.docs.stations.likeCount 喜欢次数
    @apiSuccess (Success) {String} response.docs.stations.categoryID 分类编号
    @apiSuccess (Success) {String} response.docs.stations.tag 标签
    @apiSuccess (Success) {String} response.docs.stations.categoryType 分类类型
    @apiSuccess (Success) {String} response.docs.stations.categoryCode 分类代码
    @apiSuccess (Success) {String} response.docs.stations.listenCount 试听次数
    @apiSuccess (Success) {String} response.docs.stations.author 作者
    @apiSuccess (Success) {String} response.docs.stations.rank 等级
    @apiSuccess (Success) {String} response.docs.stations.imagePathMap 图像路径图
    @apiSuccess (Success) {String} response.docs.stations.imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} response.docs.stations.imagePathMap.key 图像路径图键
    @apiSuccess (Success) {String} response.docs.stations.description 描述
    @apiSuccess (Success) {String} response.docs.stations.name 名称
    @apiSuccess (Success) {String} response.docs.stations.favorivateCount 喜欢次数
    @apiSuccess (Success) {String} response.docs.description 描述
    @apiSuccess (Success) {String} response.docs.name 名称
    @apiSuccess (Success) {String} response.docs.categoryType 分类编号
    @apiSuccess (Success) {String} response.docs.categoryCode 分类代号
    @apiSuccess (Success) {String} response.docs.havemore 剩余焦点图对象数
    @apiSuccess (Success) {String} response.docs.offset 偏移量
    @apiSuccess (Success) {String} response.docs.size 文件大小
    @apiSuccess (Success) {String} response.numFound 查找数量
    @apiSuccess (Success) {Object} responseHeader 响应头
    @apiSuccess (Success) {String} responseHeader.errorinfo 错误码
    @apiSuccess (Success) {String} responseHeader.status 状态

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "response": {
                "start": 0,
                "docs": {
                    "total": 2450,
                    "modifydate": "2016-10-25",
                    "imagePathMap": [
                        {
                            "value": "",
                            "key": "JPG-320X320-GENRE"
                        }
                    ],
                    "categoryID": 8,
                    "stations": [
                        {
                            "modifydate": "2018-08-13",
                            "likeCount": 2599,
                            "categoryID": 7851,
                            "tag": "",
                            "categoryType": "CT_SONGLIST",
                            "categoryCode": "",
                            "listenCount": 15358,
                            "author": "子期如期",
                            "rank": 9,
                            "imagePathMap": [
                                {
                                    "value": "/station/000/7851-JPG-320X320-STATION.jpg",
                                    "key": "JPG-320X320-STATION"
                                }
                            ],
                            "description": "走心推荐最新单曲",
                            "name": "「头条新歌」今天雨，可是我们在一起",
                            "favorivateCount": 2436
                        }
                    ],
                    "description": "推荐歌单描述",
                    "name": "推荐歌单",
                    "categoryType": "CT_SONGLIST",
                    "categoryCode": "Genre_SongList",
                    "havemore": 2430,
                    "offset": 0,
                    "size": 20
                },
                "numFound": 1
            },
            "responseHeader": {
                "errorinfo": "",
                "status": "00"
            }
        }
    }
    """


def roewe():
    """
    @api {post} /music/recommend/roewe 荣威推荐
    @apiVersion 1.0.0
    @apiGroup Recommend
    @apiDescription 荣威推荐

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} artistID 歌手编号
    @apiSuccess (Success) {Object} artistname 歌手名称
    @apiSuccess (Success) {Object} itemID 单曲编号
    @apiSuccess (Success) {Object} albumID 专辑编号
    @apiSuccess (Success) {Object} JPG-240X240-ALBUM 歌手图片（240X240）
    @apiSuccess (Success) {Object} JPG-320X320-ALBUM 歌手图片（320X320）
    @apiSuccess (Success) {Object} JPG-600X600-ALBUM 歌手图片（600X600）
    @apiSuccess (Success) {Object} JPG-1000X1000-ALBUM 歌手图片（1000X1000）
    @apiSuccess (Success) {Object} image-pattern 图片格式
    @apiSuccess (Success) {Object} albumname 专辑名称
    @apiSuccess (Success) {Object} itemname 单曲名称

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "artistID": "33261",
                "artistname": "黄龄",
                "itemID": 8540612,
                "albumID": 737921,
                "JPG-240X240-ALBUM": "/album/073/737921-JPG-240X240-ALBUM.jpg",
                "JPG-320X320-ALBUM": "/album/073/737921-JPG-320X320-ALBUM.jpg",
                "JPG-600X600-ALBUM": "/album/073/737921-JPG-600X600-ALBUM.jpg",
                "JPG-1000X1000-ALBUM": "/album/073/737921-JPG-1000X1000-ALBUM.jpg",
                "image-pattern": "images/content/imagecache/{SIZE}/contentimages/album/073/737921-JPG-240X240-ALBUM.jpg",
                "albumname": "龙珠传奇 电视剧原声带",
                "itemname": "明珠(《龙珠传奇》电视剧片头曲)"
            }
        ]
    }
    """


def combine():
    """
    @api {post} /music/recommend/combine 综合推荐
    @apiVersion 1.0.0
    @apiGroup Recommend
    @apiDescription 综合推荐

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} dailysongs 每日歌曲
    @apiSuccess (Success) {String} dailysongs.datainfo 数据信息
    @apiSuccess (Success) {String} dailysongs.datainfo.genre 流派类型
    @apiSuccess (Success) {String} dailysongs.datainfo.bitrates 比特率
    @apiSuccess (Success) {String} dailysongs.datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} dailysongs.datainfo.label 标签
    @apiSuccess (Success) {String} dailysongs.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} dailysongs.datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} dailysongs.datainfo.version 版本
    @apiSuccess (Success) {String} dailysongs.datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} dailysongs.datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} dailysongs.datainfo.explicit 脏标
    @apiSuccess (Success) {String} dailysongs.datainfo.description 描述
    @apiSuccess (Success) {String} dailysongs.datainfo.name 名称
    @apiSuccess (Success) {String} dailysongs.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} dailysongs.datainfo.rating 收听总数
    @apiSuccess (Success) {String} dailysongs.datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} dailysongs.datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} dailysongs.datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} dailysongs.datainfo.priceCode 价格代号

    @apiSuccess (Success) {String} dailysongs.artists 歌手列表
    @apiSuccess (Success) {String} dailysongs.artists.genre 歌手流派类型
    @apiSuccess (Success) {String} dailysongs.artists.region 歌手区域
    @apiSuccess (Success) {String} dailysongs.artists.birthday 歌手生日
    @apiSuccess (Success) {String} dailysongs.artists.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} dailysongs.artists.translatename 歌手翻译名称
    @apiSuccess (Success) {String} dailysongs.artists.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} dailysongs.artists.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} dailysongs.artists.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} dailysongs.artists.artistID 歌手编号
    @apiSuccess (Success) {String} dailysongs.artists.description 歌手描述
    @apiSuccess (Success) {String} dailysongs.artists.name 歌手名称
    @apiSuccess (Success) {String} dailysongs.artists.gender 歌手性别
    @apiSuccess (Success) {String} dailysongs.artists.rating 歌手收听总数
    @apiSuccess (Success) {String} dailysongs.artists.pinyinname 歌手拼音名称
    @apiSuccess (Success) {String} dailysongs.artists.albumcount 歌手专辑数量

    @apiSuccess (Success) {String} dailysongs.itemID 单曲编号
    @apiSuccess (Success) {String} dailysongs.album 专辑列表
    @apiSuccess (Success) {String} dailysongs.album.genre 专辑流派类型
    @apiSuccess (Success) {String} dailysongs.album.cpInfo 专辑出版公司信息
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.cpGroupName 专辑出版公司组名
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.cpGroupAltName 专辑出版公司组名更改名
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} dailysongs.album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} dailysongs.album.albumID 专辑专辑编号
    @apiSuccess (Success) {String} dailysongs.album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} dailysongs.album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} dailysongs.album.version 专辑版本
    @apiSuccess (Success) {String} dailysongs.album.artists 专辑歌手
    @apiSuccess (Success) {String} dailysongs.album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} dailysongs.album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} dailysongs.album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} dailysongs.album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} dailysongs.album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} dailysongs.album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} dailysongs.album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} dailysongs.album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} dailysongs.album.explicit 专辑脏标
    @apiSuccess (Success) {String} dailysongs.album.albumPriceCode 专辑价格代号
    @apiSuccess (Success) {String} dailysongs.album.description 专辑描述
    @apiSuccess (Success) {String} dailysongs.album.name 专辑名称
    @apiSuccess (Success) {String} dailysongs.album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} dailysongs.album.rating 专辑收听总数
    @apiSuccess (Success) {String} dailysongs.album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} dailysongs.album.languagetype 专辑语言类型
    @apiSuccess (Success) {String} dailysongs.itemType 专辑单曲类型

    @apiSuccess (Success) {Object} list 列表

    @apiSuccess (Success) {Object} list.response 响应
    @apiSuccess (Success) {String} list.response.start 开始
    @apiSuccess (Success) {String} list.response.docs 响应文档
    @apiSuccess (Success) {String} list.response.docs.total 歌曲总数
    @apiSuccess (Success) {String} list.response.docs.modifydate 修改日期
    @apiSuccess (Success) {String} list.response.docs.imagePathMap 图像路径图
    @apiSuccess (Success) {String} list.response.docs.imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} list.response.docs.imagePathMap.key 图像路径图键
    @apiSuccess (Success) {String} list.response.docs.stations 专辑
    @apiSuccess (Success) {String} list.response.docs.stations.modifydate 修改日期
    @apiSuccess (Success) {String} list.response.docs.stations.likeCount 喜欢次数
    @apiSuccess (Success) {String} list.response.docs.stations.categoryID 分类编号
    @apiSuccess (Success) {String} list.response.docs.stations.tag 标签
    @apiSuccess (Success) {String} list.response.docs.stations.categoryType 分类类型
    @apiSuccess (Success) {String} list.response.docs.stations.categoryCode 分类代号
    @apiSuccess (Success) {String} list.response.docs.stations.listenCount 试听次数
    @apiSuccess (Success) {String} list.response.docs.stations.author 作者
    @apiSuccess (Success) {String} list.response.docs.stations.rank 等级
    @apiSuccess (Success) {String} list.response.docs.stations.imagePathMap 图像路径图
    @apiSuccess (Success) {String} list.response.docs.stations.imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} list.response.docs.stations.imagePathMap.key 图像路径图键
    @apiSuccess (Success) {String} list.response.docs.stations.description 描述
    @apiSuccess (Success) {String} list.response.docs.stations.name 名称
    @apiSuccess (Success) {String} list.response.docs.stations.favorivateCount 喜欢次数？单词拼错了？

    @apiSuccess (Success) {String} list.response.docs.categoryID 分类编号
    @apiSuccess (Success) {String} list.response.docs.description 描述
    @apiSuccess (Success) {String} list.response.docs.categoryType 分类类型
    @apiSuccess (Success) {String} list.response.docs.name 名称
    @apiSuccess (Success) {String} list.response.docs.categoryCode 分类代号
    @apiSuccess (Success) {String} list.response.docs.havemore 剩余焦点图对象数
    @apiSuccess (Success) {String} list.response.docs.offset 偏移量
    @apiSuccess (Success) {String} list.response.docs.size 文件大小

    @apiSuccess (Success) {String} list.responseHeader 响应
    @apiSuccess (Success) {String} list.responseHeader.errorinfo 错误码
    @apiSuccess (Success) {String} list.responseHeader.status 状态

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "dailysongs": [
                {
                    "datainfo": {
                        "genre": "Pop",
                        "bitrates": [
                            "FLAC-1000K-FTD",
                            "LRC-LRC",
                            "MP3-128K-FTD",
                            "MP3-192K-FTD",
                            "MP3-256K-FTD",
                            "MP3-320K-FTD"
                        ],
                        "releasedate": "2017-10-11",
                        "label": "黄色石头",
                        "exclusivity": 1,
                        "translatename": "今天雨，可是我们在一起",
                        "version": "",
                        "duration": "03:51",
                        "side": 1,
                        "explicit": 0,
                        "description": "",
                        "name": "今天雨，可是我们在一起",
                        "tracknumber": 1,
                        "rating": 367518,
                        "cpItemID": "kwm17101110091_FTD",
                        "pinyinname": "Jin Tian Yu，Ke Shi Wo Men Zai Yi Qi",
                        "languagetype": "MAN",
                        "priceCode": ""
                    },
                    "artists": [
                        {
                            "genre": "Pop",
                            "region": "CN",
                            "birthday": "1984-03-10",
                            "itemcount": 16,
                            "translatename": "Chris Lee",
                            "imagePathMap": [
                                {
                                    "value": "/artist/001/16038-JPG-200X200-ARTIST.jpg",
                                    "key": "JPG-200X200-ARTIST"
                                }
                            ],
                            "artistID": 16038,
                            "description": "李宇春（Chris Lee），1984年3月10日出生于成都，中国流行女歌手、词曲创作人、电影演员、演唱会导演。    2005年，李宇春获得“超级女声”比赛全国总冠军，10月登上美国《时代周刊》封面。2006年发行首张个人专辑《皇后与梦想》，年终销量137万张，创立品牌演唱会“WhyMe”。2007年发行第二张专辑《我的》并首次开展全国巡演，凭此再登美国《时代周刊》。2008年发行概念专辑《少年中国》，获得MTV亚洲音乐大奖中国最受欢迎歌手奖。2009年发行创作专辑《李宇春》，入驻杜莎夫人蜡像馆，获得亚洲音乐节亚洲最佳歌手奖。2010年成立个人工作室。2011年发行创作专辑《会跳舞的文艺青年》，成为第一位获得香港十大中文金曲全国最佳女歌手奖的内地歌手。2012年举行疯狂世界巡演，获得韩国MAMA亚洲最佳歌手奖。2013年凭原创作品《再不疯狂我们就老了》获得EMA欧洲音乐大奖全球最佳艺人奖。2014年发行创作专辑《1987我不知会遇见你》，获得WMA世界音乐大奖大中华区最高销量奖和APEC杰出女性奖。2015年首登央视春晚独唱个人作品《蜀绣》。2016年与经济公司约满成为独立艺人。    李宇春涉足影视，主演了《十月围城》《龙门飞甲》《血滴子》《澳门风云3》，两度入围香港金像奖最佳原创电影歌曲，凭《十月围城》获得香港导演会最佳新演员金奖及亚洲电影大奖、香港金像奖、大众电影百花奖最佳新演员提名。2013年主演赖声川话剧《如梦之梦》。2014年担任戛纳电影节颁奖嘉宾。    李宇春是玉米爱心基金终身形象代言人。",
                            "name": "李宇春",
                            "gender": "Female",
                            "rating": 12950596,
                            "pinyinname": "Li Yu Chun",
                            "albumcount": 6
                        }
                    ],
                    "itemID": 9708704,
                    "album": {
                        "genre": "Pop",
                        "cpInfo": [
                            {
                                "contentProviderGroupID": 304,
                                "cpGroupName": "QQ",
                                "cpGroupAltName": "QQ",
                                "cpName": "黄色石头",
                                "cpCode": "黄色石头",
                                "contentProviderID": 8781
                            }
                        ],
                        "albumID": 882238,
                        "releasedate": "2017-10-11",
                        "translatename": "今天雨，可是我们在一起",
                        "version": "",
                        "artists": [
                            {
                                "artistname": "李宇春",
                                "artistID": 16038,
                                "artisttranslatename": "Chris Lee",
                                "artistpinyinname": "Li Yu Chun"
                            }
                        ],
                        "totaltrack": 1,
                        "imagePathMap": [
                            {
                                "value": "/album/088/882238-JPG-240X240-ALBUM.jpg",
                                "key": "JPG-240X240-ALBUM"
                            }
                        ],
                        "explicit": 0,
                        "albumPriceCode": -1,
                        "description": "在童话作者的故事里，雨是有魔法的。它能让一整座花园的玫瑰，瞬间绽放。\n在摄影师的镜头里，雨是有情绪的。缤纷多彩的雨伞上，它特别活跃。忽明忽暗的街灯下，它格外忧伤。\n在画家的画笔下，雨是有颜色的。海洋上空的暴风雨是黑色，融化在池塘里的是绿色，掉入情人眼里滚落出来的是蓝色。\n在李宇春的新歌里，雨是有故事的。那些静静站在雨中听她唱歌的身影；那些坐满了一整个体育场的黄色雨衣；那些湿透了全身却不减半分明媚的笑容；那些滂沱大雨都浇不灭的热情和深情。十二年的歌手生涯里到底经历过多少次大雨小雨中的演出，数字或许真的记不清楚了。但是站在舞台正中央，站在聚光灯的簇拥下，每一次看到前方迷朦雨水中一双双不停挥舞的手，那一刻弥漫心中的感动，直到写进歌里才算平静。\n\n这是李宇春十二年第一次为她亲爱的歌迷朋友们写歌，她写下了一首动人的情歌：在这颗星球上 / 我和你最特别 / 今天下着雨 / 可是我们在一起。\n不煽情，不励志，不热血，不悲伤，唱出的每一个句子都是长久以来未曾说出的心里话：可是我们在一起！\n\n作为筹备良久且备受期待的2017李宇春全新创作专辑的重磅作品之一，《今天雨，可是我们在一起》由多次与Madonna、Janet Jackson，Chris Brown等著名流行歌手合作的美国鬼才创作组合NONFICTION担纲制作，李宇春填词和演唱。“我轻轻闭眼／随微风拂面／你淡淡的笑脸／一尘也不染”这首旋律轻快迷人的浪漫舞曲，过耳不忘且朗朗上口，从创作到编曲用心且小心地避开了流行歌曲的流行套路，用领先的制作理念赋予了作品的新颖和不俗。一贯不靠炫技喧宾夺主，而是真诚诠释情感的李宇春，这一次依然献上温润诚挚的演唱。让这首悦耳的情歌，甜蜜却丝毫不矫揉造作，自然朴实却能句句动人。\n\n在2017全新专辑的概念、风格仍深藏不露之时，作为新专辑的重要收录歌曲《今天雨，可是我们在一起》先以单曲形式先于专辑面世，看似不寻常的安排，却更能体现出这首单曲的特别之处。同时也令即将登场的2017全新专辑更具期待。\n《今天雨，可是我们在一起》，送给所有“在一起”的人。\n\n这同样也是一首唱给恋人们的情歌：想和你一起漫步梧桐树下/想和你一起淋湿头发/雨声虽掩盖许多甜蜜情话/却不灭心中小小的火花。歌中扑面而来的清新甜蜜，让每一个身处爱中的人忍不住就微笑了起来。",
                        "name": "今天雨，可是我们在一起",
                        "totaldisk": 1,
                        "rating": 367519,
                        "pinyinname": "Jin Tian Yu，Ke Shi Wo Men Zai Yi Qi",
                        "languagetype": "MAN"
                    },
                    "itemType": "FTD"
                }
            ],
            "list": {
                "response": {
                    "start": 0,
                    "docs": {
                        "total": 2450,
                        "modifydate": "2016-10-25",
                        "imagePathMap": [
                            {
                                "value": "",
                                "key": "JPG-320X320-GENRE"
                            }
                        ],
                        "stations": [
                            {
                                "modifydate": "2018-08-13",
                                "likeCount": 2599,
                                "categoryID": 7851,
                                "tag": "",
                                "categoryType": "CT_SONGLIST",
                                "categoryCode": "",
                                "listenCount": 15358,
                                "author": "子期如期",
                                "rank": 9,
                                "imagePathMap": [
                                    {
                                        "value": "/station/000/7851-JPG-320X320-STATION.jpg",
                                        "key": "JPG-320X320-STATION"
                                    }
                                ],
                                "description": "走心推荐最新单曲",
                                "name": "「头条新歌」今天雨，可是我们在一起",
                                "favorivateCount": 2436
                            }
                        ],
                        "categoryID": 8,
                        "description": "推荐歌单描述",
                        "categoryType": "CT_SONGLIST",
                        "name": "推荐歌单",
                        "categoryCode": "Genre_SongList",
                        "havemore": 2430,
                        "offset": 0,
                        "size": 20
                    },
                    "numFound": 1
                },
                "responseHeader": {
                    "errorinfo": "",
                    "status": "00"
                }
            }
        }
    }
    """