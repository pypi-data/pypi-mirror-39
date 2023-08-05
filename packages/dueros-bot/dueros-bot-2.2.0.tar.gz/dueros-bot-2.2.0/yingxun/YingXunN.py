#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/11/23

"""
    desc:pass
"""
import urllib3
import json
import logging
from dueros.Bot import Bot
from dueros.directive.Permission.AskForPermissionsConsent import AskForPermissionsConsent
from dueros.directive.Permission.PermissionEnum import PermissionEnum
from dueros.card.TextCard import TextCard
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem
from dueros.directive.Display.tag.CustomTag import CustomTag
from dueros.directive.Display.Hint import Hint
from dueros.directive.Display.PushStack import PushStack
from dueros.directive.Display.template.BodyTemplate3 import BodyTemplate3
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.VideoPlayer.Play import VideoPlayer
from dueros.directive.VideoPlayer.Stop import Stop
from dueros.directive.AudioPlayer.PlayBehaviorEnum import PlayBehaviorEnum
from dueros.directive.Display.RenderVideoList import RenderVideoList
from dueros.directive.Display.media.VideoItem import VideoItem
from yingxun import UserUtils
from yingxun import MovieUtils

SESSION_KEY_API_ACCESS_TOKEN = 'session_key_api_access_token'
SESSION_KEY_LOCATION = 'session_key_location'
SESSION_KEY_VIDEO_INDEX = 'session_key_video_index'
SESSION_KEY_VIDEO_COUNT = 'session_key_video_count'

PERMISSION_URL_USER_INFO = 'https://xiaodu.baidu.com/saiya/v1/user/profile'
BOT_BG = 'http://dbp-resource.gz.bcebos.com/5e20a761-64be-4431-e14e-f75b65107eb7/0008020498701976_b.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-08-31T12%3A47%3A13Z%2F-1%2F%2F97034e75331cbf794bb6c3e1915261e4114cad9e9ffbb4bacf51078ef9ff8efc'

SESSION_ENDED_SPEECH = '欢迎您再次使用最新影讯'


