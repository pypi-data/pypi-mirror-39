#! usr/bin/env python
# coding = utf-8


def playlist():
    """
    @api {post} /music/flaclist/playlist 热门标签
    @apiVersion 1.0.0
    @apiGroup Apelist
    @apiDescription 热门标签

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} datainfo 数据详情列表
    @apiSuccess (Success) {String} datainfo.genre 流派类型
    @apiSuccess (Success) {String} datainfo.bitrates 比特率
    @apiSuccess (Success) {String} datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} datainfo.label 标签
    @apiSuccess (Success) {String} datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）

    @apiSuccess (Success) {String} datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} datainfo.version 版本
    @apiSuccess (Success) {String} datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} datainfo.explicit 脏标？
    @apiSuccess (Success) {String} datainfo.description 描述
    @apiSuccess (Success) {String} datainfo.name 歌曲名
    @apiSuccess (Success) {String} datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} datainfo.rating 收听总数
    @apiSuccess (Success) {String} datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} datainfo.priceCode 价格代号

    @apiSuccess (Success) {Object} artists 歌手列表
    @apiSuccess (Success) {String} artist.genre 歌手流派类型
    @apiSuccess (Success) {String} artist.region 歌手区域
    @apiSuccess (Success) {String} artist.birthday 歌手生日
    @apiSuccess (Success) {String} artist.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} artist.translatename 歌手翻译名称
    @apiSuccess (Success) {String} artist.imagePathMap 歌手图像路径图？
    @apiSuccess (Success) {String} artist.imagePathMap.value 歌手图像路径图值？
    @apiSuccess (Success) {String} artist.imagePathMap.key 歌手图像路径图键？
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
    @apiSuccess (Success) {String} album.cpInfo.contentProviderGroupID 版权唱片公司分组编号？
    @apiSuccess (Success) {String} album.cpInfo.cpGroupName 出版公司组名？
    @apiSuccess (Success) {String} album.cpInfo.cpGroupAltName 出版公司组名更改名？
    @apiSuccess (Success) {String} album.cpInfo.cpName 出版公司名称
    @apiSuccess (Success) {String} album.cpInfo.cpCode 出版公司代号
    @apiSuccess (Success) {String} album.cpInfo.contentProviderID 版权唱片公司ID
    @apiSuccess (Success) {String} album.albumID 专辑编号
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
                    "releasedate": "2014-12-26",
                    "label": "杰威尔音乐",
                    "exclusivity": 1,
                    "translatename": "天涯过客",
                    "version": "",
                    "duration": "04:13",
                    "side": 1,
                    "explicit": 0,
                    "description": "",
                    "name": "天涯过客",
                    "tracknumber": 4,
                    "rating": 257221,
                    "cpItemID": "m2015032713435_FTD",
                    "pinyinname": "Tian Ya Guo Ke",
                    "languagetype": "MAN",
                    "priceCode": ""
                },
                "artists": [
                    {
                        "genre": "Pop",
                        "region": "TW",
                        "birthday": "1979-01-18",
                        "itemcount": 415,
                        "translatename": "Jay Chou",
                        "imagePathMap": [
                            {
                                "value": "/artist/000/6478-PNG-100X100-ARTIST.png",
                                "key": "PNG-100X100-ARTIST"
                            }
                        ],
                        "artistID": 6478,
                        "description": "周杰伦（Jay Chou），1979年1月18日出生在台湾新北市，身兼华语男歌手、词曲创作人、制作人、导演、编剧、监制等。2000年发行首张专辑《Jay》出道，2002年在中国、新加坡、马来西亚、美国等地举办首场世界巡回演唱会。2003年登美国《时代周刊》封面人物。曾四次获得世界音乐大奖中国最畅销艺人奖，并凭借专辑《Jay》《范特西》《叶惠美》《跨时代》四次获金曲奖最佳国语专辑奖，又通过《魔杰座》《跨时代》两度获得金曲奖最佳男歌手奖。2014年、2015年两度获得QQ音乐年度盛典最佳全能艺人奖。2015年获得全球华语榜中榜亚洲最受欢迎全能艺人奖；同年担任《中国好声音第四季》导师。2005年以电影《头文字D》获台湾电影金马奖及香港电影金像奖最佳新人奖。2007年成立杰威尔有限公司，自编自导电影《不能说的秘密》获台湾电影金马奖年度杰出电影奖。2009年入选美国CNN亚洲极具影响力人物，2011年主演好莱坞电影《青蜂侠》进军国际，获美国MTV电影大奖最佳新人提名。2012年登福布斯中国名人榜榜首。2013年自编自导电影《天台爱情》获选纽约电影节闭幕片。2014年加盟好莱坞电影《惊天魔盗团2》。2015年监制电影《一万公里的约定》。演艺事业外，2011年担任华硕笔电设计师并入股香港文化传信集团。2012年开设真爱范特西连锁KTV。2013年受邀北京大学演讲。2016年个人品牌MRJ电商上市。除了个人事业外，周杰伦还热心慈善，多次向内地灾区捐款并募款新建希望小学。",
                        "name": "周杰伦",
                        "gender": "Male",
                        "rating": 91272320,
                        "pinyinname": "Zhou Jie Lun",
                        "albumcount": 38
                    }
                ],
                "itemID": 1247543,
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
                    "albumID": 122072,
                    "releasedate": "2014-12-26",
                    "translatename": "哎呦，不错哦",
                    "version": "",
                    "artists": [
                        {
                            "artistname": "周杰伦",
                            "artistID": 6478,
                            "artisttranslatename": "Jay Chou",
                            "artistpinyinname": "Zhou Jie Lun"
                        }
                    ],
                    "totaltrack": 12,
                    "imagePathMap": [
                        {
                            "value": "images/content/imagecache/{SIZE}/contentimages/album/012/122072-JPG-240X240-ALBUM.jpg",
                            "key": "image-pattern"
                        }
                    ],
                    "explicit": 0,
                    "albumPriceCode": -1,
                    "name": "哎呦，不错哦",
                    "totaldisk": 1,
                    "rating": 3213089,
                    "pinyinname": "Ai Yo，Bu Cuo O",
                    "languagetype": "MAN"
                },
                "itemType": "FTD"
            }
        ]
    }
    """


