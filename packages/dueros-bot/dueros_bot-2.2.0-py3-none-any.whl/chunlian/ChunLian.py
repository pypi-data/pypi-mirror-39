#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018-12-15

"""
    desc:pass
"""
from datetime import datetime
from datetime import date
import logging
import random

from dueros.Bot import Bot
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.BodyTemplate5 import BodyTemplate5
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.Hint import Hint
from dueros.card.TextCard import TextCard

class ChunLian(Bot):

    def __init__(self, request_data):
        super(ChunLian, self).__init__(request_data)
        self.add_launch_handler(self.handle_launch)
        self.add_common_default_intent_handler(self.default)
        self.add_common_next_intent_handler(self.change)
        self.add_common_confirm_intent_handler(self.change)
        self.add_common_cancel_intent_handler(self.handle_end_session)
        self.add_session_ended_handler(self.handle_end_session)

    def handle_launch(self):
        self.wait_answer()
        djs = dao_ji_shi()
        if djs[0] == 2:
            text = djs[1]
            if self.is_support_display():
                return {
                    'directives': build_body_template1_directives('距离春节还很远', text, '好的/是的'),
                    'outputSpeech': '欢迎您使用春联集锦, ' + text + ', 您可以对我说:好的或是的 来获取对联, 对我说:不用了或算了 可以关闭技能'
                }
            else:
                return {
                    'card': TextCard(text),
                    'outputSpeech': '欢迎您使用春联集锦,' + text + ', 您可以对我说:好的或是的 来获取对联, 对我说:不用了或算了 可以关闭技能'
                }
        else:
            #快了
            text = djs[1] + '，我为你准备好了几幅春节对联,是否要看一看呢？'
            if self.is_support_display():
                return {
                    'directives': build_body_template1_directives('新春快乐', text, '好的/是的'),
                    'outputSpeech': '欢迎您使用春联集锦,' + text + ', 您可以对我说:好的或是的 来获取对联, 对我说:不用了或算了 可以关闭技能'
                }
            else:
                return {
                    'card': TextCard(text),
                    'outputSpeech': '欢迎您使用春联集锦,' + text + ', 您可以对我说:好的或是的 来获取对联, 对我说:不用了或算了 可以关闭技能'
                }

    def change(self):
        self.wait_answer()

        prev_index = int(self.get_session_attribute('last_index', str(random.randint(0, len(datas)))))
        last_index = 0
        random_count = 0
        while True:
            if random_count > 3:
                break
            last_index = random.randint(0, len(datas) - 1)
            if last_index != prev_index:
                break
            random_count = random_count + 1
        self.set_session_attribute('last_index', str(last_index), '0')
        data = datas[last_index]
        if self.is_support_display():
            return {
                'directives': build_body_template5_directives(data['hengpi'], data['url'], '换一个'),
                'outputSpeech': '<speak>上联是:' + data['sl'] + '<silence time="1s"></silence>下联是:' + data['xl'] + '<silence time="1s"></silence>横批:' + data['hengpi'] + '</speak>'
            }
        else:
            return {
                'card': TextCard('上联是:' + data['sl'] + '下联是:' + data['xl'] + '横批:' + data['hengpi']),
                'outputSpeech': '<speak>上联是:' + data['sl'] + '<silence time="1s"></silence>下联是:' + data['xl'] + '<silence time="1s"></silence>横批:' + data['hengpi'] + ', 您可以对我说: 换一个或下一个 来获取其他春联</speak>'
            }

    def default(self):
        self.wait_answer()
        return {
            'outputSpeech': '抱歉，我没听清，请您再次告诉我'
        }

    def handle_end_session(self):
        self.end_session()
        return {
            'outputSpeech': '谢谢您本次使用，欢迎再次使用春联集锦，我会给你更多惊喜哦'
        }