class YingXunN(Bot):

    def __init__(self, request_data):
        super(YingXunN, self).__init__(request_data)
        self.add_launch_handler(self.handle_launcher)
        self.add_common_pause_intent_handler(self.handle_pause_intent)
        self.add_common_stop_intent_handler(self.handle_stop_intent)
        self.add_common_next_intent_handler(self.handle_next_intent)
        self.add_common_continue_intent_handler(self.handle_continue_intent)
        self.add_common_default_intent_handler(self.handle_default_intent)
        self.add_session_ended_handler(self.handle_session_ended)
        # 申请权限
        self.add_permission_granted_event(self.permission_granted)
        self.add_permission_rejected_event(self.permission_rejected)
        self.add_permission_grant_failed_event(self.permission_grant_failed)
        #屏幕点击事件
        self.add_display_element_selected(self.handle_display_element_selected)
        self.add_form_button_clicked(self.handle_form_button_click)
        #自动以意图
        self.add_intent_handler('com.jack.dbp.movie.where', self.handle_movie_where)
        self.add_intent_handler('com.jack.dbp.movie.index', self.handle_movie_index)
        self.add_intent_handler('com.jack.dbp.movie.actor_list', self.handle_movie_actor_list)
        self.add_intent_handler('com.jack.dbp.movie.trailer', self.handle_movie_trailer)
        #视频
        self.add_event_listener('VideoPlayer.PlaybackStarted', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackStopped', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackPaused', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackResumed', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackNearlyFinished', self.handle_video_playback_nearly_finished)
        self.add_event_listener('VideoPlayer.PlaybackFinished', self.handle_video_playback_finished)

    def handle_launcher(self):
        """
        技能启动
        :return:
        """
        self.wait_answer()
        self.clear_session_attribute()
        device_id = self.get_device_id()
        is_first = UserUtils.is_first(device_id)
        if is_first:
            self.set_session_attribute(SESSION_KEY_API_ACCESS_TOKEN, self.get_api_access_token(), '')
            return ask_permission()
        else:
            return self.not_first_incoming(device_id)

    def handle_launcher_default(self):
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
            city_name = orgion_city['city']
            UserUtils.add_user(self.get_device_id(), {}, city_name)
            return self.__build_movie_list_by_location(city_name)

    def handle_display_element_selected(self, event):
        """
        屏幕点击事件
        :param event:
        :return:
        """
        if event:
            self.wait_answer()
            # self.set_expect_speech(False)
            token = event['token']
            values = token.split(':')
            token_type = values[0]
            token_value = values[1]
            if token_type == 'movie':
                return self.__build_movie_detail_by_index(token_value)
            elif token_type == 'trailer':
                index = token_value.split('_')[1]
                self.set_session_attribute(SESSION_KEY_VIDEO_INDEX, index, '0')
                return self.__build_movie_trailer()
            else:
                self.set_expect_speech(False)
            pass
        pass

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

    def handle_default_intent(self):
        """
        默认意图
        :return:
        """
        self.wait_answer()
        return {
            'outputSpeech': '抱歉我没听懂，请您再次告诉我'
        }

    def handle_session_ended(self, event):
        """
        技能结束
        :return:
        """
        self.end_session()
        self.clear_session_attribute()
        print('session_ended', event)
        return {
            'outputSpeech': SESSION_ENDED_SPEECH
        }

    def handle_pause_intent(self):
        self.wait_answer()
        self.set_expect_speech(False)
        stop = Stop()
        hint = Hint(['继续播放'])
        print("======handle_pause_intent")
        return {
            'directives': [stop],
            'outputSpeech': '已暂停'
        }

    def handle_stop_intent(self):
        self.wait_answer()
        self.set_expect_speech(False)
        stop = Stop()
        hint = Hint(['继续播放'])
        return {
            'directives': [hint, stop],
            'outputSpeech': '已停止'
        }

    def handle_next_intent(self):
        self.wait_answer()
        self.set_expect_speech(False)
        pass

    def handle_continue_intent(self):
        print("继续播放===handle_continue_intent")
        offset_in_milliseconds = int(self.get_session_attribute('offsetInMilliseconds', '0'))
        movie = self.get_session_attribute('current_movie', '')
        movie_detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
        if movie_detail:
            return self.build_movie_trailer(movie['id'], movie['title'], movie_detail['trailer'], offset_in_milliseconds)
        else:
            return {
                'outputSpeech': '您还未选择任何电影'
            }

    def handle_movie_index(self):
        """
        根据索引返回数据
        :return:
        """
        self.wait_answer()
        move_index = self.get_slots('move_index')
        if not move_index:
            self.ask('move_index')
            return {
                'outputSpeech': '请您告诉我要查看第几个电影的影讯,比如:查看第一个'
            }
        return self.__build_movie_detail_by_index(move_index)

    def handle_movie_actor_list(self):
        self.wait_answer()
        self.set_expect_speech(False)
        movie = self.get_session_attribute('current_movie', '')
        if movie:
            return build_movie_actor_list(self.is_support_display(), movie)
        else:
            return {
                'outputSpeech': '您还未查看任何电影,请您先选择电影。比如:查看北京的 来查看影讯列表或对我说:帮助'
            }
        pass

    def handle_movie_trailer(self):
        self.wait_answer()
        self.set_session_attribute(SESSION_KEY_VIDEO_COUNT, '-1', '-1')
        self.set_session_attribute(SESSION_KEY_VIDEO_INDEX, '0', '')
        return self.__build_movie_trailer()

    def __build_movie_trailer(self):
        movie = self.get_session_attribute('current_movie', '')
        movie_detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
        if movie_detail:
            return self.build_movie_trailer(movie['id'], movie['title'], movie_detail['trailer'])
        else:
            return {
                'outputSpeech': '您还未查看任何电影,请您先选择电影。比如:查看北京的 来查看影讯列表 或对我说:帮助'
            }

    def permission_granted(self, event):
        """
        同意授权
        :param event:
        :return:
        """
        urllib3.disable_warnings()
        api_session_token = self.get_session_attribute(SESSION_KEY_API_ACCESS_TOKEN, '')
        token = 'bearer ' + api_session_token
        headers = {
            'authorization': token
        }
        http = urllib3.PoolManager()
        r = http.request('GET', PERMISSION_URL_USER_INFO, headers=headers)
        result = str(r.data, 'utf-8')
        user_info = json.loads(result)
        device_id = self.get_device_id()
        UserUtils.add_user(device_id, user_info, '北京')
        print(str(r.data, 'utf-8'))
        logging.info("授权结果:" + str(r.data, 'utf-8'))
        self.wait_answer()
        return self.__build_movie_list_by_location('北京')

    def permission_rejected(self, event):
        """
        拒绝授权
        :param event:
        :return:
        """
        self.wait_answer()
        return self.handle_launcher_default()

    def permission_grant_failed(self, event):
        """
        授权失败
        :param event:
        :return:
        """
        self.wait_answer()
        return {
            'outputSpeech': '授权失败，请重新再试'
        }

    def not_first_incoming(self, device_id):
        """
        非首次使用
        :param device_id:
        :return:
        """
        user_info = UserUtils.get_user_info(device_id)
        location = user_info['location']
        return self.__build_movie_list_by_location(location)

    def build_movie_detail(self, title, movie, outputSpeech=True):
        """
        :param title:
        :param movie:
        :return:
        """
        if movie:
            detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
            template = BodyTemplate3()
            template.set_title(title)
            template.set_background_image(BOT_BG)
            template.set_image(movie['img'])
            content = '导演:' + detail['director'] + "\n" + detail['summary']
            template.set_plain_content(content)
            directive = RenderTemplate(template)
            hint = Hint(['查看演员列表/播放预告片'])
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
                        'outputSpeech': output_speech,
                        'reprompt': ''
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
                self.set_expect_speech(outputSpeech)
                return {
                    'directives': directives
                }

    def __build_movie_detail_by_index(self, index):
        location = self.get_session_attribute(SESSION_KEY_LOCATION, '')
        movies = MovieUtils.spider_now_plaing(location)
        if int(index) > len(movies):
            return {
                'outputSpeech': '抱歉您要查看的超出的列表所展示的，请您重新告诉我查看第几个'
            }
        movie = movies[int(index) - 1]
        self.set_session_attribute('current_movie', movie, '')
        return self.build_movie_detail(movie['title'], movie, True)

    def __build_movie_list_by_location(self, location):
        """
        根据地理位置获取最新影讯信息
        :param location:
        :return:
        """
        movie_list = MovieUtils.spider_now_plaing(location)
        if isinstance(movie_list, str):
            output_speech = '%s, 比如:查看北京的' % movie_list
            card = TextCard(output_speech)
            return {
                'card': card,
                'outputSpeech': output_speech
            }
        elif isinstance(movie_list, list):
            self.set_session_attribute(SESSION_KEY_LOCATION, location, '')
            title = '%s 的最新影讯' % location
            if self.is_support_display():
                return build_movie_list_support_display(title, location, movie_list)
            else:
                return build_movie_list_no_display(location, movie_list)

    def build_movie_trailer(self, movie_id, title, trailer_url, offset=0):
        """
        :param movie_id
        :param title:
        :param trailer_url:
        :param offset
        :return:
        """
        self.wait_answer()
        self.set_expect_speech(False)
        videos = MovieUtils.parse_trailer_video(movie_id, trailer_url)
        video_length = len(videos) if videos else -1
        if video_length > 0:
            self.set_session_attribute(SESSION_KEY_VIDEO_COUNT, str(video_length), '0')
            movie_trailer_index = int(self.get_session_attribute(SESSION_KEY_VIDEO_INDEX, '0'))
            video_data = videos[movie_trailer_index]
            video_url = video_data['url']
            video = None
            if movie_trailer_index == 0:
                video = VideoPlayer(video_url)
            else:
                video = VideoPlayer(video_url, PlayBehaviorEnum.REPLACE_ALL)
            video.set_offset_in_milliseconds(offset)
            video.set_token('trailer:%s_%s' % (video_data['id'], movie_trailer_index))
            hint = Hint('返回列表')
            directives = list()
            directives.append(hint)
            directives.append(video)
            if movie_trailer_index == 0:
               directives.append(PushStack())
            return {
                'directives': directives
            }
        else:
            output_speech = '%s暂无预告片' % title
            return {
                'outputSpeech': output_speech
            }

    def build_video_list(self):

        movie = self.get_session_attribute('current_movie', '')
        movie_detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
        if movie_detail:
            movie_id = movie['id']
            videos = MovieUtils.parse_trailer_video(movie_id, movie_detail['trailer'])
            directive = RenderVideoList(movie['title'])
            movie_trailer_index = 0
            for video in videos:
                name = video['name']
                image = video['img']
                item = VideoItem(name, '')
                item.set_token('trailer:%s_%s' % (video['id'], movie_trailer_index))
                item.set_image(image)
                item.set_media_length_in_milliseconds(video['time'])
                directive.add_video_item(item)
                movie_trailer_index = movie_trailer_index + 1
            return {
                'directives': [directive]
            }
        else:
            print('build_video_list movie_detail is None')

    def __save_session_attribute(self, event):
        self.set_session_attribute('offsetInMilliseconds', event['offsetInMilliseconds'], '0')

    def handle_video_playback_nearly_finished(self, event):
        self.wait_answer()
        self.set_expect_speech(False)
        self.__save_session_attribute(event)

    def handle_video_playback_finished(self, event):
        self.wait_answer()
        movie_trailer_count = int(self.get_session_attribute(SESSION_KEY_VIDEO_COUNT, '0'))
        movie_current_index = int(self.get_session_attribute(SESSION_KEY_VIDEO_INDEX, '0'))
        movie_trailer_index = int(movie_current_index) + 1
        self.set_session_attribute(SESSION_KEY_VIDEO_INDEX, str(movie_trailer_index), '0')
        if movie_current_index > movie_trailer_count - 1:
            movie = self.get_session_attribute('current_movie', '')
            self.set_session_attribute('current_movie', movie, '')
            return self.build_movie_detail(movie['title'], movie, False)
        else:
            return self.__build_movie_trailer()