def playurl():
    """
    @api {post} /music/flaclist/playurl 播放歌曲
    @apiVersion 1.0.0
    @apiGroup Apelist
    @apiDescription 播放歌曲

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} itemid 单曲编号

    @apiSuccess (Success) {Object} file 文件
    @apiSuccess (Success) {String} file.response 响应
    @apiSuccess (Success) {String} file.response.start 开始
    @apiSuccess (Success) {String} file.response.docs 响应文档
    @apiSuccess (Success) {String} file.response.docs.fileExtension 文件扩展名
    @apiSuccess (Success) {String} file.response.docs.fileSize 文件大小
    @apiSuccess (Success) {String} file.response.docs.dailydlcount 每日下载数量
    @apiSuccess (Success) {String} file.response.docs.orderid 订阅编号
    @apiSuccess (Success) {String} file.response.docs.url 响应网址
    @apiSuccess (Success) {String} file.response.docs.monthlydlcount 每月下载数量
    @apiSuccess (Success) {String} file.response.numFound 查找量
    @apiSuccess (Success) {String} file.responseHeader 响应头
    @apiSuccess (Success) {String} file.responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} file.responseHeader.status 状态

    @apiSuccess (Success) {Object} musicinfo 音乐信息
    @apiSuccess (Success) {String} musicinfo.response 响应
    @apiSuccess (Success) {String} musicinfo.response.start 开始
    @apiSuccess (Success) {String} musicinfo.response.docs 响应文档
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo 音乐数据信息
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.genre 音乐流派类型
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.bitrates 音乐比特率
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.releasedate 音乐发布日期
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.label 音乐标签
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.translatename 音乐翻译名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.version 音乐版本
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.duration 音乐歌曲长度
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.side 音乐歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.explicit 音乐脏标
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.description 音乐描述
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.name 音乐名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.rating 音乐收听总数
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.cpItemID 音乐出版公司单曲编号
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.languagetype 音乐语言类型
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.priceCode 音乐价格代号
    @apiSuccess (Success) {String} musicinfo.response.docs.artists 歌手列表
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.genre 歌手流派类型
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.region 歌手区域
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.birthday 歌手生日
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.itemcount 歌手单曲数量
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.translatename 歌手翻译名称
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.imagePathMap 歌手图像路径图
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.imagePathMap.value 歌手图像路径图值
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.imagePathMap.key 歌手图像路径图键
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.artistID 歌手编号
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.description 歌手描述
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.name 歌手名称
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.gender 歌手性别
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.rating 歌手收听总数
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.pinyinname 歌手拼音名称
    @apiSuccess (Success) {String} musicinfo.response.docs.artists.albumcount 歌手专辑数量
    @apiSuccess (Success) {String} musicinfo.response.docs.itemID 单曲编号
    @apiSuccess (Success) {String} musicinfo.response.docs.album 专辑列表
    @apiSuccess (Success) {String} musicinfo.response.docs.album.genre 专辑流派类型
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo 专辑出版公司信息
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.contentProviderGroupID 专辑版权唱片公司分组编号
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.cpGroupName 专辑出版公司组名
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.cpGroupAltName 专辑出版公司组名更改名
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.cpName 专辑出版公司名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.cpCode 专辑出版公司代号
    @apiSuccess (Success) {String} musicinfo.response.docs.album.cpInfo.contentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} musicinfo.response.docs.album.albumID 专辑编号
    @apiSuccess (Success) {String} musicinfo.response.docs.album.releasedate 专辑发布日期
    @apiSuccess (Success) {String} musicinfo.response.docs.album.translatename 专辑翻译名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.version 专辑版本
    @apiSuccess (Success) {String} musicinfo.response.docs.album.artists 专辑歌手
    @apiSuccess (Success) {String} musicinfo.response.docs.album.artists.artistname 专辑歌手名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.artists.artistID 专辑歌手编号
    @apiSuccess (Success) {String} musicinfo.response.docs.album.artists.artisttranslatename 专辑歌手翻译名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.artists.artistpinyinname 专辑歌手拼音名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.totaltrack 专辑总声音数量
    @apiSuccess (Success) {String} musicinfo.response.docs.album.imagePathMap 专辑图像路径图
    @apiSuccess (Success) {String} musicinfo.response.docs.album.imagePathMap.value 专辑图像路径图值
    @apiSuccess (Success) {String} musicinfo.response.docs.album.imagePathMap.key 专辑图像路径图键
    @apiSuccess (Success) {String} musicinfo.response.docs.album.explicit 专辑脏标
    @apiSuccess (Success) {String} musicinfo.response.docs.album.albumPriceCode 专辑价格代号
    @apiSuccess (Success) {String} musicinfo.response.docs.album.description 专辑描述
    @apiSuccess (Success) {String} musicinfo.response.docs.album.name 专辑名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.totaldisk 专辑总磁盘
    @apiSuccess (Success) {String} musicinfo.response.docs.album.rating 专辑收听总数
    @apiSuccess (Success) {String} musicinfo.response.docs.album.pinyinname 专辑拼音名称
    @apiSuccess (Success) {String} musicinfo.response.docs.album.languagetype 专辑语言类型
    @apiSuccess (Success) {String} musicinfo.response.docs.itemType 单曲类型
    @apiSuccess (Success) {String} musicinfo.response.numFound 查找数
    @apiSuccess (Success) {String} musicinfo.responseHeader 响应头
    @apiSuccess (Success) {String} musicinfo.responseHeader.errorinfo 错误信息
    @apiSuccess (Success) {String} musicinfo.responseHeader.status 状态

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "file": {
                "response": {
                    "start": 0,
                    "docs": {
                        "fileExtension": "flac",
                        "fileSize": 16432015,
                        "dailydlcount": 0,
                        "orderid": "5290ddccfa47538709dea449d90ca6ef",
                        "url": "http://ksy.97ting.com/content/08/955/8955124-FLAC-1000K-FTD.flac?wsSecret=74aaf369c670131bbdd15610ed46c3ac&wsTime=5b753183&transDeliveryCode=SH@23111334@1534234243@S@",
                        "monthlydlcount": 0
                    },
                    "numFound": 1
                },
                "responseHeader": {
                    "errorinfo": "",
                    "status": "00"
                }
            },
            "musicinfo": {
                "response": {
                    "start": 0,
                    "docs": [
                        {
                            "datainfo": {
                                "genre": "Soundtrack",
                                "bitrates": [
                                    "FLAC-1000K-FTD",
                                    "LRC-LRC",
                                    "MP3-128K-FTD",
                                    "MP3-192K-FTD",
                                    "MP3-256K-FTD",
                                    "MP3-320K-FTD"
                                ],
                                "releasedate": "2017-07-11",
                                "label": "北京听见时代娱乐传媒有限公司",
                                "exclusivity": 1,
                                "translatename": "原上草 (《楚乔传》电视剧楚乔人物曲)",
                                "version": "",
                                "duration": "03:05",
                                "side": 1,
                                "explicit": 0,
                                "description": "",
                                "name": "原上草 (《楚乔传》电视剧楚乔人物曲)",
                                "tracknumber": 1,
                                "rating": 1344972,
                                "cpItemID": "kwm17071110051_FTD",
                                "pinyinname": "Yuan Shang Cao (《Chu Qiao Chuan》Dian Shi Ju Chu Qiao Ren Wu Qu)",
                                "languagetype": "MAN",
                                "priceCode": ""
                            },
                            "artists": [
                                {
                                    "genre": "Pop",
                                    "region": "CN",
                                    "birthday": "1988-04-30",
                                    "itemcount": 29,
                                    "translatename": "Sara",
                                    "imagePathMap": [
                                        {
                                            "value": "/artist/008/81742-JPG-240X240-ARTIST.jpg",
                                            "key": "JPG-240X240-ARTIST"
                                        }
                                    ],
                                    "artistID": 81742,
                                    "description": "刘惜君，1988年4月30日出生于深圳，中国流行女歌手、音乐制作人。毕业于星海音乐学院流行音乐系2006级本科班。\n    2004年推出首支单曲《贝壳风铃》。2006年演唱了《梅艳芳菲》主题曲《不必再怀念我》，并受邀录制罗比·威廉姆斯歌曲《Better Man》混音版。2007年发行首张EP《Sara刘惜君》。2009年获“快乐女声”全国五强。\n    2010年发行首张专辑《爱情花园》，《我很快乐》被广为传唱。2011年专辑《拂晓》首担音乐制作人，获得音乐先锋榜内地最受欢迎女歌手。2012年以专辑《惜·君》致敬偶像邓丽君，并出任2014年纪念邓丽君演唱会形象大使。2015年11月11日，发行暌违乐坛三年的全新专辑《当我身边空无一人》。2016年为《女医·明妃传》献唱片尾曲《直到那一天》。\n    演艺事业外，刘惜君热心公益慈善。2010年举行刘惜君“音乐·源泉”Live音乐会，所得收入全部捐给西南旱区；同年11月26日在俄罗斯圣彼得堡“全球虎保护高峰会议”上，作为唯一一位受邀的中国女歌手登台献唱。",
                                    "name": "刘惜君",
                                    "gender": "Female",
                                    "rating": 9552290,
                                    "pinyinname": "Liu Xi Jun",
                                    "albumcount": 9
                                }
                            ],
                            "itemID": 8955124,
                            "album": {
                                "genre": "Soundtrack",
                                "cpInfo": [
                                    {
                                        "contentProviderGroupID": 131,
                                        "cpGroupName": "北京听见时代娱乐传媒有限公司",
                                        "cpGroupAltName": "北京听见时代娱乐传媒有限公司",
                                        "cpName": "北京听见时代娱乐传媒有限公司",
                                        "cpCode": "北京听见时代娱乐传媒有限公司",
                                        "contentProviderID": 8576
                                    }
                                ],
                                "albumID": 788151,
                                "releasedate": "2017-07-11",
                                "translatename": "原上草",
                                "version": "",
                                "artists": [
                                    {
                                        "artistname": "刘惜君",
                                        "artistID": 81742,
                                        "artisttranslatename": "Sara",
                                        "artistpinyinname": "Liu Xi Jun"
                                    }
                                ],
                                "totaltrack": 1,
                                "imagePathMap": [
                                    {
                                        "value": "/album/078/788151-JPG-240X240-ALBUM.jpg",
                                        "key": "JPG-240X240-ALBUM"
                                    }
                                ],
                                "explicit": 0,
                                "albumPriceCode": -1,
                                "description": "不负理想 不灭信仰\n烈焰燎原 烧不灭希望\n这信念 千年回响\n特工皇妃楚乔传·楚乔人物曲\n刘惜君【原上草】压轴敬献\n听青春·见热血\n听见时代传媒携手好莱坞国际团队联袂打造\n\n夏季未央，信仰之声涌动四方，震慑心灵最深处。2017听见时代传媒联袂国际音乐大师、携手好莱坞黄金幕后音乐团队共同打造电视剧《特工皇妃楚乔传》楚乔人物曲《原上草》今日正式发布。这首歌曲由美国作曲家陈雪燃（Xueran Chen）作曲、知名词人林乔填词，实力唱将刘惜君献声，歌曲从更深度层面清晰解读主人公楚乔传奇人生，不仅有励志燃血的“如野草滋长，冲破土壤，只为一线阳光，纵战火未央，烈焰燎原，烧不灭希望”的心灵之声，也有“有多少对抗，彼此心伤，何日比翼飞翔”这样转身后的无奈与期待，歌曲不仅仅让神一般的“秀丽王”精神得以体现，更揭开了楚乔作为女子“普通人”的一面。本次听见时代亦突破华语原声风格局限，特别以好莱坞电影音乐的磅礴曲式及制作模式，邀请到美国NEM Studios、匈牙利Budapest Art Orchestra交响乐团，Budapest Art Choir合唱团等国际优秀音乐团队参与制作，歌曲后期制作均在美国洛杉矶完成。作为实力派歌者，刘惜君本次以超凡的声线发挥给予了这首《原上草》别样的“东方魅力”，恰到好处的冷静演绎，潜移默化间将剧集画面植入到这首歌曲中。\n《特工皇妃楚乔传》是由慈文传媒旗下蜜淘影业、华策影视集团克顿传媒旗下上海辛迪加影视有限公司联合出品，根据潇湘冬儿所著小说《11处特工皇妃》改编，吴锦源执导，赵丽颖、林更新、窦骁、李沁领衔主演，邓伦、金士杰特邀出演，王彦霖、牛骏峰、黄梦莹、田小洁、孙宁、金瀚、邢昭林、陈圆媛等联合出演的古装传奇剧。剧集讲述了天下战乱、一个特立独行的女奴楚乔，在协助建立新政权过程中关于守护、背叛、信仰、爱情的故事。该剧于2017年6月5日在湖南卫视“青春进行时”剧场播出。\n继《夏有乔木雅望天堂》、《微微一笑很倾城》、《夏至未至》原声大碟之后，听见时代再度企划《特工皇妃楚乔传》原声燃曲，以“听青春·见热血”为概念，邀请中国香港90后音乐小天后G.E.M.邓紫棋、内地实力派唱将刘惜君震撼发声。听见时代出品人宋鹏飞表示：“楚乔她不只是追逐信仰、顽强抵抗不公的‘神’，她也会像常人一样，在风起云涌过后也有疼痛、悲伤和对于爱的渴望。所以《原上草》这首歌曲格局要更大一些，覆盖的心境也要更广一些。也谢谢惜君非常好的演绎，让我们感受到了楚乔的心声”。",
                                "name": "原上草",
                                "totaldisk": 1,
                                "rating": 1344973,
                                "pinyinname": "Yuan Shang Cao",
                                "languagetype": "MAN"
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
    }

    @apiError (Error) 31011 No item id in the request params

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }
    """