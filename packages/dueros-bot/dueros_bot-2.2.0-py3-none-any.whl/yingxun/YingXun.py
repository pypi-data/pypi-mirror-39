#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/11/16

"""
    desc:pass
"""

import logging
import json
import urllib2
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.BodyTemplate3 import BodyTemplate3
from dueros.directive.Display.Hint import Hint
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem
from dueros.directive.Display.PushStack import PushStack
from dueros.directive.VideoPlayer.Play import VideoPlayer
from dueros.directive.Display.RenderVideoList import RenderVideoList
from dueros.directive.Display.media.VideoItem import VideoItem
from dueros.directive.Permission.AskForPermissionsConsent import AskForPermissionsConsent
from dueros.directive.Permission import PermissionEnum
from dueros.directive.AudioPlayer import PlayBehaviorEnum
from dueros import Utils
from yingxun import MovieUtils
from yingxun import UserUtils


class YingXun(Bot):

    def __init__(self, request_data):
        super(YingXun, self).__init__(request_data)
        self.add_launch_handler(self.handle_launcher)
        #权限
        self.add_permission_granted_event(self.handle_permission_granted)
        self.add_permission_rejected_event(self.handle_permission_rejected)

        #意图
        self.add_intent_handler('com.jack.dbp.movie.where', self.handle_movie_where)
        self.add_intent_handler('com.jack.dbp.movie.index', self.handle_movie_index)
        self.add_intent_handler('com.jack.dbp.movie.actor_list', self.handle_movie_actor_list)
        self.add_intent_handler('com.jack.dbp.movie.trailer', self.handle_movie_trailer)

        #事件
        self.add_event_listener('Display.ElementSelected', self.handle_screen_click)
        self.add_event_listener('Form.ButtonClicked', self.handle_form_button_click)
        self.add_event_listener('VideoPlayer.PlaybackStarted', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackStopped', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackPaused', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackFinished', self.handle_video_playback_finished)
        self.add_event_listener('VideoPlayer.PlaybackNearlyFinished', self.handle_video_playback_nearly_finished)

        self.add_intent_handler('ai.dueros.common.default_intent', self.handle_default_intent)
        self.add_intent_handler('ai.dueros.common.stop_intent', self.ended)
        self.add_session_ended_handler(self.ended)

    def handle_launcher(self):
        logging.info('技能启动')
        api_access_token = self.get_api_access_token()
        self.set_session_attribute('api_access_token', api_access_token, '')
        #用户授权
        deviceId = self.request.get_device_id()
        #判断是否首次使用
        is_first = UserUtils.is_first(deviceId)
        is_support_display = self.is_support_display()
        logging.info('技能启动  deviceId = %s, is_first = %s, is_support_display =%s' % (deviceId, is_first, is_support_display))
        if is_first:
            #获取授权
            ask_permissions = AskForPermissionsConsent()
            ask_permissions.add_permission(PermissionEnum.PERMISSION_USER_INFO)
            # ask_permissions.add_permission(PermissionEnum.PERMISSION_LOCATION)
            return {
                'directives': [ask_permissions]
            }
        else:
            return self.__not_first_incoming(deviceId)

    def __first_incoming(self):
        """
        首次使用
        :return:
        """
        self.wait_answer()
        is_support_display = self.is_support_display()
        if is_support_display:
            directives = build_body_template1_directives('最新影讯',
                '请您告诉我要查看哪里的影讯。比如:查看北京的', ['查看北京的', '查看上海的'])
            return {
                'directives': directives,
                'outputSpeech': '欢迎使用最新影讯，请您告诉我要查看哪里的影讯。比如:查看北京的 或 对我说:"帮助"'
            }
        else:
            card = TextCard('欢迎使用最新影讯，请您告诉我要查看哪里的影讯。比如:查看北京的 或 对我说:"帮助"')
            return {
                'card': card,
                'outputSpeech': '欢迎使用最新影讯，请您告诉我要查看哪里的影讯。比如:查看北京的 或 对我说:"帮助"'
            }

    def __not_first_incoming(self, device_id):
        """
        非首次
        :param device_id:
        :return:
        """
        self.wait_answer()
        user_info = UserUtils.get_user_info(device_id)
        city = user_info['locationInfo']
        logging.info('用户非首次使用 地理位置=%s' % city)
        return self.__build_movies_by_city(city)

    def handle_permission_granted(self, event):
        print('handle_permission_granted', event)
        urllib2.disable_warnings()
        api_session_token = self.get_session_attribute('api_access_token', '')
        token = 'bearer ' + api_session_token
        print(token)
        headers = {
            'authorization': token
        }
        http = urllib2.PoolManager()
        r = http.request('GET', 'https://xiaodu.baidu.com/saiya/v1/user/profile', headers=headers)

        result = str(r.data, 'utf-8')
        user_info = json.loads(result)
        UserUtils.add_user(self.request.get_device_id(), user_info, '北京')
        print(str(r.data, 'utf-8'))
        logging.info("授权结果:" + str(r.data, 'utf-8'))
        return self.__first_incoming()

    def handle_permission_rejected(self, event):
        print('handle_permission_rejected', event)
        pass

    def handle_movie_where(self):
        """
        :return:
        """
        #根据地理位置获取信息
        self.wait_answer()
        self.clear_session_attribute()
        city = self.get_slots('city')
        if not city:
            self.ask('city')
            card = TextCard('请您告诉我要查看哪个城市的影讯,比如:查看北京的')
            return {
                'card': card,
                'outputSpeech': '请您告诉我要查看哪个城市的影讯,比如:查看北京的'
            }
        else:
            orgion_city = json.loads(city)
            print(orgion_city)
            city_name = orgion_city['city']
            print(city_name)
            return self.__build_movies_by_city(city_name)

    def handle_movie_actor_list(self):
        self.wait_answer()
        self.set_expect_speech(False)
        movie_detail = self.get_session_attribute('current_detail', '')
        if movie_detail:
            movie = self.get_session_attribute('current_movie', '')
            return build_movie_actor_list(self.is_support_display(), movie, movie_detail)
        else:
            return {
                'outputSpeech': '您还未查看任何电影,请您先选择电影。比如:查看北京的 来查看影讯列表或对我说:帮助'
            }

    def handle_screen_click(self, event):
        self.wait_answer()
        if event:
            token = event['token']
            values = token.split(':')
            token_type = values[0]
            token_value = values[1]
            if token_type == 'movie':
                return self.__build_movie_detail_by_index(token_value)

    def handle_form_button_click(self, event):
        """
        播放页面的点击事件
        :param event:
        :return:
        """
        self.wait_answer()
        self.set_expect_speech(False)
        if event:
            print('handle_form_button_click:', event)
            button_name = event['name']
            if 'SHOW_PLAYLIST' == button_name:
                return self.build_video_list()
            elif 'NEXT' == button_name or 'PREVIOUS' == button_name:
                pass
                # return self.build_prev_next(button_name)
            elif 'PAUSE' == button_name:
                pass
            pass

    def __build_movies_by_city(self, city):
        """
        根据用户地理位置获取信息
        :param city:
        :return:
        """
        result = MovieUtils.spider_now_plaing(city)
        if isinstance(result, str):
            output_speech = '%s, 比如:查看北京的' % result
            card = TextCard(output_speech)
            return {
                'card': card,
                'outputSpeech': output_speech
            }
        elif isinstance(result, list):
            self.set_session_attribute('city', city, '')
            self.set_session_attribute('movies', result, '')
            if self.is_support_display():
                directives = build_movie_list_template(city + '的影讯', result)
                movie_list = ''
                count = 0
                for m in result:
                    if count > 5:
                        break
                    movie_list = movie_list + ',' + m['title']
                    count = count + 1

                output_speech = '%s 正在热映的电影有%s等,您可以对我说:查看第一个,来查看电影的详情' % (city, movie_list)
                directives.append(PushStack())
                return {
                    'directives': directives,
                    'outputSpeech': output_speech
                }
            else:
                movie_list = ''
                show_list = ''
                count = 1
                for m in result:
                    movie_list = movie_list + ('第%s个:' % count) + m['title']
                    show_list += ('第%s个:' % count) + m['title'] + '<silence time="1s"></silence>'
                    count = count + 1

                cardshow = '%s正在热映的电影依次如下:%s ,您可以对我说:查看第一个,来查看电影的详情' % (city, movie_list)
                output_speech = '<speak>%s正在热映的电影依次如下:%s ,您可以对我说:查看第一个,来查看电影的详情</speak>' % (city, show_list)

                card = TextCard(cardshow)
                return {
                    'card': card,
                    'outputSpeech': output_speech
                }

    def handle_movie_index(self):
        self.wait_answer()
        move_index = self.get_slots('move_index')
        if not move_index:
            self.ask('move_index')
            return {
                'outputSpeech': '请您告诉我要查看第几个电影的影讯,比如:查看第一个'
            }
        return self.__build_movie_detail_by_index(move_index)

    def __build_movie_detail_by_index(self, index):
        movies = self.get_session_attribute('movies', [])
        if int(index) > len(movies):
            return {
                'outputSpeech': '抱歉您要查看的超出的列表所展示的，请您重新告诉我查看第几个'
            }
        movie = movies[int(index) - 1]
        self.set_session_attribute('current_movie', movie, '')
        return self.build_movie_detail(movie['title'], movie, True)

    def build_movie_detail(self, title, movie, outputSpeech=True):
        """
        :param title:
        :param movie:
        :return:
        """
        if movie:
            detail = self.get_session_attribute('current_detail', None)
            if not detail or movie['title'] != detail['title']:
                detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
            self.set_session_attribute('current_detail', {'id': movie['id'], 'title': title, 'director': detail['director'], 'summary': detail['summary'], 'trailer': detail['trailer'], 'celebritys': detail['celebritys']}, '')
            self.clear_session_field('movie:trailer:index')
            self.clear_session_field('movie:trailer:count')
            template = BodyTemplate3()
            template.set_title(title)
            template.set_background_image(BG)
            template.set_image(movie['img'])
            content = '导演:' + detail['director'] + "\n" + detail['summary']
            template.set_plain_content(content)
            directive = RenderTemplate(template)
            hint = Hint(['查看演员列表/播放预告片',])
            directives = []
            directives.append(hint)
            directives.append(directive)
            push_stack = PushStack()
            directives.append(push_stack)

            self.wait_answer()
            if outputSpeech:
                output_speech = movie['title'] + '本片由导演' + detail['director'] + '执导, 剧情简介:' + detail['summary']
                if self.is_support_display():
                    return {
                        'directives': directives,
                        'outputSpeech': output_speech
                    }
                else:
                    card = TextCard(output_speech)
                    city_name = self.get_session_attribute('city', '')
                    if not city_name:
                        output_speech += ',对我说:查看演员列表 来获取主要演员信息 或对我说:返回列表页 来返回影讯列表信息'
                    else:
                        output_speech += ',对我说:查看演员列表 来获取主要演员信息 或对我说:返回列表页来返回%s的影讯信息' % city_name

                    return {
                        'card': card,
                        'outputSpeech': output_speech
                    }
            else:
                # self.set_expect_speech(outputSpeech)
                return {
                    'directives': directives
                }

    def handle_movie_trailer(self):
        """
        查看预告片
        :return:
        """
        self.wait_answer()
        movie_detail = self.get_session_attribute('current_detail', '')
        if movie_detail:
            return self.build_movie_trailer(movie_detail['id'], movie_detail['title'], movie_detail['trailer'])
        else:
            return {
                'outputSpeech': '您还未查看任何电影,请您先选择电影。比如:查看北京的 来查看影讯列表 或对我说:帮助'
            }

    def build_video_list(self):

        movie_detail = self.get_session_attribute('current_detail', '')
        if movie_detail:
            movie_id = movie_detail['id']
            videos = MovieUtils.parse_trailer_video(movie_id, movie_detail['trailer'])
            directive = RenderVideoList(movie_detail['title'])

            for video in videos:
                name = video['name']
                image = video['img']
                item = VideoItem(name, '')
                # item.set_token(Utils.hash_str(video['url']))
                item.set_token('trailer:%s' % video['id'])
                item.set_image(image)
                item.set_media_length_in_milliseconds(video['time'])
                directive.add_video_item(item)

            return {
                'directives': [directive]
            }
        else:
            print('build_video_list movie_detail is None')

    def handle_video_playback_nearly_finished(self, event):
        self.wait_answer()
        self.set_expect_speech(False)

    def handle_video_playback_finished(self, event):
        """
        播放完毕回调
        :param event:
        :return:
        """
        self.wait_answer()
        movie_trailer_count = int(self.get_session_attribute('movie:trailer:count', '0'))
        movie_current_index = int(self.get_session_attribute('movie:trailer:index', '0'))
        if movie_current_index > movie_trailer_count - 1:
            # movie = self.get_session_attribute('current_movie', '')
            # return self.build_movie_detail(movie['title'], movie, False)
            pass
        else:
            movie_detail = self.get_session_attribute('current_detail', '')
            if movie_detail:
                print('movie_detail = ', movie_detail)
                return self.build_movie_trailer(movie_detail['id'], movie_detail['title'], movie_detail['trailer'])
            else:
                print('movie_detail is None')

    def ended(self):
        """
        关闭
        :return:
        """
        self.end_session()
        return {
            'outputSpeech': '欢迎再次使用最新影讯！！'
        }

    def handle_default_intent(self):

        self.wait_answer()
        return {
            'outputSpeech': '抱歉，我没听清，请您再说一次 或 对我说:帮助！！'
        }

    def build_movie_trailer(self, movie_id, title, trailer_url):
        """

        :param title:
        :param trailer_url:
        :return:
        """
        self.wait_answer()
        videos = MovieUtils.parse_trailer_video(movie_id, trailer_url)
        video_length = len(videos)
        if video_length > 0:
            movie_trailer_index = self.get_session_attribute('movie:trailer:index', '-1')
            if movie_trailer_index == '-1':
                movie_trailer_index = 0
                self.set_session_attribute('movie:trailer:index', movie_trailer_index, '0')
                self.set_session_attribute('movie:trailer:count', str(video_length), '0')
            else:
                movie_trailer_index = int(movie_trailer_index) + 1
                self.set_session_attribute('movie:trailer:index', movie_trailer_index, '0')

            self.set_expect_speech(False)
            if movie_trailer_index > 2:
                pass
            video_data = videos[movie_trailer_index]
            video_url = video_data['url']
            video = None
            if movie_trailer_index == 0:
                video = VideoPlayer(video_url)
            else:
                video = VideoPlayer(video_url, PlayBehaviorEnum.REPLACE_ALL)
            video.set_token('trailer:%s' % video_data['id'])
            hint = Hint('返回列表')
            directives = []
            directives.append(hint)
            directives.append(video)
            if movie_trailer_index == 0:
               directives.append(PushStack())
               return {
                   'directives': directives
               }
            else:
                return {
                    'directives': directives
                }
        else:
            outputSpeech = '%s暂无预告片' % title
            return {
                'outputSpeech': outputSpeech
            }


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


def build_movie_list_template(title, datas):

    template = ListTemplate2()
    template.set_title(title)
    template.set_background_image(BG)
    count = 1
    for movie in datas:
        item = ListTemplateItem()
        item.set_image(movie['img'])
        item.set_plain_primary_text(movie['title'])
        score = '评分:%s / 标星:%s' % (movie['score'], movie['star'])
        item.set_plain_secondary_text(score)
        token = 'movie:%s' % count
        item.set_token(token)
        template.add_item(item)
        count = count + 1

    directive = RenderTemplate(template)
    hint = Hint(['查看第一个'])
    directives = []
    directives.append(hint)
    directives.append(directive)
    return directives


def build_movie_actor_list(is_support_display, movie, movie_detail):
    """
    查看演员列表
    :param movie:
    :return:
    """
    celebritys = movie_detail['celebritys']
    if not is_support_display:
        output_speech = movie['title'] + '的演员列表'
        for celebrity in celebritys:
            output_speech += '%s %s,' % (celebrity['name'], celebrity['role'])
        output_speech += ',您可以对我说:查看北京的 来获取北京的影讯信息 或 对我说:返回列表页面'
        card = TextCard(output_speech)
        return {
            'card': card,
            'outputSpeech': output_speech
        }

    else:
        template = ListTemplate1()
        title = movie['title'] + '的演员列表'
        template.set_title(title)
        template.set_background_image(BG)
        for celebrity in celebritys:
            item = ListTemplateItem()
            item.set_image(celebrity['avatar'])
            item.set_plain_primary_text(celebrity['name'])
            item.set_plain_secondary_text(celebrity['role'])
            token = 'actor:'
            item.set_token(token)
            template.add_item(item)

        directive = RenderTemplate(template)
        hint = Hint(['查看北京的'])
        directives = []
        directives.append(hint)
        directives.append(directive)
        directives.append(PushStack())
        outputSpeech = title
        return {
            'directives': directives,
            'outputSpeech': outputSpeech
        }



BG ='http://dbp-resource.gz.bcebos.com/5e20a761-64be-4431-e14e-f75b65107eb7/0008020498701976_b.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-08-31T12%3A47%3A13Z%2F-1%2F%2F97034e75331cbf794bb6c3e1915261e4114cad9e9ffbb4bacf51078ef9ff8efc'

if __name__ == '__main__':
    pass