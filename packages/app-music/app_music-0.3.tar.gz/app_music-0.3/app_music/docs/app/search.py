#! usr/bin/env python
# coding = utf-8


def hottags():
    """
    @api {post} /music/search/hottags 热门标签
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 热门标签

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} rank 等级
    @apiSuccess (Success) {Object} imagePathMap 图像路径图
    @apiSuccess (Success) {String} imagePathMap.value 图像路径图值
    @apiSuccess (Success) {String} imagePathMap.key 图像路径图键
    @apiSuccess (Success) {Object} categoryID 分类编号
    @apiSuccess (Success) {Object} description 描述
    @apiSuccess (Success) {Object} categoryType 分类类型
    @apiSuccess (Success) {Object} name 名称
    @apiSuccess (Success) {Object} categoryCode 分类代码

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "rank": 999,
                "imagePathMap": [
                    {
                        "value": "",
                        "key": "JPG-320X320-NODELIST"
                    },
                    {
                        "value": "",
                        "key": "JPG-600X600-NODELIST"
                    },
                    {
                        "value": "",
                        "key": "JPG-NXN-NODELIST"
                    }
                ],
                "categoryID": 766,
                "description": "",
                "categoryType": "CT_KV",
                "name": "中国新歌声第二季",
                "categoryCode": ""
            }
        ]
    }
    """