def ask_permission():
    """
    获取用户权限
    :return:
    """
    permission = AskForPermissionsConsent()
    permission.add_permission(PermissionEnum.PERMISSION_USER_INFO)
    return {
        'directives': [permission]
    }


def build_movie_list_support_display(title, location, movie_list):
    directives = build_movie_list_template(title, movie_list)
    brief_speech = ''
    count = 0
    for movie in movie_list:
        if count > 5:
            break
        brief_speech = brief_speech + ',' + movie['title']
        count = count + 1

    output_speech = '%s 正在热映的电影有%s等,您可以对我说:查看第一个,来查看电影的详情' % (location, brief_speech)
    directives.append(PushStack())
    return {
        'directives': directives,
        'outputSpeech': output_speech
    }


def build_movie_list_no_display(city, movie_list):
    brief_speech = ''
    show_list = ''
    count = 1
    for m in movie_list:
        brief_speech = brief_speech + ('第%s个:' % count) + m['title']
        show_list += ('第%s个:' % count) + m['title'] + '<silence time="1s"></silence>'
        count = count + 1
    cardshow = '%s正在热映的电影依次如下:%s ,您可以对我说:查看第一个,来查看电影的详情' % (city, brief_speech)
    output_speech = '<speak>%s正在热映的电影依次如下:%s ,您可以对我说:查看第一个,来查看电影的详情</speak>' % (city, show_list)

    card = TextCard(cardshow)
    return {
        'card': card,
        'outputSpeech': output_speech
    }


