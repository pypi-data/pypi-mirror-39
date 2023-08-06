#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/8/26

"""
    desc:pass
"""

import sys
import json
import re
import time
from bs4 import BeautifulSoup
import requests
import redis
import logging

conn = None
try:
    conn = redis.Redis('106.12.27.65', port=7379, password='yaserongyao123', decode_responses=True, db=0)
except Exception:
    logging.error('redis 不可用了')
    pass

#默认缓存半小时
DEFAULT_EXPIRE_TIME = 30 * 60

DEFAULT_HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
}


def spider_now_plaing(city):
    city_code = convert_name_code(city)
    KEY = 'YINGXUN:MOVIE:LIST:%s' % city_code
    nowplayings = []
    if conn is not None:
        if conn.exists(KEY):
            datas = json.loads(conn.get(KEY))
            for movie in datas:
                nowplayings.append(movie)
            return nowplayings

    url = BASE_URL_PLAYING + '%s/' % city_code
    response = requests.get(url, headers=DEFAULT_HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    uncovering_tip = soup.find('div', {'class': 'uncovering-tip'})
    if uncovering_tip:
        return uncovering_tip.text.replace(' ', '')
    nowplaying = soup.find('div', {'id': 'nowplaying'})
    lists = nowplaying.find_all('li', {'class': 'list-item'})
    for child in lists:
        if len(nowplayings) > 9:
            break
        movie_id = child['id']
        star = child['data-star']
        if star and star != '00':
            if int(star) % 10 == 0:
                star = str(int(star) / 10) + '星'
            else:
                star = str(float(star) / 10) + '星'
        else:
            star = '暂无'
        title = child['data-title']
        score = child['data-score']
        img = child.find('img')['src']
        detail = child.find('a')['href']
        movie = {
            'id': movie_id,
            'title': title,
            'score': score if score and score != '0' else '暂无',
            'star': star,
            'img': img,
            'detail': detail
        }
        #放到redis
        nowplayings.append(movie)
    if conn is not None:
        conn.setnx(KEY, json.dumps(nowplayings))
        #设置缓存失效时间 默认为半小时
        conn.expire(KEY, DEFAULT_EXPIRE_TIME)
    return nowplayings


def spider_movie_detail(movie_id, move_url):
    """
    """

    KEY = 'YINGXUN:MOVIE:DETAIL:%s' % movie_id
    if conn is not None:
        redis_exist = conn.exists(KEY)
        if redis_exist:
            move_detail = json.loads(conn.get(KEY))
            return move_detail

    response = requests.get(move_url, headers=DEFAULT_HEADER)
    soup = BeautifulSoup(response.text, "html.parser")

    #主演
    main_pic_info = soup.find('div', {'id': 'info'})
    director = main_pic_info.find('span').find('a').text

    #名人
    celebritys = soup.find_all('li', {'class': 'celebrity'})
    celebritys_info = parse_celebritys(celebritys)

    #简介
    summary_tag = soup.find('div', {'class':'related-info'})
    move_intro = summary_tag.find('i').text
    move_summary = summary_tag.find('span', {'property': 'v:summary'}).text
    trailer = 'https://movie.douban.com/subject/%s/trailer#trailer' % movie_id

    move_detail = {
        'director': director,
        'celebritys': celebritys_info,
        'summary': move_summary.replace(' ','').replace('\n',''),
        'trailer': trailer
    }
    if conn is not None:
        #放到redis movie:id:detail
        conn.setnx(KEY, json.dumps(move_detail))
        conn.expire(KEY, DEFAULT_EXPIRE_TIME)
    return move_detail


def parse_trailer(movie_url):
    response = requests.get(movie_url, headers=DEFAULT_HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    trailer = soup.find('source', {'type': 'video/mp4'})['src']
    return trailer


def parse_actors(actor):
    if actor and actor.find('span', {'class': 'attrs'}):
        actors = actor.find('span', {'class': 'attrs'}).find_all('a')
        display_actors = ''
        count = 0
        for actor in actors:
            if count > 4:
                break
            display_actors = display_actors + actor.text + '/'
            count += 1
        #放到redis movie:id:actors
    else:
        display_actors ='暂无'
    return display_actors


def parse_celebritys(celebritys):
    details = []
    for celebrity in celebritys:
        if celebrity and len(celebrity.contents):
            name = ''
            role = ''
            name_detal = ''
            name_span = celebrity.find('span', {'class': 'name'})
            if name_span:
                name = name_span.find('a').text
            role_span = celebrity.find('span', {'class': 'role'})
            if role_span:
                role = role_span['title']

            avatar_detail_tag = celebrity.find('a')
            avatar_url = ''
            if avatar_detail_tag:
                avatar_url = avatar_detail_tag['href']

            avatar_div = celebrity.find('div', {'class': 'avatar'})
            if avatar_div:
                avatar = avatar_div['style']
                if avatar:
                    avatar = re.findall(r"[(](.*?)[)]", avatar)
                    if len(avatar):
                        avatar = avatar[0]
            detail = {'name': name, 'role': role, 'avatar': avatar, 'avatar_url': avatar_url}
            details.append(detail)
        continue
    return details


def parse_trailer_video(movie_id, trailer_url):

    KEY = 'YINGXUN:MOVIE:TRAILER:%s' % movie_id
    if conn is not None:
        redis_exist = conn.exists(KEY)
        if redis_exist:
            videos = json.loads(conn.get(KEY))
            return videos
    print('trailer_url = ', trailer_url)
    response = requests.get(trailer_url, headers=DEFAULT_HEADER)
    soup = BeautifulSoup(response.text, "html.parser")
    div_video_list = soup.find('ul', {'class': 'video-list '})
    if div_video_list is None:
        return None
    lis = div_video_list.find_all('li')
    count = 1
    videos = []
    for li in lis:
        if count > 2:
            break
        img = li.find('img')['src']
        atag = li.find('p').find('a')
        video_url = atag['href']
        print('名称:%s, 视频地址:%s, 图片:%s' % (atag.text.strip(), video_url, img))
        trailer = parse_trailer(video_url)
        time = li.find('em').text
        time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
        trailer_video = {
            'id': video_url.split('/')[-2],
            'name': atag.text.strip(),
            'img': img,
            'url': trailer,
            'time': time * 1000
        }
        videos.append(trailer_video)
        count += 1
    if conn is not None:
        #放到redis  movie:id:trailer
        conn.setnx(KEY, json.dumps(videos))
        conn.expire(KEY, DEFAULT_EXPIRE_TIME * 2 * 24 * 30)
    return videos


BASE_URL_PLAYING = 'https://movie.douban.com/cinema/nowplaying/'


def convert_name_code(name):
    if name in citys:
        return citys[name]

citys = {
    '安庆': 'anqing',
    '安阳': 'anyang',
    '鞍山': 'anshan',
    '安康': 'ankang',
    '安顺': 'anshun',
    '阿勒泰': 'aletai',
    '阿克苏': 'akesu',
    '阿坝': 'aba',
    '北京': 'beijing',
    '保定': 'baoding',
    '宝鸡': 'baoji',
    '包头': 'baotou',
    '滨州': 'binzhou',
    '蚌埠': 'bangbu',
    '亳州': 'bozhou',
    '毕节': 'bijie',
    '本溪': 'benxi',
    '北海': 'beihai',
    '巴彦淖尔': 'bayannaoer',
    '白银': 'baiyin',
    '保山': 'baoshan',
    '百色': 'baise',
    '白山': 'baishan',
    '巴中': 'bazhong',
    '巴音郭楞': 'bayinguoleng',
    '白城': 'baicheng',
    '保亭': '131586',
    '重庆': 'chongqing',
    '成都': 'chengdu',
    '长沙': 'changsha',
    '长春': 'changchun',
    '常州': 'changzhou',
    '郴州': 'chenzhou',
    '常德': 'changde',
    '滁州': 'chuzhou',
    '沧州': 'cangzhou',
    '长治': 'changzhi',
    '赤峰': 'chifeng',
    '承德': 'chengde',
    '朝阳': 'chaoyang',
    '潮州': 'chaozhou',
    '昌吉': 'changji',
    '池州': 'chizhou',
    '崇左': 'chongzuo',
    '楚雄': 'chuxiong',
    '常熟': '129306',
    '澄迈': '131580',
    '昌江': '131583',
    '东莞': 'dongguan',
    '大连': 'dalian',
    '大庆': 'daqing',
    '东营': 'dongying',
    '德阳': 'deyang',
    '德州': 'dezhou',
    '大同': 'datong',
    '达州': 'dazhou',
    '丹东': 'dandong',
    '大理': 'dali',
    '定西': 'dingxi',
    '德宏': 'dehong',
    '儋州': 'danzhou',
    '东方': '131577',
    '大兴安岭': 'daxinganling',
    '迪庆': 'diqing',
    '恩施': 'enshi',
    '鄂尔多斯': 'eerduosi',
    '鄂州': 'ezhou',
    '佛山': 'foshan',
    '福州': 'fuzhou',
    '抚州': '118218',
    '阜阳': 'fuyang',
    '抚顺': 'fushun',
    '防城港': 'fangchenggang',
    '阜新': 'fuxin',
    '广州': 'guangzhou',
    '赣州': 'ganzhou',
    '贵阳': 'guiyang',
    '桂林': 'guilin',
    '广元': 'guangyuan',
    '广安': 'guangan',
    '甘南': 'gannan',
    '固原': 'guyuan',
    '贵港': 'guigang',
    '甘孜': 'ganzi',
    '杭州': 'hangzhou',
    '合肥': 'hefei',
    '哈尔滨': 'haerbin',
    '惠州': 'huizhou',
    '邯郸': 'handan',
    '湖州': 'huzhou',
    '海口': 'haikou',
    '淮安': 'huaian',
    '呼和浩特': 'huhehaote',
    '衡阳': 'hengyang',
    '黄冈': 'huanggang',
    '河源': 'heyuan',
    '菏泽': 'heze',
    '呼伦贝尔': 'hulunbeier',
    '淮南': 'huainan',
    '黄石': 'huangshi',
    '怀化': 'huaihua',
    '黄山': 'huangshan',
    '红河': 'honghe',
    '衡水': 'hengshui',
    '葫芦岛': 'huludao',
    '汉中': 'hanzhong',
    '黑河': 'heihe',
    '淮北': 'huaibei',
    '鹤壁': 'hebi',
    '河池': 'hechi',
    '贺州': 'hezhou',
    '鹤岗': 'hegang',
    '海东': 'haidong',
    '海西': 'haixi',
    '哈密': 'hami',
    '合肥': 'hefei',
    '海南': '118399',
    '金华': 'jinhua',
    '济南': 'jinan',
    '嘉兴': 'jiaxing',
    '江门': 'jiangmen',
    '九江': 'jiujiang',
    '济宁': 'jining',
    '荆州': 'jingzhou',
    '吉安': 'jian',
    '吉林': 'jilin',
    '晋中': 'jinzhong',
    '荆门': 'jingmen',
    '揭阳': 'jieyang',
    '焦作': 'jiaozuo',
    '晋城': 'jincheng',
    '酒泉': 'jiuquan',
    '锦州': 'jinzhou',
    '景德镇': 'jingdezhen',
    '佳木斯': 'jiamusi',
    '济源': 'jiyuan',
    '金昌': 'jinchang',
    '鸡西': 'jixi',
    '嘉峪关': 'jiayuguan',
    '吉林': 'jilinsheng',
    '昆明': 'kunming',
    '开封': 'kaifeng',
    '克拉玛依': 'kelamayi',
    '喀什': 'kashen',
    '昆山': '131410',
    '开平': '130313',
    '昆山': '131410',
    '临沂': 'linyi',
    '兰州': 'lanzhou',
    '洛阳': 'luoyang',
    '临汾': 'linfen',
    '廊坊': 'langfang',
    '丽水': 'lishui',
    '六安': 'luan',
    '娄底': 'loudi',
    '聊城': 'liaocheng',
    '连云港': 'lianyungang',
    '柳州': 'liuzhou',
    '吕梁': 'lvliang',
    '漯河': 'luohe',
    '乐山': 'leshan',
    '龙岩': 'longyan',
    '临夏': 'linxia',
    '泸州': 'luzhou',
    '辽阳': 'liaoyang',
    '六盘水': 'liupanshui',
    '陇南': 'longnan',
    '辽源': 'liaoyuan',
    '丽江': 'lijiang',
    '凉山': 'liangshan',
    '来宾': 'laibin',
    '拉萨': 'lasa',
    '临沧': 'lincang',
    '莱芜': 'laiwu',
    '乐东': '131584',
    '绵阳': 'mianyang',
    '梅州': 'meizhou',
    '马鞍山': 'maanshan',
    '茂名': 'maoming',
    '眉山': 'meishan',
    '牡丹江': 'mudanjiang',
    '南京': 'nanjing',
    '宁波': 'ningbo',
    '南通': 'nantong',
    '南昌': 'nanchang',
    '南宁': 'nanning',
    '南充': 'nanchong',
    '南阳': 'nanyang',
    '宁德': 'ningde',
    '南平': 'nanping',
    '内江': 'neijiang',
    '怒江': 'nujiang',
    '平顶山': 'pingdingshan',
    '莆田': 'putian',
    '盘锦': 'panjin',
    '萍乡': 'pingxiang',
    '平凉': 'pingliang',
    '普洱': 'puer',
    '濮阳': 'puyang',
    '攀枝花': 'panzhihua',
    '青岛': 'qingdao',
    '泉州': 'quanzhou',
    '衢州': 'quzhou',
    '曲靖': 'qujing',
    '黔南': 'qiannan',
    '清远': 'qingyuan',
    '黔东南': 'qiandongnan',
    '黔西南': 'qianxinan',
    '秦皇岛': 'qinhuangdao',
    '齐齐哈尔': 'qiqihaer',
    '庆阳': 'qingyang',
    '钦州': 'qinzhou',
    '潜江': 'qianjiang',
    '七台河': 'qitaihe',
    '琼海': 'qionghai',
    '日照': 'rizhao',
    '上海': 'shanghai',
    '深圳': 'shenzhen',
    '苏州': 'suzhou',
    '石家庄': 'shijiazhuang',
    '沈阳': 'shenyang',
    '上饶': 'shangrao',
    '绍兴': 'shaoxing',
    '商丘': 'shangqiu',
    '汕头': 'shantou',
    '宿迁': 'suqian',
    '三明': 'sanming',
    '韶关': 'shaoguan',
    '邵阳': 'shaoyang',
    '三亚': 'sanya',
    '绥化': 'suihua',
    '十堰': 'shiyan',
    '四平': 'siping',
    '汕尾': 'shanwei',
    '遂宁': 'suining',
    '宿州': '118194',
    '松原': 'songyuan',
    '商洛': 'shangluo',
    '随州': 'suizhou',
    '石嘴山': 'shizuishan',
    '三门峡': 'sanmenxia',
    '朔州': 'shuozhou',
    '双鸭山': 'shuangyashan',
    '石河子': 'shihezi',
    '天津': 'tianjin',
    '台州': '118181',
    '泰州': 'taizhou',
    '唐山': 'tangshan',
    '太原': 'taiyuan',
    '泰安': 'taian',
    '通辽': 'tongliao',
    '铁岭': 'tieling',
    '通化': 'tonghua',
    '铜仁': 'tongren',
    '天水': 'tianshui',
    '铜陵': 'tongling',
    '铜川': 'tongchuan',
    '塔城': 'tacheng',
    '天门': 'tianmen',
    '屯昌': '131579',
    '武汉': 'wuhan',
    '温州': 'wenzhou',
    '无锡': 'wuxi',
    '潍坊': 'weifang',
    '芜湖': 'wuhu',
    '乌鲁木齐': 'wulumuqi',
    '威海': 'weihai',
    '渭南': 'weinan',
    '梧州': 'wuzhou',
    '乌兰察布': 'wulanchabu',
    '乌海': 'wuhai',
    '文山': 'wenshan',
    '吴忠': 'wuzhong',
    '武威': 'wuwei',
    '文昌': 'wenchang',
    '万宁': '131576',
    '吴江区': '129309',
    '五指山': '131575',
    '西安': 'xian',
    '厦门': 'xiamen',
    '徐州': 'xuzhou',
    '新乡': 'xinxiang',
    '襄阳': 'xiangyang',
    '信阳': 'xinyang',
    '湘潭': 'xiangtan',
    '邢台': 'xingtai',
    '宣城': 'xuancheng',
    '孝感': 'xiaogan',
    '许昌': 'xuchang',
    '西宁': 'xining',
    '咸宁': 'xianning',
    '咸阳': 'xianyang',
    '湘西': 'xiangxi',
    '忻州': 'xinzhou',
    '新余': 'xinyu',
    '仙桃': 'xiantao',
    '兴安盟': 'xinganmeng',
    '锡林郭勒': 'xilinguole',
    '西双版纳': 'xishuangbanna',
    '兴安盟': 'xinganmeng',
    '烟台': 'yantai',
    '盐城': 'yancheng',
    '扬州': 'yangzhou',
    '宜春': 'yichun',
    '银川': 'yinchuan',
    '运城': 'yuncheng',
    '延边': 'yanbian',
    '宜昌': 'yichang',
    '阳江': 'yangjiang',
    '营口': 'yingkou',
    '宜宾': 'yibin',
    '永州': 'yongzhou',
    '榆林': '118378',
    '玉林': 'yulin',
    '益阳': 'yiyang',
    '岳阳': 'yueyang',
    '玉溪': 'yuxi',
    '延安': 'yanan',
    '鹰潭': 'yingtan',
    '伊犁': 'yili',
    '阳泉': 'yangquan',
    '云浮': 'yunfu',
    '雅安': 'yaan',
    '伊春': '118152',
    '杨凌区': '131061',
    '郑州': 'zhengzhou',
    '中山': 'zhongshan',
    '镇江': 'zhenjiang',
    '珠海': 'zhuhai',
    '株洲': 'zhuzhou',
    '湛江': 'zhanjiang',
    '漳州': 'zhangzhou',
    '淄博': 'zibo',
    '张家口': 'zhangjiakou',
    '肇庆': 'zhaoqing',
    '枣庄': 'zaozhuang',
    '遵义': 'zunyi',
    '周口': 'zhoukou',
    '驻马店': 'zhumadian',
    '舟山': 'zhoushan',
    '自贡': 'zigong',
    '资阳': 'ziyang',
    '张家界': 'zhangjiajie',
    '张掖': 'zhangye',
    '中卫': 'zhongwei',
    '昭通': 'zhaotong'
}


if __name__ == '__main__':
    import re
    # nowplayings = spider_now_plaing('巴音郭楞')
    # print nowplayings
    #
    # print nowplayings
    # for nowplaying in nowplayings:
    #     spider_move_detail(nowplaying['title'], nowplaying['detail'])
    # a = 'background-image: url(https://img3.doubanio.com/view/celebrity/s_ratio_celebrity/public/p6285.jpg)'

    # print convert_name_code('中卫')
    # p = re.compile(r'[(](.*?)[)]', re.S)
    # print re.findall(r"[(](.*?)[)]", a)[0]

    # parse_trailer_video('https://movie.douban.com/trailer/234679/#content')

    # spider_move_detail('https://movie.douban.com/subject/26425063')

    # trailer = 'https://movie.douban.com/subject/26147417/trailer#trailer'
    #
    # response = requests.get(trailer)
    # print(response.text)
    # soup = BeautifulSoup(response.text, "html.parser")
    # div_video_list = soup.find('ul', {'class': 'video-list '})
    # print(div_video_list)
    # lis = div_video_list.find_all('li')
    # count = 1
    # for li in lis:
    #     if count > 2:
    #         break
    #     print('============')
    #     img = li.find('img')['src']
    #     atag = li.find('p').find('a')
    #     time = li.find('em').text

        # print()
        # print('名称:%s, 视频地址:%s, 图片:%s' %(atag.text.strip(), atag['href'], img))
        # print(parse_trailer(atag['href']))
        # count = count + 1
    #     print()


    # print(spider_now_plaing('北京'))

    # a=[{'name':'www'}]
    # print(type(json.dumps(a)))

    # a = 'https://movie.douban.com/trailer/237883/#content'
    # print(a.split('/')[-2])

    # for city,value in citys.items():
    #     print(city, value)
    #     nowplayings = spider_now_plaing(city)
    #     if isinstance(nowplayings, list):
    #         for movie in nowplayings:
    #             movie_detail = spider_movie_detail(movie['id'], movie['detail'])
    #             parse_trailer_video(movie['id'], movie_detail['trailer'])