def assocaite():
    """
    @api {post} /music/search/associate 关键词联想匹配
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 关键词联想匹配

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词

    @apiSuccess (Success) {Int} musicNum 歌曲数量
    @apiSuccess (Success) {Int} liveNum 演唱会版数量

    @apiSuccessExample {json} Success-Response:
    {
        "data": {
            "经典老歌串烧 (live)": 1,
            "经典老歌": 1
        }
    }

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def music():
    """
    @api {post} /music/search/music 单曲搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 单曲搜索

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词
    @apiParam (Body) {String} pageSize 请求的每页所含条目数目。注意：允许最大为100，否则都按100返回

    @apiSuccess (Success) {Object} AlbumCoverL 大尺寸专辑封面图片
    @apiSuccess (Success) {Object} AlbumCoverM 中等尺寸专辑封面图片
    @apiSuccess (Success) {Object} AlbumCoverS 小尺寸专辑封面图片
    @apiSuccess (Success) {Object} AlbumID 专辑编号
    @apiSuccess (Success) {Object} AlbumName 专辑名称
    @apiSuccess (Success) {Object} ArtistID 歌手编号
    @apiSuccess (Success) {Object} ArtistName 歌手名称
    @apiSuccess (Success) {Object} ContentProviderID 版权唱片公司ID
    @apiSuccess (Success) {Object} Gender 性别
    @apiSuccess (Success) {Object} Genre 流派类型
    @apiSuccess (Success) {Object} ItemCode 单曲代码
    @apiSuccess (Success) {Object} ItemID 单曲编号
    @apiSuccess (Success) {Object} ItemType 单曲类型
    @apiSuccess (Success) {Object} LanguageType 语言类型
    @apiSuccess (Success) {Object} Name 名称
    @apiSuccess (Success) {Object} ProductID 产品编号
    @apiSuccess (Success) {Object} Rating 收听总数
    @apiSuccess (Success) {Object} RegionCode 区域代码
    @apiSuccess (Success) {Object} ReleaseDate 发布日期
    @apiSuccess (Success) {Object} StartDate 开始日期
    @apiSuccess (Success) {Object} TranslateName 翻译名称
    @apiSuccess (Success) {Object} version 版本

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "AlbumCoverL": "/album/011/116872-JPG-1000X1000-ALBUM.jpg",
                "AlbumCoverM": "/album/011/116872-JPG-600X600-ALBUM.jpg",
                "AlbumCoverS": "/album/011/116872-JPG-320X320-ALBUM.jpg",
                "AlbumID": [
                    "116872"
                ],
                "AlbumName": [
                    "下课后"
                ],
                "ArtistID": [
                    "88399"
                ],
                "ArtistName": [
                    "经典老歌"
                ],
                "ContentProviderID": 4461,
                "Gender": [
                    "group"
                ],
                "Genre": "children",
                "ItemCode": "00000000",
                "ItemID": "1209670",
                "ItemType": "ftd",
                "LanguageType": "man",
                "Name": "三字经",
                "ProductID": 1209670,
                "Rating": 2289382,
                "RegionCode": [
                    "CN"
                ],
                "ReleaseDate": "1992-01-26",
                "StartDate": "1992-01-26",
                "TranslateName": "三字经",
                "version": ""
            }
          ]
        }

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def artist():
    """
    @api {post} /music/search/artist 歌手搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 歌手搜索

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词
    @apiParam (Body) {String} pageSize 请求的每页所含条目数目。注意：允许最大为100，否则都按100返回

    @apiSuccess (Success) {Object} ArtistID 歌手编号
    @apiSuccess (Success) {Object} Gender 性别
    @apiSuccess (Success) {Object} Name 歌手名
    @apiSuccess (Success) {Object} Rating 收听总数
    @apiSuccess (Success) {Object} RegionCode 区域代号
    @apiSuccess (Success) {Object} TranslateName 翻译名称
    @apiSuccess (Success) {Object} AlbumCount 专辑数量
    @apiSuccess (Success) {Object} Birthday 生日
    @apiSuccess (Success) {Object} Blood 血型
    @apiSuccess (Success) {Object} Country 国家
    @apiSuccess (Success) {Object} Height 身高
    @apiSuccess (Success) {Object} Horoscope 星座
    @apiSuccess (Success) {Object} ItemCount 单曲数量
    @apiSuccess (Success) {Object} JPG-1000X1000-Artist 歌手图片（1000X1000）
    @apiSuccess (Success) {Object} JPG-240X240-Artist 歌手图片（240X240）
    @apiSuccess (Success) {Object} JPG-320X320-Artist 歌手图片（320X320）
    @apiSuccess (Success) {Object} JPG-600X600-Artist 歌手图片（600X600）
    @apiSuccess (Success) {Object} Weight 体重

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "ArtistID": "88399",
                "Gender": "Group",
                "Name": "经典老歌",
                "Rating": 1952167,
                "RegionCode": "CN",
                "TranslateName": "经典老歌",
                "AlbumCount": 1,
                "Birthday": "0000-00-00",
                "Blood": "N/A",
                "Country": "中国",
                "Height": 0,
                "Horoscope": "",
                "ItemCount": 1,
                "JPG-1000X1000-ARTIST": "/artist/008/88399-JPG-1000X1000-ARTIST.jpg",
                "JPG-240X240-ARTIST": "/artist/008/88399-JPG-240X240-ARTIST.jpg",
                "JPG-320X320-ARTIST": "/artist/008/88399-JPG-320X320-ARTIST.jpg",
                "JPG-600X600-ARTIST": "/artist/008/88399-JPG-600X600-ARTIST.jpg",
                "Weight": 0
            }
        ]
    }

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def album():
    """
    @api {post} /music/search/album 专辑搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 专辑搜索

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词
    @apiParam (Body) {String} pageSize 请求的每页所含条目数目。注意：允许最大为100，否则都按100返回

    @apiSuccess (Success) {Object} AlbumID 专辑编号
    @apiSuccess (Success) {Object} ArtistID 歌手编号
    @apiSuccess (Success) {Object} ArtistName 歌手名称
    @apiSuccess (Success) {Object} ContentProviderID 版权唱片公司ID
    @apiSuccess (Success) {Object} Genre 流派类型
    @apiSuccess (Success) {Object} LanguageType 语言类型
    @apiSuccess (Success) {Object} Name 名称
    @apiSuccess (Success) {Object} Price 价格
    @apiSuccess (Success) {Object} Rating 收听总数
    @apiSuccess (Success) {Object} ReleaseDate 发布日期
    @apiSuccess (Success) {Object} TranslateName 翻译名称
    @apiSuccess (Success) {Object} version 版本
    @apiSuccess (Success) {Object} JPG-1000X1000-ALBUM 专辑图片（1000X1000）
    @apiSuccess (Success) {Object} JPG-240X240-ALBUM 专辑图片（240X240）
    @apiSuccess (Success) {Object} JPG-320X320-ALBUM 专辑图片（320X320）
    @apiSuccess (Success) {Object} JPG-600X600-ALBUM 专辑图片（600X600）
    @apiSuccess (Success) {Object} NoOfTracks 声音编号


    @apiSuccessExample {json} Success-Response:
    [
    {
        "AlbumID": "116872",
        "ArtistID": "88399",
        "ArtistName": "经典老歌",
        "ContentProviderID": "4461",
        "Genre": "Children",
        "LanguageType": "MAN",
        "Name": "下课后",
        "Price": "0",
        "Rating": "1848966",
        "ReleaseDate": "1992-01-26T00:00:00Z",
        "TranslateName": "下课后",
        "version": "",
        "JPG-1000X1000-ALBUM": "/album/011/116872-JPG-1000X1000-ALBUM.jpg",
        "JPG-240X240-ALBUM": "/album/011/116872-JPG-240X240-ALBUM.jpg",
        "JPG-320X320-ALBUM": "/album/011/116872-JPG-320X320-ALBUM.jpg",
        "JPG-600X600-ALBUM": "/album/011/116872-JPG-600X600-ALBUM.jpg",
        "NoOfTracks": "1"
    }
    ]

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def list():
    """
    @api {post} /music/search/list 歌单搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 歌单搜索

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词

    @apiSuccess (Success) {Object} start 开始
    @apiSuccess (Success) {Object} docs 文档
    @apiSuccess (Success) {String} docs.Name 名称
    @apiSuccess (Success) {String} docs.GenreID 类型编号
    @apiSuccess (Success) {String} docs.StationID 专辑编号
    @apiSuccess (Success) {String} docs.Description 描述
    @apiSuccess (Success) {String} docs._version_ 版本
    @apiSuccess (Success) {String} docs.ServiceFlag 服务标志
    @apiSuccess (Success) {String} docs.GenreName 类型名称
    @apiSuccess (Success) {String} docs.CTType 热词类型
    @apiSuccess (Success) {String} docs.Author 作者
    @apiSuccess (Success) {String} docs.Attribute 属性
    @apiSuccess (Success) {String} docs.Attribute.JPG-NXN-STATION 专辑单属性图片（NXN）
    @apiSuccess (Success) {String} docs.Attribute.Description 属性描述
    @apiSuccess (Success) {String} docs.Attribute.Headline 属性标题
    @apiSuccess (Success) {String} docs.Attribute.JPG-600X600-STATION 专辑图片（600X600）
    @apiSuccess (Success) {String} docs.Attribute.AlternateDescription 属性更改描述
    @apiSuccess (Success) {String} docs.Attribute.JPG-320X320-STATION 专辑图片（320X320）
    @apiSuccess (Success) {String} docs.Attribute.AlternateHeadline 属性更改标题
    @apiSuccess (Success) {String} docs.ModifyDate 修改日期


    @apiSuccessExample {json} Success-Response:
    {
        "response": {
            "start": 0,
            "docs": [
                {
                    "Name": "老歌~时光里的玫瑰，不会枯萎",
                    "GenreID": [
                        "377",
                        "380"
                    ],
                    "StationID": "9226",
                    "Description": "80后90后都听过的经典老歌。我们一起大合唱吧！怀旧的人总爱听老歌，尽管已经都会唱了，但还是习惯偶尔翻出来听一听。",
                    "_version_": 1601801976406867968,
                    "ServiceFlag": [
                        "AT"
                    ],
                    "GenreName": [
                        "80后",
                        "90后"
                    ],
                    "CTType": "CT_SONGLIST",
                    "Author": "太滚妮呀@爱听达人",
                    "Attribute": {
                        "JPG-NXN-STATION": "/station/000/9226-20170428171507-JPG-NXN-STATION.jpeg",
                        "Description": "",
                        "Headline": "",
                        "JPG-600X600-STATION": "/station/000/9226-20170428171506-JPG-600X600-STATION.jpeg",
                        "AlternateDescription": "",
                        "JPG-320X320-STATION": "/station/000/9226-20170428171505-JPG-320X320-STATION.jpeg",
                        "AlternateHeadline": ""
                    },
                    "ModifyDate": "2017-10-11T10:19:21Z"
                }
        ]
    }

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def combine():
    """
    @api {post} /music/search/combine 综合搜索
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 综合搜索

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} searchvalue 搜索词
    @apiParam (Body) {String} pageSize 请求的每页所含条目数目。注意：允许最大为100，否则都按100返回

    @apiSuccess (Success) {Object} music 音乐
    @apiSuccess (Success) {String} music.AlbumCoverL 大尺寸专辑封面
    @apiSuccess (Success) {String} music.AlbumCoverM 中等尺寸专辑封面
    @apiSuccess (Success) {String} music.AlbumCoverS 小尺寸专辑封面
    @apiSuccess (Success) {String} music.AlbumID 专辑编号
    @apiSuccess (Success) {String} music.AlbumName 专辑名称
    @apiSuccess (Success) {String} music.ArtistID 歌手编号
    @apiSuccess (Success) {String} music.ArtistName 歌手名称
    @apiSuccess (Success) {String} music.ContentProviderID 内版权唱片公司ID
    @apiSuccess (Success) {String} music.Gender 性别
    @apiSuccess (Success) {String} music.Genre 流派类型
    @apiSuccess (Success) {String} music.ItemCode 单曲代码
    @apiSuccess (Success) {String} music.ItemID 单曲编号
    @apiSuccess (Success) {String} music.ItemType 单曲类型
    @apiSuccess (Success) {String} music.LanguageType 语言类型
    @apiSuccess (Success) {String} music.Name 名称
    @apiSuccess (Success) {String} music.ProductID 产品编号
    @apiSuccess (Success) {String} music.Rating 收听总数
    @apiSuccess (Success) {String} music.RegionCode 区域代码
    @apiSuccess (Success) {String} music.ReleaseDate 发布日期
    @apiSuccess (Success) {String} music.StartDate 开始日期
    @apiSuccess (Success) {String} music.TranslateName 翻译名称
    @apiSuccess (Success) {String} music.version 版本

    @apiSuccess (Success) {Object} Album 专辑列表
    @apiSuccess (Success) {String} Album.AlbumID 专辑编号
    @apiSuccess (Success) {String} Album.ArtistID 专辑歌手编号
    @apiSuccess (Success) {String} Album.ArtistName 专辑歌手名称
    @apiSuccess (Success) {String} Album.ContentProviderID 专辑版权唱片公司ID
    @apiSuccess (Success) {String} Album.Genre 专辑流派类型
    @apiSuccess (Success) {String} Album.LanguageType 专辑语言类型
    @apiSuccess (Success) {String} Album.Name 专辑名称
    @apiSuccess (Success) {String} Album.Price 专辑价格
    @apiSuccess (Success) {String} Album.Rating 专辑收听总数
    @apiSuccess (Success) {String} Album.ReleaseDate 专辑发布日期
    @apiSuccess (Success) {String} Album.TranslateName 专辑翻译名称
    @apiSuccess (Success) {String} Album.version 专辑版本
    @apiSuccess (Success) {String} Album.JPG-1000X1000-ALBUM 专辑专辑图片（1000X1000）
    @apiSuccess (Success) {String} Album.JPG-240X240-ALBUM 专辑专辑图片（240X240）
    @apiSuccess (Success) {String} Album.JPG-320X320-ALBUM 专辑专辑图片（320X320）
    @apiSuccess (Success) {String} Album.JPG-600X600-ALBUM 专辑专辑图片（600X600）
    @apiSuccess (Success) {String} Album.NoOfTracks 专辑声音编号

    @apiSuccess (Success) {Object} Artist 歌手列表
    @apiSuccess (Success) {String} Artist.ArtistID 歌手编号
    @apiSuccess (Success) {String} Artist.Gender 歌手流派类型
    @apiSuccess (Success) {String} Artist.Name 歌手名
    @apiSuccess (Success) {String} Artist.Rating 歌手收听总数
    @apiSuccess (Success) {String} Artist.RegionCode 歌手区域代码
    @apiSuccess (Success) {String} Artist.TranslateName 歌手翻译名称
    @apiSuccess (Success) {String} Artist.AlbumCount 歌手专辑数量
    @apiSuccess (Success) {String} Artist.Birthday 歌手生日
    @apiSuccess (Success) {String} Artist.Blood 歌手血型
    @apiSuccess (Success) {String} Artist.Country 歌手国家
    @apiSuccess (Success) {String} Artist.Height 歌手身高
    @apiSuccess (Success) {String} Artist.Horoscope 歌手星座
    @apiSuccess (Success) {String} Artist.ItemCount 歌手单曲数量
    @apiSuccess (Success) {String} Artist.JPG-1000X1000-Artist 歌手图片（1000X1000）
    @apiSuccess (Success) {String} Artist.JPG-240X240-Artist 歌手图片（240X240）
    @apiSuccess (Success) {String} Artist.JPG-320X320-Artist 歌手图片（320X320）
    @apiSuccess (Success) {String} Artist.JPG-600X600-Artist 歌手图片（600X600）
    @apiSuccess (Success) {String} Artist.Weight 体重

    @apiSuccessExample {json} Success-Response:
    {
        "music": [
            {
                "AlbumCoverL": "/album/011/116872-JPG-1000X1000-ALBUM.jpg",
                "AlbumCoverM": "/album/011/116872-JPG-600X600-ALBUM.jpg",
                "AlbumCoverS": "/album/011/116872-JPG-320X320-ALBUM.jpg",
                "AlbumID": [
                    "116872"
                ],
                "AlbumName": [
                    "下课后"
                ],
                "ArtistID": [
                    "88399"
                ],
                "ArtistName": [
                    "经典老歌"
                ],
                "ContentProviderID": 4461,
                "Gender": [
                    "group"
                ],
                "Genre": "children",
                "ItemCode": "00000000",
                "ItemID": "1209670",
                "ItemType": "ftd",
                "LanguageType": "man",
                "Name": "三字经",
                "ProductID": 1209670,
                "Rating": 2289382,
                "RegionCode": [
                    "CN"
                ],
                "ReleaseDate": "1992-01-26",
                "StartDate": "1992-01-26",
                "TranslateName": "三字经",
                "version": ""
            }
        ],
        "album": [
            {
                "AlbumID": "116872",
                "ArtistID": "88399",
                "ArtistName": "经典老歌",
                "ContentProviderID": "4461",
                "Genre": "Children",
                "LanguageType": "MAN",
                "Name": "下课后",
                "Price": "0",
                "Rating": "1848966",
                "ReleaseDate": "1992-01-26T00:00:00Z",
                "TranslateName": "下课后",
                "version": "",
                "JPG-1000X1000-ALBUM": "/album/011/116872-JPG-1000X1000-ALBUM.jpg",
                "JPG-240X240-ALBUM": "/album/011/116872-JPG-240X240-ALBUM.jpg",
                "JPG-320X320-ALBUM": "/album/011/116872-JPG-320X320-ALBUM.jpg",
                "JPG-600X600-ALBUM": "/album/011/116872-JPG-600X600-ALBUM.jpg",
                "NoOfTracks": "1"
            }
        ],
        "artist": [
            {
                "ArtistID": "88399",
                "Gender": "Group",
                "Name": "经典老歌",
                "Rating": 1952167,
                "RegionCode": "CN",
                "TranslateName": "经典老歌",
                "AlbumCount": 1,
                "Birthday": "0000-00-00",
                "Blood": "N/A",
                "Country": "中国",
                "Height": 0,
                "Horoscope": "",
                "ItemCount": 1,
                "JPG-1000X1000-ARTIST": "/artist/008/88399-JPG-1000X1000-ARTIST.jpg",
                "JPG-240X240-ARTIST": "/artist/008/88399-JPG-240X240-ARTIST.jpg",
                "JPG-320X320-ARTIST": "/artist/008/88399-JPG-320X320-ARTIST.jpg",
                "JPG-600X600-ARTIST": "/artist/008/88399-JPG-600X600-ARTIST.jpg",
                "Weight": 0
            }
        ]
    }

    @apiError (Error) 31003 No keyword in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No keyword in the request params!"
    }
    """


def gethistory():
    """
    @api {post} /music/search/gethistory 获取搜索记录
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 获取搜索记录

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiSuccess (Success) {Object} keyword 搜索关键字

    @apiSuccessExample {json} Success-Response:
    {
        "data": [
            {
                "keyword": "经典老歌"
            }
        ]
    }

    """


def clearhistory():
    """
    @api {post} /music/search/gethistory 获取搜索记录
    @apiVersion 1.0.0
    @apiGroup Search
    @apiDescription 获取搜索记录

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    """