def build_movie_list_template(title, datas):

    template = ListTemplate2()
    template.set_title(title)
    template.set_background_image(BOT_BG)
    count = 1
    for movie in datas:
        item = ListTemplateItem()
        item.set_image(movie['img'])
        item.set_plain_primary_text(movie['title'])
        score = '评分:%s / 标星:%s' % (movie['score'], movie['star'])
        item.set_plain_secondary_text(score)
        token = 'movie:%s' % count
        item.set_token(token)
        left_tag = CustomTag('%s分' % movie['score'])
        left_tag.set_background_color('FF0000')
        right_tag = CustomTag('%s' % movie['star'])
        # item.set_image_tags([left_tag, right_tag])
        template.add_item(item)
        count = count + 1

    directive = RenderTemplate(template)
    hint = Hint(['查看第一个'])
    directives = list()
    directives.append(hint)
    directives.append(directive)
    return directives


def build_movie_actor_list(is_support_display, movie):
    """
    查看演员列表
    :param is_support_display
    :param movie:
    :return:
    """
    movie_detail = MovieUtils.spider_movie_detail(movie['id'], movie['detail'])
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
        template.set_background_image(BOT_BG)
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


def build_body_template1_directives(title, content, hint_txt):

    directives = []
    template = BodyTemplate1()
    template.set_title(title)
    template.set_plain_text_content(content)
    template.set_background_image(BOT_BG)
    directive = RenderTemplate(template)
    hint = Hint(hint_txt)
    directives.append(hint)
    directives.append(directive)
    return directives


if __name__ == '__main__':
    import zlib
    import binascii

    print(zlib.crc32(b'0b34edc532618bf9ef195613916b19b1'))
    print(zlib.crc32(b'0b34edc532618bf9ef195613916b19b1')%2)
    pass