def dao_ji_shi():
    now = date.today()
    print(now)
    logging.info('今天是 = %s' % now)
    if (date(2019, 3, 7) - now).days > 0:
        cha = (date(2019, 2, 5)-now).days
        print(cha)
        logging.info('还差几天 = %s' % cha)
        if cha > 0:
            if cha > 120:
                return 2, '距离2019年春节至少还有4个多月, 要继续好好学习和工作哦 '
            elif cha > 60:
                return 1, '距离2019年春节还有2个多月'
            elif (cha > 1) and (cha < 6):
                return 0, '马上就要到除夕了，阖家团圆的日子，即使再忙也要记得回家哦 '
            else:
                return 0, '距离2019年猪年春节还有%s天' % cha
        elif cha == 1:
            return 0, '今天是中国传统节除夕，记得要早点回家团圆哦'
        elif cha == 0:
            return 0, '小度祝您春节快乐，猪年大吉大利, 万事如意，身体健康, 阖家欢乐'
        elif cha > -30:
            return 0, '小度祝您春节快乐，春节期间注意饮食和人身安全'
    else:
        if (date(2020, 1, 25)-now).days > 0:
            if (date(2020, 1, 25)-now).days > 120:
                return 2, '距离2020年春节至少还有4个多月, 要继续好好学习和工作哦 '
            elif (date(2020, 1, 25)-now).days > 60:
                return 1, '距离2020年春节还有3个多月, 不要松懈哦 '
            else:
                return 0, '距离2020年春节还有%s天' % (date(2020, 1, 25) - now).days
        elif (date(2020, 1, 25)-now).days == 0:
            return 0, '小度祝您春节快乐，万事如意，身体健康, 阖家欢乐'
        elif (date(2020, 1, 25)-now).days == 1:
            return 0, '今天是中国传统节除夕，记得要早点回家团圆哦'
        elif (date(2020, 1, 25) - now).days > -30:
            return 0, '小度祝您春节快乐，春节期间注意饮食和人身安全'


def build_body_template1_directives(title, content, hint_txt):
    directives = []
    template = BodyTemplate1()
    template.set_title(title)
    template.set_plain_text_content(content)
    template.set_background_image(BG)
    directive = RenderTemplate(template)
    hint = Hint(hint_txt)
    directives.append(hint)
    directives.append(directive)
    return directives


def build_body_template5_directives(title, img, hint_txt):
    directives = []
    template = BodyTemplate5()
    template.set_title(title)
    template.set_background_image(img)
    template.add_images(img)
    directive = RenderTemplate(template)
    hint = Hint(hint_txt)
    directives.append(hint)
    directives.append(directive)
    return directives

BG = 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/demo.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T03%3A32%3A42Z%2F-1%2F%2Facff03992c14ecc95bb3b4e90f8caf50dd00a7de2a9d5fe1a35752d2e896e9ca'

