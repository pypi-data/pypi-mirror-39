#! usr/bin/env python
# coding = utf-8


def music():
    """
    @api {post} /music/play/music 单曲信息
    @apiVersion 1.0.0
    @apiGroup Play
    @apiDescription 单曲信息

    @apiParam (Headers) {string} token 令牌
    @apiParam (Headers) {String} device_token 设备令牌
    @apiParam (Headers) {String} content_type 内容类型
    @apiParam (Headers) {String} timestamp 时间戳

    @apiParam (Body) {String} itemid 单曲编号

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
    @apiSuccess (Success) {String} response.docs.datainfo.rating 评分
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
    @apiSuccess (Success) {String} response.docs.itemType 专辑单曲类型
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
                                "FLAC-1000K-FTD",
                                "LRC-LRC",
                                "MP3-128K-FTD",
                                "MP3-192K-FTD",
                                "MP3-256K-FTD",
                                "MP3-320K-FTD"
                            ],
                            "releasedate": "2017-10-05",
                            "label": "福茂唱片",
                            "exclusivity": 1,
                            "translatename": "Be Your Light (电视剧「隧道」片尾曲)",
                            "version": "",
                            "duration": "05:19",
                            "side": 1,
                            "explicit": 0,
                            "description": "",
                            "name": "Be Your Light (电视剧「隧道」片尾曲)",
                            "tracknumber": 1,
                            "rating": 13373,
                            "cpItemID": "kwm17092810411_FTD",
                            "pinyinname": "Be Your Light (Dian Shi Ju「Sui Dao」Pian Wei Qu)",
                            "languagetype": "MAN",
                            "priceCode": ""
                        },
                        "artists": [
                            {
                                "genre": "Pop",
                                "region": "TW",
                                "birthday": "1989-7-7",
                                "itemcount": 89,
                                "translatename": "Bii",
                                "imagePathMap": [
                                    {
                                        "value": "/artist/005/54130-JPG-200X200-ARTIST.jpg",
                                        "key": "JPG-200X200-ARTIST"
                                    }
                                ],
                                "artistID": 54130,
                                "description": "  毕书尽（Bii \\ 필서진），1989年7月7日出生于韩国首尔，中国台湾籍流行男歌手。\n2006年由父亲友人推荐给老鹰音乐公司创办人李亚明的赏识而签约成为旗下练习生。2010年7月发行首张EP《Bii》出道；同年10月6日发行首张专辑《Bii Story》，凭借专辑歌曲《转身之后》乐坛走红。2013年5月发行第二张个人专辑《Come back to Bii》，凭借专辑歌曲《Come Back To Me》入选第4届全球流行音乐金榜年度20大金曲与Hit Fm联播网年度电台点播冠军奖。2014年6月获得“2014Hito流行音乐奖”之Hito潜力男歌手奖；同年11月获得第19届新加坡金曲奖之舞台魅力奖。",
                                "name": "毕书尽",
                                "gender": "Male",
                                "rating": 2215800,
                                "pinyinname": "Bi Shu Jin",
                                "albumcount": 20
                            }
                        ],
                        "itemID": 9546550,
                        "album": {
                            "genre": "Pop",
                            "cpInfo": [
                                {
                                    "contentProviderGroupID": 30,
                                    "cpGroupName": "福茂唱片",
                                    "cpGroupAltName": "福茂唱片",
                                    "cpName": "福茂唱片",
                                    "cpCode": "福茂唱片",
                                    "contentProviderID": 4453
                                }
                            ],
                            "albumID": 869035,
                            "releasedate": "2017-10-05",
                            "translatename": "Bii Your Light",
                            "version": "",
                            "artists": [
                                {
                                    "artistname": "毕书尽",
                                    "artistID": 54130,
                                    "artisttranslatename": "Bii",
                                    "artistpinyinname": "Bi Shu Jin"
                                }
                            ],
                            "totaltrack": 10,
                            "imagePathMap": [
                                {
                                    "value": "/album/086/869035-JPG-240X240-ALBUM.jpg",
                                    "key": "JPG-240X240-ALBUM"
                                }
                            ],
                            "explicit": 0,
                            "albumPriceCode": -1,
                            "description": "我是光\n投射你的每一道光\n渴望相遇 渴望相爱\n\n你是光\n反射我的每一道光\n互相辉映 互相补偿\n\n2017.10.05 I’ll Be Your Light 老鹰制作 福茂发行\n\nBii毕书尽睽违一年发行个人第五张全新专辑【Bii Your Light】，卸下华丽的武装回归音乐本质，拿出他最厉害的武器，用歌声攻占华语乐坛，一向给人忧郁王子印象的Bii毕书尽，不再只是单方面的接收大家给予的关爱，如今的他已经有能力作为别人的光芒，带给他人温暖与希望，如同这次专辑光的概念，不单单只是歌迷一直以来为他照明方向，而是交由他带领着大家前行，象是恒星般的照亮自己也照亮身旁的人相互依存着。\n\n发行四张专辑后，Bii毕书尽与公司一直在寻找如何突破以往形象的作品，这次集结了各方菁英，由金曲歌后蔡健雅x JerryC x陈君豪x黄宣铭x格莱美混音大师Ken Lewis，摄影大师邵亭魁x金曲设计大师颜伯骏，天王天后御用造型师王鸿志（小小）齐心打造，摆脱过往的既定印象，造型以简单又不失时尚的睡衣为主轴，打破旧规颠覆创意新思维，不添加过度华丽的包装，更衬托Bii毕书尽独特气质，也让大众更零距离接触Bii毕书尽最真实的样貌，希望大家着重在他的音乐和歌声上。\n在新专辑发行之前，Bii毕书尽陆续推出三首不同曲风的音乐作品，从第一首裸视自身状态的【You’re Gone】到第二首失去歌唱便一无所有的【Nothing At All】和第三首正能量爆发的【Be Your Light】，都一一展现Bii毕书尽在音乐上的无限潜能，新专辑首波强打【我想你了】毕式情歌再进化，撕裂般的深情呼唤，煽动人心止不住想念的泪水，原来最残忍的爱情，是你离开后还遗留下的痕迹，思念处处暗潮汹涌的侵袭独留下来的我。\n\n2017老鹰音乐年度大事，Bii毕书尽在万众期盼之下宣布年底12/9进攻台北小巨蛋，举办他个人首场小巨蛋演唱会【天堂M Bii毕书尽My Best Moment】，门票更在首卖当天3分钟内完售开出大红盘，Bii毕书尽表示：非常感谢大家对他的支持，演唱会当天一定会把最好的一面展现出来，绝对会让大家值回票价。\n\n2017/10/05老鹰制作 福茂发行\n\n曲序：\n1.\tBe Your Light/电视剧「隧道」片尾曲\n2.\tYou’re Gone/电视剧「噗通噗通我爱你」片尾曲\n3.\tNothing At All/电视剧「守护者K2」片头曲\n4.\tMy Girl \n5.\t蛋/电视剧「噗通噗通我爱你」插曲\n6.\t爱你就够了/电视剧「噗通噗通我爱你」插曲\n7.\tRed n’ Hot\n8.\tLet’s Drunk \n9.\t我想你了/电视剧「1%可能性」片尾曲\n10.\t在你的世界\n\n歌曲介绍：\n--Be Your Light—\n大气恢弘的一首能量系抒情摇滚主打，由第28届金曲奖最佳编曲人提名/最佳制作人陈君豪操刀编曲，海洋般深邃的琴音带入温柔坚定的呢喃，多层次和声铺排环绕，如置身宇宙天地之间的舒坦辽阔，撼动心窝的鼓击声响，如拂晓透窗般乍现，毕书尽招牌厚实的假音冲破阻碍，随着摇滚乐队倾斜而出，引领着群众的吶喊振奋人心，曲末突变切换的EDM曲风更是一绝，令人耳目一新的混搭巧思，也呈现了「光」的多元面貌概念，无论是黑夜闪烁的星光，床头温暖的月光，穿透云层曙光，专注所爱的目光，相信只要是「光」一定会灿烂的，I’ll be your light，每个黑暗时刻，为了你存活，I’ll be your light，每个回首时刻，陪在你身后。\n\n--You’re Gone—\n由金曲歌后蔡健雅量身作曲，制作人陈又齐填词，赤裸刻划出毕书尽内心世界的深度省思作品，诚恳不造作的木吉他弹奏，似唸似唱的呢喃嗓音，娓娓道出一路走来的颠簸与刻骨，象是休止符一般，渴望偶尔停驻，却又不得不前行的矛盾自缚。也许这一刻功成名就，停留在至高的纬度，下一幕就坠落到粉身碎骨，面对无所适从的黑暗与孤独，反覆轮唱的You’re Gone迷航于逆境漩涡，众里寻它千百度，蓦然回首终于明白，那道光始终藏在内心深处。副歌幽美洒脱的假音诠释，勇于和过去的自己道别，眺望前方无尽的旅途，Finding love is easy, finding you ain’t easy, 因为有爱，让我们找到归属，因为有爱，就不会止于幸福，琴声伴随大编制弦乐与多部和声交响，层层叠进的丰沛情感，曲末一语You’re gone，释然归零后重啓，看见自我最真实的面目。疗愈心灵的一首励志抒情歌曲。\n\n--Nothing At All—\n你住在我的眼睛，也住在我的心里。\n你主宰我的眼泪与记忆，渴望共生共存永不分离。\n若失去你，And I’m Just Nothing At All.\n\n迷幻颓废的一首英式摇滚作品，由毕书尽X陈又齐最佳拍档共同创作，乐坛新锐鳄鱼乐团成员李晋玮/谢达孝担当编曲，述说一段失去所爱，却难以抽离的凄美爱情篇章，看似诗情画意的文字，冷眼哀悼着挚爱的出走，飘渺的电吉他回响揭开序曲。原来失去最爱的景象，就是世界毁灭的模样，原来你离去的地方，就是我一无所有的心脏，And I’m Just Nothing At All.\n\n--My Girl –\n清新不腻的一首抒情民谣作品，由金曲乐团佛跳墙吉他手黄宣铭操刀编曲，毕书尽X陈又齐共同创作词曲，简单青涩的木吉他分解和弦进歌，搭配象征着心跳的大鼓点，毕书尽回归温柔唱腔，诉说着即将萌芽的爱情，My Girl，你就是我要的心跳，没有你我就要死掉(疯掉)，没有华丽的词汇与包装，青春校园般的暧昧情节，小心翼翼的保护着最珍贵的事物，层层叠进的和声呼喊所爱的人，最直接的敞开心胸对白，回到最纯真的学生时代，Because You Are, My Girl.\n\n--蛋—\n「你是蛋黄我是蛋白，让我保护你的存在，然后变成蛋壳，我们就永远分不开。」异想天开的一首俏皮告白歌曲，由鳄鱼乐团吉他手李晋玮创作词曲，金曲歌手JerryC担任编曲，流行EDM的节奏MIX民谣吉他线条，意外Match无厘头却又诚恳实在的音乐风格，轻快的旋律加上多层次丰沛的和声编排，搭配毕书尽招牌甜蜜暖嗓，混搭蹦出全新滋味，曲末毕书尽唱到兴起，更突发奇想乱入「科科」窃喜笑声，让人会心一笑直接Fall In Love的撩妹系主打。\n\n--爱你就够了—\n灵感来自「I Need You Girl」的谐音「爱你就够了」，毕书尽X陈又齐共同创作词曲，由鳄鱼乐团吉他手李晋玮编曲，以最擅长的美式摇滚曲风，外加南洋乐器吉它丽丽，神采飞扬的阳光沙滩热情氛围，毕书尽邻家男孩般的青春唱腔，搭配时而勾人的帅气尾音，与摇滚乐队大放齐唱，洗脑旋律I Need You Girl不停播送，仿佛对着心仪女孩大声呼喊，伴随狂野的吉他Solo直上云霄，大胆示爱的一首夏季限定摇滚作品，此曲也收录偶像剧「噗通噗通我爱你」担任插曲。\n\n--Red n’ Hot—\n霸气狂放的一首硬式EDM作品，力邀Jolin/J.Sheon御用电子歌手LilPan潘信维操刀编曲，更送到美国纽约与BTS/LadyGaga /BrunoMars/AliciaKeys合作的格莱美混音大师Ken Lewis进行后置工程。凶猛的Trap＋Dubstep曲风为主架构，洗脑的Red n’ Hot如咒语般入侵脑细胞，宇宙浩瀚的合成器声响与重拍节奏轰炸，仿佛置身航天飞机倒数起飞，毕书尽化身舰长指挥，火箭喷发至梦想无尽的未来世界，Red n’ Hot, Like Fire Like Shot, Like Rocket Fly To The Star！曲末暴走Hot Style群众吶喊风格更令人疯狂摇摆！此曲也担任天堂M手游的指定歌曲。\n\n--Let’s Drunk –\n沁凉微醺的一首EDM作品，由金曲电音歌手JerryC 跨刀编曲与共同制作，歌曲是毕书尽X陈又齐在小酌放松之际，突来灵感以口哨吹奏的洗脑Hook，酒精与嬉闹中Free Style共同写下的词曲，完全打破过往忧郁悲伤的形象，以欧美时尚流行之Tropical House曲风，Sexy假音与抒情Rap唸唱的露骨挑逗文字，搭配轻快的电子节奏声响，如置身岛国夏夜海滩的慵懒风情，令人醉心闻之起舞，也呈现出毕书尽外冷内热的撩人面向，一首意图使人犯醉之性感力作。\n\n--我想你了—\n我想你了，最直白常见的一句话，也是最简单真切的表述。毕书尽X陈又齐共同创作词曲，由擅长钢琴弦乐的音乐家周菲比担任编曲，继「都是你害的」后再次挑战One Take无剪接的录音配唱，制作人为引导歌者内心情绪，要求毕书尽抱膝「坐」在沙发上演唱，以最无拘束的放空姿态，诠释最想念的柔软心境，伴着冷冽的钢琴进歌，不加修饰的呼吸与换气，略带失控的温柔假音弥漫空气，令人屏息聆听为之动容，不断轮唱洗脑「我想你了」，随着凄美弦乐压境来到崩溃边缘之际，却忍住眼泪收起伤悲，把最想念的瞬间，封存在心最深处的房间，最后熄灭全世界的灯，留下一位最想念的人。想念超载的一首走心抒情主打。\n\n--在你的世界--\n由老鹰音乐创作鬼才陈彦允量身订做词曲，金曲乐团佛跳墙吉他手黄宣铭操刀编曲，以一把尼龙弦吉他弹奏贯穿全曲，毕书尽叙事般的嗓音娓娓道来，从孤单的低语到哽咽的呢喃，从悲伤的吟唱到掏心的吶喊，曲末摇滚电吉他Solo与尼龙吉他合奏，看似两个不兼容的配器声响，却完美诠释了离爱出走后的伴侣，分裂成两个平行宇宙的陌生世界，忘不记却又回不去的幸福篇章，随着记忆渐行渐远消失不见，越夜越心酸的一首失恋抒情小品。",
                            "name": "Bii Your Light",
                            "totaldisk": 1,
                            "rating": 62293,
                            "pinyinname": "Bii Your Light",
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

    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }
    """