datas = [
    {'hengpi': '万事如意', 'sl': '大顺大财大吉利', 'xl': '新春新喜新世纪',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F-%E5%A4%A7%E9%A1%BA%E5%A4%A7%E8%B4%A2%E5%A4%A7%E5%90%89%E5%88%A9-%E6%96%B0%E6%98%A5%E6%96%B0%E5%96%9C%E6%96%B0%E4%B8%96%E7%BA%AA.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-14T16%3A31%3A55Z%2F-1%2F%2F0f337dcf4156e6d60be0dff9dbf87b85fbb8e481bbd4f0dc148e8717c2fba332'},
    {'hengpi': '国强富民', 'sl': '精耕细作丰收岁', 'xl': '勤俭持家有余年',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%9B%BD%E5%BC%BA%E5%AF%8C%E6%B0%91-%E7%B2%BE%E8%80%95%E7%BB%86%E4%BD%9C%E4%B8%B0%E6%94%B6%E5%B2%81-%E5%8B%A4%E4%BF%AD%E6%8C%81%E5%AE%B6%E6%9C%89%E4%BD%99%E5%B9%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A43%3A53Z%2F-1%2F%2F17cca44aefd458cc79967874cc52b924c97b4a1d17ecfd93039013f044fbad97'},
    {'hengpi': '大展宏图', 'sl': '创大业千秋昌盛', 'xl': '展宏图再就辉煌',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%A4%A7%E5%B1%95%E5%AE%8F%E5%9B%BE-%E5%88%9B%E5%A4%A7%E4%B8%9A%E5%8D%83%E7%A7%8B%E6%98%8C%E7%9B%9B-%E5%B1%95%E5%AE%8F%E5%9B%BE%E5%86%8D%E5%B0%B1%E8%BE%89%E7%85%8C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A44%3A54Z%2F-1%2F%2Fc78f9fe23328e7c600e33992bd9ee377a1fe6540e3b05ea21491fbbf94402672'},
    {'hengpi': '福喜盈门', 'sl': '丹凤呈祥龙献瑞', 'xl': '红桃贺岁杏迎春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E7%A6%8F%E5%96%9C%E7%9B%88%E9%97%A8-%E4%B8%B9%E5%87%A4%E5%91%88%E7%A5%A5%E9%BE%99%E7%8C%AE%E7%91%9E-%E7%BA%A2%E6%A1%83%E8%B4%BA%E5%B2%81%E6%9D%8F%E8%BF%8E%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A50%3A02Z%2F-1%2F%2F2a62d6753c3032451101140da1e41108b07a785b4e8281022a75690a14d10830'},
    {'hengpi': '福满人间', 'sl': '丹凤呈祥龙献瑞', 'xl': '红桃贺岁杏迎春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E7%A6%8F%E6%BB%A1%E4%BA%BA%E9%97%B4-%E4%B8%B9%E5%87%A4%E5%91%88%E7%A5%A5%E9%BE%99%E7%8C%AE%E7%91%9E-%E7%BA%A2%E6%A1%83%E8%B4%BA%E5%B2%81%E6%9D%8F%E8%BF%8E%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A52%3A22Z%2F-1%2F%2Fe9389810999440e258dd86a1902ca206c36e425aa6be94d470f3368ed59d9ef9'},
    {'hengpi': '喜气盈门', 'sl': '福旺财旺运气旺', 'xl': '家兴人兴事业兴',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%96%9C%E6%B0%94%E7%9B%88%E9%97%A8-%E7%A6%8F%E6%97%BA%E8%B4%A2%E6%97%BA%E8%BF%90%E6%B0%94%E6%97%BA-%E5%AE%B6%E5%85%B4%E4%BA%BA%E5%85%B4%E4%BA%8B%E4%B8%9A%E5%85%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A54%3A50Z%2F-1%2F%2F02374b6fa22a88e6bda1f60d3765ce55ce86af6291aa5c48d71426ff6a12c744'},
    {'hengpi': '合家欢乐', 'sl': '欢声笑语贺新春', 'xl': '欢聚一堂迎新年',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%90%88%E5%AE%B6%E6%AC%A2%E4%B9%90-%E6%AC%A2%E5%A3%B0%E7%AC%91%E8%AF%AD%E8%B4%BA%E6%96%B0%E6%98%A5-%E6%AC%A2%E8%81%9A%E4%B8%80%E5%A0%82%E8%BF%8E%E6%96%B0%E5%B9%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A56%3A36Z%2F-1%2F%2F7e30d8484f1a85c80d8953c7a50bc31f6b21b5e2f49e892bd9072783954aa175'},
    {'hengpi': '春回大地', 'sl': '绿竹别其三分景', 'xl': '红梅正报万家春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%98%A5%E5%9B%9E%E5%A4%A7%E5%9C%B0-%E7%BB%BF%E7%AB%B9%E5%88%AB%E5%85%B6%E4%B8%89%E5%88%86%E6%99%AF-%E7%BA%A2%E6%A2%85%E6%AD%A3%E6%8A%A5%E4%B8%87%E5%AE%B6%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A58%3A10Z%2F-1%2F%2F5c56034a19104df8cfe21cf1227c121111a190cf9296118ce3f2ec07272c1f1b'},
    {'hengpi': '财源不断', 'sl': '占天时地利人和', 'xl': '取九州四海财宝',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E8%B4%A2%E6%BA%90%E4%B8%8D%E6%96%AD-%E5%8D%A0%E5%A4%A9%E6%97%B6%E5%9C%B0%E5%88%A9%E4%BA%BA%E5%92%8C-%E5%8F%96%E4%B9%9D%E5%B7%9E%E5%9B%9B%E6%B5%B7%E8%B4%A2%E5%AE%9D.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T00%3A59%3A58Z%2F-1%2F%2F0cc34aabb93c228698f3b69d42c8f071f420bf4a0d5eda6850e28b71e1fd2e03'},
    {'hengpi': '喜迎新春', 'sl': '一年四季春常在', 'xl': '万紫千红永开花',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%96%9C%E8%BF%8E%E6%96%B0%E6%98%A5-%E4%B8%80%E5%B9%B4%E5%9B%9B%E5%AD%A3%E6%98%A5%E5%B8%B8%E5%9C%A8-%E4%B8%87%E7%B4%AB%E5%8D%83%E7%BA%A2%E6%B0%B8%E5%BC%80%E8%8A%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A01%3A32Z%2F-1%2F%2F86bdf93f80ea61a703b5d00e0aa8cecb01c4e7cd98239df4246ba49e520d6867'},
    {'hengpi': '新年大吉', 'sl': '冬去山川齐秀丽', 'xl': '喜来桃里共芬芳',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%96%B0%E5%B9%B4%E5%A4%A7%E5%90%89-%E5%86%AC%E5%8E%BB%E5%B1%B1%E5%B7%9D%E9%BD%90%E7%A7%80%E4%B8%BD-%E5%96%9C%E6%9D%A5%E6%A1%83%E9%87%8C%E5%85%B1%E8%8A%AC%E8%8A%B3.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A03%3A05Z%2F-1%2F%2F3288e6de0987fd38081c7aaad99497e47044c5df9e6f0336e9297c04ff8377b3'},
    {'hengpi': '财源广进', 'sl': '财源滚滚随春到', 'xl': '喜气洋洋伴福来',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E8%B4%A2%E6%BA%90%E5%B9%BF%E8%BF%9B-%E8%B4%A2%E6%BA%90%E6%BB%9A%E6%BB%9A%E9%9A%8F%E6%98%A5%E5%88%B0-%E5%96%9C%E6%B0%94%E6%B4%8B%E6%B4%8B%E4%BC%B4%E7%A6%8F%E6%9D%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A04%3A42Z%2F-1%2F%2Fcdde2a42ecef29c111ab7037fd4fbf5c0c2bfa6a6e169870c125599a85ca6577'},
    {'hengpi': '好事临门', 'sl': '迎新春事事如意', 'xl': '接鸿福步步高升',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%A5%BD%E4%BA%8B%E4%B8%B4%E9%97%A8-%E8%BF%8E%E6%96%B0%E6%98%A5%E4%BA%8B%E4%BA%8B%E5%A6%82%E6%84%8F-%E6%8E%A5%E9%B8%BF%E7%A6%8F%E6%AD%A5%E6%AD%A5%E9%AB%98%E5%8D%87.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A06%3A17Z%2F-1%2F%2F0fe7e90c844404d8cdd581ac520c24541965a32042c20c56fb84f22ca0b4eb68'},
    {'hengpi': '欢度春节', 'sl': '大地流金万事通', 'xl': '冬去春来万象新',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%AC%A2%E5%BA%A6%E6%98%A5%E8%8A%82-%E5%A4%A7%E5%9C%B0%E6%B5%81%E9%87%91%E4%B8%87%E4%BA%8B%E9%80%9A-%E5%86%AC%E5%8E%BB%E6%98%A5%E6%9D%A5%E4%B8%87%E8%B1%A1%E6%96%B0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A07%3A52Z%2F-1%2F%2F102038045a4aeb5d4f06b2e238e84549ac4d3b07a76d71a03cb926f1dbd60fe3'},
    {'hengpi': '鸟语花香', 'sl': '日出江花红胜火', 'xl': '春来江水绿如蓝',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E9%B8%9F%E8%AF%AD%E8%8A%B1%E9%A6%99-%E6%97%A5%E5%87%BA%E6%B1%9F%E8%8A%B1%E7%BA%A2%E8%83%9C%E7%81%AB-%E6%98%A5%E6%9D%A5%E6%B1%9F%E6%B0%B4%E7%BB%BF%E5%A6%82%E8%93%9D.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A09%3A22Z%2F-1%2F%2F10855feac1978b4a5fd5a77fd156c4943658d3bb728c2b8a563e4871df4e9705'},
    {'hengpi': '喜迎新春', 'sl': '喜居宝地千年旺', 'xl': '万水千山尽得辉',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%96%9C%E8%BF%8E%E6%96%B0%E6%98%A5-%E5%96%9C%E5%B1%85%E5%AE%9D%E5%9C%B0%E5%8D%83%E5%B9%B4%E6%97%BA-%E4%B8%87%E6%B0%B4%E5%8D%83%E5%B1%B1%E5%B0%BD%E5%BE%97%E8%BE%89.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A10%3A56Z%2F-1%2F%2Fcc2bc1bcb13ec43dece8eadf2de7ec1541cc11696c0858d67079641207a95f13'},
    {'hengpi': '万象更新', 'sl': '五湖四海皆春色', 'xl': '万水千山尽得辉',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%B8%87%E8%B1%A1%E6%9B%B4%E6%96%B0-%E4%BA%94%E6%B9%96%E5%9B%9B%E6%B5%B7%E7%9A%86%E6%98%A5%E8%89%B2-%E4%B8%87%E6%B0%B4%E5%8D%83%E5%B1%B1%E5%B0%BD%E5%BE%97%E8%BE%89.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A12%3A33Z%2F-1%2F%2F1c83b96ee62d4f08833a6c41f80605e4bc89f9a51dfc46f3e8dd2432f7d42d52'},
    {'hengpi': '欢度春节', 'sl': '和顺门第增百福', 'xl': '合家欢乐纳千祥',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%AC%A2%E5%BA%A6%E6%98%A5%E8%8A%82-%E5%92%8C%E9%A1%BA%E9%97%A8%E7%AC%AC%E5%A2%9E%E7%99%BE%E7%A6%8F-%E5%90%88%E5%AE%B6%E6%AC%A2%E4%B9%90%E7%BA%B3%E5%8D%83%E7%A5%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A14%3A07Z%2F-1%2F%2Ffbe7cec77d0d381d3d049029d77991aa102683b95230003c43fbd9a18687654f'},
    {'hengpi': '山河壮丽', 'sl': '壮丽山河多异彩', 'xl': '文明国度遍高风',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%B1%B1%E6%B2%B3%E5%A3%AE%E4%B8%BD-%E5%A3%AE%E4%B8%BD%E5%B1%B1%E6%B2%B3%E5%A4%9A%E5%BC%82%E5%BD%A9-%E6%96%87%E6%98%8E%E5%9B%BD%E5%BA%A6%E9%81%8D%E9%AB%98%E9%A3%8E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A15%3A23Z%2F-1%2F%2Fb7df0e5db6b423fb2c6cf89c095751f5cd2ec9b03c7138054bae5133770109f2'},
    {'hengpi': '春风化雨', 'sl': '东风化雨山山翠', 'xl': '政策归心处处春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%98%A5%E9%A3%8E%E5%8C%96%E9%9B%A8-%E4%B8%9C%E9%A3%8E%E5%8C%96%E9%9B%A8%E5%B1%B1%E5%B1%B1%E7%BF%A0-%E6%94%BF%E7%AD%96%E5%BD%92%E5%BF%83%E5%A4%84%E5%A4%84%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A16%3A47Z%2F-1%2F%2Fbec690abe981df4c2761a7212cf9d3eff4880a96ec9df9a3e7c601c81cb38a12'},
    {'hengpi': '福喜盈门', 'sl': '春归大地人间暖', 'xl': '福降神州喜临门',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E7%A6%8F%E5%96%9C%E7%9B%88%E9%97%A8-%E6%98%A5%E5%BD%92%E5%A4%A7%E5%9C%B0%E4%BA%BA%E9%97%B4%E6%9A%96-%E7%A6%8F%E9%99%8D%E7%A5%9E%E5%B7%9E%E5%96%9C%E4%B8%B4%E9%97%A8.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A18%3A12Z%2F-1%2F%2F4cc5e7c4e95bcf47d4e980330a1906c7640d692ce8409a4fb254c7267bfc97ea'},
    {'hengpi': '吉星高照', 'sl': '内外平安好运来', 'xl': '合家欢乐财源进',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%90%89%E6%98%9F%E9%AB%98%E7%85%A7-%E5%86%85%E5%A4%96%E5%B9%B3%E5%AE%89%E5%A5%BD%E8%BF%90%E6%9D%A5-%E5%90%88%E5%AE%B6%E6%AC%A2%E4%B9%90%E8%B4%A2%E6%BA%90%E8%BF%9B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A20%3A27Z%2F-1%2F%2Fdc0670b0c57c798f66e98fe9ff278e2a7ec8ccaa43a1ad092f0f3fa6f7e99249'},
    {'hengpi': '喜迎新春', 'sl': '喜滋滋迎新年', 'xl': '笑盈盈辞旧岁',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%96%9C%E8%BF%8E%E6%96%B0%E6%98%A5-%E5%96%9C%E6%BB%8B%E6%BB%8B%E8%BF%8E%E6%96%B0%E5%B9%B4-%E7%AC%91%E7%9B%88%E7%9B%88%E8%BE%9E%E6%97%A7%E5%B2%81.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A22%3A22Z%2F-1%2F%2F384207e4e1a25c8b516484752d97f8e5a53cfa0a6e7a72ece09dcd81694b68de'},
    {'hengpi': '五福临门', 'sl': '万事如意展宏图', 'xl': '万事如意步步高',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%BA%94%E7%A6%8F%E4%B8%B4%E9%97%A8-%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F%E5%B1%95%E5%AE%8F%E5%9B%BE-%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F%E6%AD%A5%E6%AD%A5%E9%AB%98.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A24%3A13Z%2F-1%2F%2Ff66d346cf8f1685c6955869f155b46586c4f721f95ff9806567328528b2c1d33'},
    {'hengpi': '吉星高照', 'sl': '一帆风顺年年好', 'xl': '万事如意步步高',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%90%89%E6%98%9F%E9%AB%98%E7%85%A7-%E4%B8%80%E5%B8%86%E9%A3%8E%E9%A1%BA%E5%B9%B4%E5%B9%B4%E5%A5%BD-%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F%E6%AD%A5%E6%AD%A5%E9%AB%98.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A25%3A44Z%2F-1%2F%2F77dcff2dd640108428c41e4391ab1e18fef5e09fc450ccb3831764636d5e3a7e'},
    {'hengpi': '人心欢畅', 'sl': '家过小康欢乐日', 'xl': '春回大地艳阳天',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%BA%BA%E5%BF%83%E6%AC%A2%E7%95%85-%E5%AE%B6%E8%BF%87%E5%B0%8F%E5%BA%B7%E6%AC%A2%E4%B9%90%E6%97%A5-%E6%98%A5%E5%9B%9E%E5%A4%A7%E5%9C%B0%E8%89%B3%E9%98%B3%E5%A4%A9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A28%3A24Z%2F-1%2F%2F965383920f5933a0db91b2caa4b3fa58eaccdf63d3d43a9280fc1c53af1c07f6'},
    {'hengpi': '五福四海', 'sl': '春满人间欢歌阵阵', 'xl': '福临门第喜气洋洋',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%BA%94%E7%A6%8F%E5%9B%9B%E6%B5%B7-%E6%98%A5%E6%BB%A1%E4%BA%BA%E9%97%B4%E6%AC%A2%E6%AD%8C%E9%98%B5%E9%98%B5-%E7%A6%8F%E4%B8%B4%E9%97%A8%E7%AC%AC%E5%96%9C%E6%B0%94%E6%B4%8B%E6%B4%8B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A30%3A11Z%2F-1%2F%2F3180f7455d5ffa3368dd05bc89ce6524b9c47727ecbbf5f186ae91c66f14c0b8'},
    {'hengpi': '新春大吉', 'sl': '日日财源顺意来', 'xl': '年年福禄随春到',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%96%B0%E6%98%A5%E5%A4%A7%E5%90%89-%E6%97%A5%E6%97%A5%E8%B4%A2%E6%BA%90%E9%A1%BA%E6%84%8F%E6%9D%A5-%E5%B9%B4%E5%B9%B4%E7%A6%8F%E7%A6%84%E9%9A%8F%E6%98%A5%E5%88%B0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A31%3A32Z%2F-1%2F%2F6f4fe74069d76fc09be29fdbf83d187208654ec5fe884225899cad659c880cc4'},
    {'hengpi': '形势喜人', 'sl': '多劳多得人人乐', 'xl': '丰产丰收岁岁甜',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%BD%A2%E5%8A%BF%E5%96%9C%E4%BA%BA-%E5%A4%9A%E5%8A%B3%E5%A4%9A%E5%BE%97%E4%BA%BA%E4%BA%BA%E4%B9%90-%E4%B8%B0%E4%BA%A7%E4%B8%B0%E6%94%B6%E5%B2%81%E5%B2%81%E7%94%9C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A33%3A51Z%2F-1%2F%2F8f3d17f8ec7be3eb8c7c73c0c2cc813e4421a5a46382f3da267b3abfb0f42199'},
    {'hengpi': '辞旧迎春', 'sl': '一干二净除旧习', 'xl': '五讲四美树新风',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E8%BE%9E%E6%97%A7%E8%BF%8E%E6%98%A5-%E4%B8%80%E5%B9%B2%E4%BA%8C%E5%87%80%E9%99%A4%E6%97%A7%E4%B9%A0-%E4%BA%94%E8%AE%B2%E5%9B%9B%E7%BE%8E%E6%A0%91%E6%96%B0%E9%A3%8E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A35%3A08Z%2F-1%2F%2F6f848e9ec8b341523c3fa913aee8201e916a2fbaf1aeaf282cf00e9ee2f22e8c'},
    {'hengpi': '新春大吉', 'sl': '春风入喜财入户', 'xl': '岁月更新福满门',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%96%B0%E6%98%A5%E5%A4%A7%E5%90%89-%E6%98%A5%E9%A3%8E%E5%85%A5%E5%96%9C%E8%B4%A2%E5%85%A5%E6%88%B7-%E5%B2%81%E6%9C%88%E6%9B%B4%E6%96%B0%E7%A6%8F%E6%BB%A1%E9%97%A8.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A36%3A37Z%2F-1%2F%2F0c480fb986598bcea3979a97203f09097c9044e021c0939920e4f02ed799ac14'},
    {'hengpi': '欢度春节', 'sl': '红梅含苞傲冬雪', 'xl': '绿柳吐絮迎新春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%AC%A2%E5%BA%A6%E6%98%A5%E8%8A%82-%E7%BA%A2%E6%A2%85%E5%90%AB%E8%8B%9E%E5%82%B2%E5%86%AC%E9%9B%AA-%E7%BB%BF%E6%9F%B3%E5%90%90%E7%B5%AE%E8%BF%8E%E6%96%B0%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A37%3A48Z%2F-1%2F%2F1b9e80fa0a53cc9742fdc3cb64012f91c7feb3b74d30b8903760b9848fecb34a'},
    {'hengpi': '万象更新', 'sl': '和顺一门有百福', 'xl': '平安二字值千金',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E4%B8%87%E8%B1%A1%E6%9B%B4%E6%96%B0-%E5%92%8C%E9%A1%BA%E4%B8%80%E9%97%A8%E6%9C%89%E7%99%BE%E7%A6%8F-%E5%B9%B3%E5%AE%89%E4%BA%8C%E5%AD%97%E5%80%BC%E5%8D%83%E9%87%91.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A40%3A49Z%2F-1%2F%2Ff3d79f465bf2247494bf30368f084551daa20bbf2980910df477d11297dc5bd1'},
    {'hengpi': '家和万事兴', 'sl': '一年四季行好运', 'xl': '喜气洋洋伴福来',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%AE%B6%E5%92%8C%E4%B8%87%E4%BA%8B%E5%85%B4-%E4%B8%80%E5%B9%B4%E5%9B%9B%E5%AD%A3%E8%A1%8C%E5%A5%BD%E8%BF%90-%E5%96%9C%E6%B0%94%E6%B4%8B%E6%B4%8B%E4%BC%B4%E7%A6%8F%E6%9D%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A42%3A45Z%2F-1%2F%2F15f5774329da31cd90308f1964d9de780934e1e254e5a846fdf9a9826423283e'},
    {'hengpi': '春意盎然', 'sl': '迎新春江山锦绣', 'xl': '辞旧岁事泰辉煌',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%98%A5%E6%84%8F%E7%9B%8E%E7%84%B6-%E8%BF%8E%E6%96%B0%E6%98%A5%E6%B1%9F%E5%B1%B1%E9%94%A6%E7%BB%A3-%E8%BE%9E%E6%97%A7%E5%B2%81%E4%BA%8B%E6%B3%B0%E8%BE%89%E7%85%8C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A45%3A06Z%2F-1%2F%2Fc7c00ee840e83430ac82b2a730e651730626c2f6a90a1694af8ff9aff559f98a'},
    {'hengpi': '皆大欢喜', 'sl': '岁通盛世家家富', 'xl': '人遇年华个个欢',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E7%9A%86%E5%A4%A7%E6%AC%A2%E5%96%9C-%E5%B2%81%E9%80%9A%E7%9B%9B%E4%B8%96%E5%AE%B6%E5%AE%B6%E5%AF%8C-%E4%BA%BA%E9%81%87%E5%B9%B4%E5%8D%8E%E4%B8%AA%E4%B8%AA%E6%AC%A2.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A48%3A22Z%2F-1%2F%2F03814a7a83839bdf5f0d483dde93e00d3166287c5874cd868cebf314846b0302'},
    {'hengpi': '心想事成', 'sl': '高居宝地财兴旺', 'xl': '福照家门富生辉',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%BF%83%E6%83%B3%E4%BA%8B%E6%88%90-%E9%AB%98%E5%B1%85%E5%AE%9D%E5%9C%B0%E8%B4%A2%E5%85%B4%E6%97%BA-%E7%A6%8F%E7%85%A7%E5%AE%B6%E9%97%A8%E5%AF%8C%E7%94%9F%E8%BE%89.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A49%3A51Z%2F-1%2F%2F146bf9af7ae3ed78e3394a279e882cf77341566eb1382ff77d942c72c77cb826'},
    {'hengpi': '家和万事兴', 'sl': '一年四季行好运', 'xl': '八方财宝进家门',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%AE%B6%E5%92%8C%E4%B8%87%E4%BA%8B%E5%85%B4-%E4%B8%80%E5%B9%B4%E5%9B%9B%E5%AD%A3%E8%A1%8C%E5%A5%BD%E8%BF%90-%E5%85%AB%E6%96%B9%E8%B4%A2%E5%AE%9D%E8%BF%9B%E5%AE%B6%E9%97%A8.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T01%3A52%3A09Z%2F-1%2F%2F00e7fc2130e806a389a909ad5e85b4a761a996ad51cd1b4b8202615ddbc1db29'},
    {'hengpi': '恭贺新春', 'sl': '五更分二年年年称心', 'xl': '一夜连两岁岁岁如意',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%81%AD%E8%B4%BA%E6%96%B0%E6%98%A5-%E4%BA%94%E6%9B%B4%E5%88%86%E4%BA%8C%E5%B9%B4%E5%B9%B4%E5%B9%B4%E7%A7%B0%E5%BF%83-%E4%B8%80%E5%A4%9C%E8%BF%9E%E4%B8%A4%E5%B2%81%E5%B2%81%E5%B2%81%E5%A6%82%E6%84%8F.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A00%3A05Z%2F-1%2F%2F67e1e2a921fc990da43e593f7bd9bda71b855a05df38c398a00c9afb3d02c393'},
    {'hengpi': '欢度春节', 'sl': '春满人间百花吐艳', 'xl': '福临小院四季常安',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%AC%A2%E5%BA%A6%E6%98%A5%E8%8A%82-%E6%98%A5%E6%BB%A1%E4%BA%BA%E9%97%B4%E7%99%BE%E8%8A%B1%E5%90%90%E8%89%B3-%E7%A6%8F%E4%B8%B4%E5%B0%8F%E9%99%A2%E5%9B%9B%E5%AD%A3%E5%B8%B8%E5%AE%89.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A03%3A14Z%2F-1%2F%2F82da08aa1e0a2f3198064344fb482b901c8bab6fbcf01fc1fa88e9ad1d137adc'},
    {'hengpi': '年年有余', 'sl': '千年迎新春', 'xl': '瑞雪兆丰年',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%B9%B4%E5%B9%B4%E6%9C%89%E4%BD%99-%E5%8D%83%E5%B9%B4%E8%BF%8E%E6%96%B0%E6%98%A5-%E7%91%9E%E9%9B%AA%E5%85%86%E4%B8%B0%E5%B9%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A06%3A55Z%2F-1%2F%2F0e37862f7b1dada52665fb372955610ac4bcd0f52560273433a12cd7cdb48b2a'},
    {'hengpi': '辞旧迎新', 'sl': '旧岁又添几个喜', 'xl': '新年更上一层楼',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E8%BE%9E%E6%97%A7%E8%BF%8E%E6%96%B0-%E6%97%A7%E5%B2%81%E5%8F%88%E6%B7%BB%E5%87%A0%E4%B8%AA%E5%96%9C-%E6%96%B0%E5%B9%B4%E6%9B%B4%E4%B8%8A%E4%B8%80%E5%B1%82%E6%A5%BC.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A08%3A36Z%2F-1%2F%2Faf6ffa76214d5260b61e3d6b72dc01fa8b1e6ea0166f30185bdf4163a791cfd6'},
    {'hengpi': '家庭幸福', 'sl': '欢天喜地度佳节', 'xl': '张灯结彩迎新春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E5%AE%B6%E5%BA%AD%E5%B9%B8%E7%A6%8F-%E6%AC%A2%E5%A4%A9%E5%96%9C%E5%9C%B0%E5%BA%A6%E4%BD%B3%E8%8A%82-%E5%BC%A0%E7%81%AF%E7%BB%93%E5%BD%A9%E8%BF%8E%E6%96%B0%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A10%3A40Z%2F-1%2F%2Fa495a7c890cb46365e11f62b24e6f472d20db62b4a011d8e6634aef0ee9e08cd'},
    {'hengpi': '春意盎然', 'sl': '春雨丝丝润万物', 'xl': '万事如意福临门',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%98%A5%E6%84%8F%E7%9B%8E%E7%84%B6-%E6%98%A5%E9%9B%A8%E4%B8%9D%E4%B8%9D%E6%B6%A6%E4%B8%87%E7%89%A9-%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F%E7%A6%8F%E4%B8%B4%E9%97%A8.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A12%3A07Z%2F-1%2F%2Fca519b24d4f2cbf8c6f7f5b5c3a57df86ae0305d032068a12a38f4f412246dae'},
    {'hengpi': '财源广进', 'sl': '一帆风顺吉星到', 'xl': '万事如意福临门',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E8%B4%A2%E6%BA%90%E5%B9%BF%E8%BF%9B-%E4%B8%80%E5%B8%86%E9%A3%8E%E9%A1%BA%E5%90%89%E6%98%9F%E5%88%B0-%E4%B8%87%E4%BA%8B%E5%A6%82%E6%84%8F%E7%A6%8F%E4%B8%B4%E9%97%A8.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A13%3A48Z%2F-1%2F%2Ff408582367d108be0f2458ef15c101440c152bdf5e62c014a2da9ec1b2cc7eeb'},
    {'hengpi': '春意盎然', 'sl': '福星高照全家福', 'xl': '春光耀辉满堂春',
     'url': 'http://dbp-resource.gz.bcebos.com/82aa3cd7-7053-aece-7dc5-65116aec1392/%E6%98%A5%E6%84%8F%E7%9B%8E%E7%84%B6-%E7%A6%8F%E6%98%9F%E9%AB%98%E7%85%A7%E5%85%A8%E5%AE%B6%E7%A6%8F-%E6%98%A5%E5%85%89%E8%80%80%E8%BE%89%E6%BB%A1%E5%A0%82%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-12-15T02%3A15%3A27Z%2F-1%2F%2Fd6aad5fbf87ae322dc6ff9ae58ab46e9785a42bb9d7f2b2998efa7f99defca69'}
]

if __name__ == '__main__':
    from datetime import date

    print((date(2018, 12, 16) - date.today()).days)
    # djs = dao_ji_shi()
    # print(djs[1])
    # print(random.randint(0, len(datas)-1))
    # print(-1>-10)
    print(datetime.now() - datetime(2019,2,5))
    pass