def play():
    """
    @api {post} /music/play/play 播放歌曲
    @apiVersion 1.0.0
    @apiGroup Play
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
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo 数据信息
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.genre 流派类型
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.bitrates 比特率
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.releasedate 发布日期
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.label 标签
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.exclusivity 歌曲版权付费模式（FREE，Normal，Purchase，ALAKA，Streaming，Cache）
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.translatename 翻译名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.version 版本
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.duration 歌曲长度
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.side 歌曲位于专辑的片（面）数
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.explicit 脏标
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.description 描述
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.name 名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.tracknumber 声音编号
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.rating 收听总数
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.cpItemID 出版公司单曲编号
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.pinyinname 歌曲拼音名称
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.languagetype 语言类型
    @apiSuccess (Success) {String} musicinfo.response.docs.datainfo.priceCode 价格代号
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
    @apiSuccess (Success) {String} musicinfo.response.docs.album.albumID 专辑专辑编号
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
    @apiSuccess (Success) {String} musicinfo.response.docs.album.albumPriceCode 专辑专辑价格代号
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
                        "fileExtension": "aac",
                        "fileSize": 2558709,
                        "dailydlcount": 0,
                        "orderid": "b3e3a9ebf396ee1a6903a59a1fcc4aee",
                        "url": "http://ksy.97ting.com/content/09/546/9546550-AAC-64K-FTD.aac?wsSecret=74ad66111ec652e547865f9013da6ecf&wsTime=5b766f80&transDeliveryCode=SH@23111334@1534315648@S@",
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
                                "genre": "Pop",
                                "bitrates": [
                                    "FLAC-1000K-FTD",
                                    "LRC-LRC",
                                    "MP3-128K-FTD",
                                    "MP3-192K-FTD",
                                    "MP3-256K-FTD",
                                    "MP3-320K-FTD"
                                ],
                                "releasedate": "2017-10-05",
                                "label": "福茂唱片",
                                "exclusivity": 1,
                                "translatename": "Be Your Light (电视剧「隧道」片尾曲)",
                                "version": "",
                                "duration": "05:19",
                                "side": 1,
                                "explicit": 0,
                                "description": "",
                                "name": "Be Your Light (电视剧「隧道」片尾曲)",
                                "tracknumber": 1,
                                "rating": 13373,
                                "cpItemID": "kwm17092810411_FTD",
                                "pinyinname": "Be Your Light (Dian Shi Ju「Sui Dao」Pian Wei Qu)",
                                "languagetype": "MAN",
                                "priceCode": ""
                            },
                            "artists": [
                                {
                                    "genre": "Pop",
                                    "region": "TW",
                                    "birthday": "1989-7-7",
                                    "itemcount": 89,
                                    "translatename": "Bii",
                                    "imagePathMap": [
                                        {
                                            "value": "/artist/005/54130-JPG-200X200-ARTIST.jpg",
                                            "key": "JPG-200X200-ARTIST"
                                        }
                                    ],
                                    "artistID": 54130,
                                    "description": "  毕书尽（Bii \\ 필서진），1989年7月7日出生于韩国首尔，中国台湾籍流行男歌手。\n2006年由父亲友人推荐给老鹰音乐公司创办人李亚明的赏识而签约成为旗下练习生。2010年7月发行首张EP《Bii》出道；同年10月6日发行首张专辑《Bii Story》，凭借专辑歌曲《转身之后》乐坛走红。2013年5月发行第二张个人专辑《Come back to Bii》，凭借专辑歌曲《Come Back To Me》入选第4届全球流行音乐金榜年度20大金曲与Hit Fm联播网年度电台点播冠军奖。2014年6月获得“2014Hito流行音乐奖”之Hito潜力男歌手奖；同年11月获得第19届新加坡金曲奖之舞台魅力奖。",
                                    "name": "毕书尽",
                                    "gender": "Male",
                                    "rating": 2215800,
                                    "pinyinname": "Bi Shu Jin",
                                    "albumcount": 20
                                }
                            ],
                            "itemID": 9546550,
                            "album": {
                                "genre": "Pop",
                                "cpInfo": [
                                    {
                                        "contentProviderGroupID": 30,
                                        "cpGroupName": "福茂唱片",
                                        "cpGroupAltName": "福茂唱片",
                                        "cpName": "福茂唱片",
                                        "cpCode": "福茂唱片",
                                        "contentProviderID": 4453
                                    }
                                ],
                                "albumID": 869035,
                                "releasedate": "2017-10-05",
                                "translatename": "Bii Your Light",
                                "version": "",
                                "artists": [
                                    {
                                        "artistname": "毕书尽",
                                        "artistID": 54130,
                                        "artisttranslatename": "Bii",
                                        "artistpinyinname": "Bi Shu Jin"
                                    }
                                ],
                                "totaltrack": 10,
                                "imagePathMap": [
                                    {
                                        "value": "/album/086/869035-JPG-240X240-ALBUM.jpg",
                                        "key": "JPG-240X240-ALBUM"
                                    }
                                ],
                                "explicit": 0,
                                "albumPriceCode": -1,
                                "description": "我是光\n投射你的每一道光\n渴望相遇 渴望相爱\n\n你是光\n反射我的每一道光\n互相辉映 互相补偿\n\n2017.10.05 I’ll Be Your Light 老鹰制作 福茂发行\n\nBii毕书尽睽违一年发行个人第五张全新专辑【Bii Your Light】，卸下华丽的武装回归音乐本质，拿出他最厉害的武器，用歌声攻占华语乐坛，一向给人忧郁王子印象的Bii毕书尽，不再只是单方面的接收大家给予的关爱，如今的他已经有能力作为别人的光芒，带给他人温暖与希望，如同这次专辑光的概念，不单单只是歌迷一直以来为他照明方向，而是交由他带领着大家前行，象是恒星般的照亮自己也照亮身旁的人相互依存着。\n\n发行四张专辑后，Bii毕书尽与公司一直在寻找如何突破以往形象的作品，这次集结了各方菁英，由金曲歌后蔡健雅x JerryC x陈君豪x黄宣铭x格莱美混音大师Ken Lewis，摄影大师邵亭魁x金曲设计大师颜伯骏，天王天后御用造型师王鸿志（小小）齐心打造，摆脱过往的既定印象，造型以简单又不失时尚的睡衣为主轴，打破旧规颠覆创意新思维，不添加过度华丽的包装，更衬托Bii毕书尽独特气质，也让大众更零距离接触Bii毕书尽最真实的样貌，希望大家着重在他的音乐和歌声上。\n在新专辑发行之前，Bii毕书尽陆续推出三首不同曲风的音乐作品，从第一首裸视自身状态的【You’re Gone】到第二首失去歌唱便一无所有的【Nothing At All】和第三首正能量爆发的【Be Your Light】，都一一展现Bii毕书尽在音乐上的无限潜能，新专辑首波强打【我想你了】毕式情歌再进化，撕裂般的深情呼唤，煽动人心止不住想念的泪水，原来最残忍的爱情，是你离开后还遗留下的痕迹，思念处处暗潮汹涌的侵袭独留下来的我。\n\n2017老鹰音乐年度大事，Bii毕书尽在万众期盼之下宣布年底12/9进攻台北小巨蛋，举办他个人首场小巨蛋演唱会【天堂M Bii毕书尽My Best Moment】，门票更在首卖当天3分钟内完售开出大红盘，Bii毕书尽表示：非常感谢大家对他的支持，演唱会当天一定会把最好的一面展现出来，绝对会让大家值回票价。\n\n2017/10/05老鹰制作 福茂发行\n\n曲序：\n1.\tBe Your Light/电视剧「隧道」片尾曲\n2.\tYou’re Gone/电视剧「噗通噗通我爱你」片尾曲\n3.\tNothing At All/电视剧「守护者K2」片头曲\n4.\tMy Girl \n5.\t蛋/电视剧「噗通噗通我爱你」插曲\n6.\t爱你就够了/电视剧「噗通噗通我爱你」插曲\n7.\tRed n’ Hot\n8.\tLet’s Drunk \n9.\t我想你了/电视剧「1%可能性」片尾曲\n10.\t在你的世界\n\n歌曲介绍：\n--Be Your Light—\n大气恢弘的一首能量系抒情摇滚主打，由第28届金曲奖最佳编曲人提名/最佳制作人陈君豪操刀编曲，海洋般深邃的琴音带入温柔坚定的呢喃，多层次和声铺排环绕，如置身宇宙天地之间的舒坦辽阔，撼动心窝的鼓击声响，如拂晓透窗般乍现，毕书尽招牌厚实的假音冲破阻碍，随着摇滚乐队倾斜而出，引领着群众的吶喊振奋人心，曲末突变切换的EDM曲风更是一绝，令人耳目一新的混搭巧思，也呈现了「光」的多元面貌概念，无论是黑夜闪烁的星光，床头温暖的月光，穿透云层曙光，专注所爱的目光，相信只要是「光」一定会灿烂的，I’ll be your light，每个黑暗时刻，为了你存活，I’ll be your light，每个回首时刻，陪在你身后。\n\n--You’re Gone—\n由金曲歌后蔡健雅量身作曲，制作人陈又齐填词，赤裸刻划出毕书尽内心世界的深度省思作品，诚恳不造作的木吉他弹奏，似唸似唱的呢喃嗓音，娓娓道出一路走来的颠簸与刻骨，象是休止符一般，渴望偶尔停驻，却又不得不前行的矛盾自缚。也许这一刻功成名就，停留在至高的纬度，下一幕就坠落到粉身碎骨，面对无所适从的黑暗与孤独，反覆轮唱的You’re Gone迷航于逆境漩涡，众里寻它千百度，蓦然回首终于明白，那道光始终藏在内心深处。副歌幽美洒脱的假音诠释，勇于和过去的自己道别，眺望前方无尽的旅途，Finding love is easy, finding you ain’t easy, 因为有爱，让我们找到归属，因为有爱，就不会止于幸福，琴声伴随大编制弦乐与多部和声交响，层层叠进的丰沛情感，曲末一语You’re gone，释然归零后重啓，看见自我最真实的面目。疗愈心灵的一首励志抒情歌曲。\n\n--Nothing At All—\n你住在我的眼睛，也住在我的心里。\n你主宰我的眼泪与记忆，渴望共生共存永不分离。\n若失去你，And I’m Just Nothing At All.\n\n迷幻颓废的一首英式摇滚作品，由毕书尽X陈又齐最佳拍档共同创作，乐坛新锐鳄鱼乐团成员李晋玮/谢达孝担当编曲，述说一段失去所爱，却难以抽离的凄美爱情篇章，看似诗情画意的文字，冷眼哀悼着挚爱的出走，飘渺的电吉他回响揭开序曲。原来失去最爱的景象，就是世界毁灭的模样，原来你离去的地方，就是我一无所有的心脏，And I’m Just Nothing At All.\n\n--My Girl –\n清新不腻的一首抒情民谣作品，由金曲乐团佛跳墙吉他手黄宣铭操刀编曲，毕书尽X陈又齐共同创作词曲，简单青涩的木吉他分解和弦进歌，搭配象征着心跳的大鼓点，毕书尽回归温柔唱腔，诉说着即将萌芽的爱情，My Girl，你就是我要的心跳，没有你我就要死掉(疯掉)，没有华丽的词汇与包装，青春校园般的暧昧情节，小心翼翼的保护着最珍贵的事物，层层叠进的和声呼喊所爱的人，最直接的敞开心胸对白，回到最纯真的学生时代，Because You Are, My Girl.\n\n--蛋—\n「你是蛋黄我是蛋白，让我保护你的存在，然后变成蛋壳，我们就永远分不开。」异想天开的一首俏皮告白歌曲，由鳄鱼乐团吉他手李晋玮创作词曲，金曲歌手JerryC担任编曲，流行EDM的节奏MIX民谣吉他线条，意外Match无厘头却又诚恳实在的音乐风格，轻快的旋律加上多层次丰沛的和声编排，搭配毕书尽招牌甜蜜暖嗓，混搭蹦出全新滋味，曲末毕书尽唱到兴起，更突发奇想乱入「科科」窃喜笑声，让人会心一笑直接Fall In Love的撩妹系主打。\n\n--爱你就够了—\n灵感来自「I Need You Girl」的谐音「爱你就够了」，毕书尽X陈又齐共同创作词曲，由鳄鱼乐团吉他手李晋玮编曲，以最擅长的美式摇滚曲风，外加南洋乐器吉它丽丽，神采飞扬的阳光沙滩热情氛围，毕书尽邻家男孩般的青春唱腔，搭配时而勾人的帅气尾音，与摇滚乐队大放齐唱，洗脑旋律I Need You Girl不停播送，仿佛对着心仪女孩大声呼喊，伴随狂野的吉他Solo直上云霄，大胆示爱的一首夏季限定摇滚作品，此曲也收录偶像剧「噗通噗通我爱你」担任插曲。\n\n--Red n’ Hot—\n霸气狂放的一首硬式EDM作品，力邀Jolin/J.Sheon御用电子歌手LilPan潘信维操刀编曲，更送到美国纽约与BTS/LadyGaga /BrunoMars/AliciaKeys合作的格莱美混音大师Ken Lewis进行后置工程。凶猛的Trap＋Dubstep曲风为主架构，洗脑的Red n’ Hot如咒语般入侵脑细胞，宇宙浩瀚的合成器声响与重拍节奏轰炸，仿佛置身航天飞机倒数起飞，毕书尽化身舰长指挥，火箭喷发至梦想无尽的未来世界，Red n’ Hot, Like Fire Like Shot, Like Rocket Fly To The Star！曲末暴走Hot Style群众吶喊风格更令人疯狂摇摆！此曲也担任天堂M手游的指定歌曲。\n\n--Let’s Drunk –\n沁凉微醺的一首EDM作品，由金曲电音歌手JerryC 跨刀编曲与共同制作，歌曲是毕书尽X陈又齐在小酌放松之际，突来灵感以口哨吹奏的洗脑Hook，酒精与嬉闹中Free Style共同写下的词曲，完全打破过往忧郁悲伤的形象，以欧美时尚流行之Tropical House曲风，Sexy假音与抒情Rap唸唱的露骨挑逗文字，搭配轻快的电子节奏声响，如置身岛国夏夜海滩的慵懒风情，令人醉心闻之起舞，也呈现出毕书尽外冷内热的撩人面向，一首意图使人犯醉之性感力作。\n\n--我想你了—\n我想你了，最直白常见的一句话，也是最简单真切的表述。毕书尽X陈又齐共同创作词曲，由擅长钢琴弦乐的音乐家周菲比担任编曲，继「都是你害的」后再次挑战One Take无剪接的录音配唱，制作人为引导歌者内心情绪，要求毕书尽抱膝「坐」在沙发上演唱，以最无拘束的放空姿态，诠释最想念的柔软心境，伴着冷冽的钢琴进歌，不加修饰的呼吸与换气，略带失控的温柔假音弥漫空气，令人屏息聆听为之动容，不断轮唱洗脑「我想你了」，随着凄美弦乐压境来到崩溃边缘之际，却忍住眼泪收起伤悲，把最想念的瞬间，封存在心最深处的房间，最后熄灭全世界的灯，留下一位最想念的人。想念超载的一首走心抒情主打。\n\n--在你的世界--\n由老鹰音乐创作鬼才陈彦允量身订做词曲，金曲乐团佛跳墙吉他手黄宣铭操刀编曲，以一把尼龙弦吉他弹奏贯穿全曲，毕书尽叙事般的嗓音娓娓道来，从孤单的低语到哽咽的呢喃，从悲伤的吟唱到掏心的吶喊，曲末摇滚电吉他Solo与尼龙吉他合奏，看似两个不兼容的配器声响，却完美诠释了离爱出走后的伴侣，分裂成两个平行宇宙的陌生世界，忘不记却又回不去的幸福篇章，随着记忆渐行渐远消失不见，越夜越心酸的一首失恋抒情小品。",
                                "name": "Bii Your Light",
                                "totaldisk": 1,
                                "rating": 62293,
                                "pinyinname": "Bii Your Light",
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

    @apiError (Error) 31011 No item id in the request params!

    @apiErrorExample {json} Error-Response:
    {
        "data": "No item id in the request params!"
    }
    """