#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/11/18

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
from yingxun.DBUtils import UserDao , User

conn = None
try:
    conn = redis.Redis('106.12.27.65', port=7379, password='yaserongyao123', decode_responses=True, db=0)
except Exception as e:
    print(e)
    logging.error('redis 不可用了')
    pass


def add_user(device_id, user_info, location=None):
    """
    添加用户信息
    :param device_id:
    :param nick:
    :param phone:
    :param address:
    :param location:
    :return:
    """
    KEY = 'USER:INFO:DEVICE:%s' % device_id
    if conn.exists(KEY):
        user_dao = UserDao()
        user = User()
        user.device_id = device_id
        user.nick_name = user_info['nickname']
        user.phone = user_info['phone']
        user.protrait = user_info['portrait']
        user.location = location
        user_dao.update_user_by_device_id(user)
        update_user_info(device_id, user_info, location)
    else:
        user_info['deviceId'] = device_id
        user_info['location'] = location
        conn.setnx(KEY, json.dumps(user_info))


def update_user_info(device_id, user_info, location):
    KEY = 'USER:INFO:DEVICE:%s' % device_id
    user_info['deviceId'] = device_id
    user_info['location'] = location
    conn.set(KEY, json.dumps(user_info))


def get_user_info(device_id):
    """
    获取用户信息
    :param device_id:
    :return:
    """
    KEY = 'USER:INFO:DEVICE:%s' % device_id
    data = conn.get(KEY)
    if data:
        return json.loads(data)
    else:
        return None


def is_first(device_id):
    """
    是否首次使用
    :param device_id:
    :return:
    """
    KEY = 'USER:INFO:DEVICE:%s' % device_id
    if conn.exists(KEY):
        return False
    else:
        return True


def add_last_location(device_id, location):
    KEY = 'USER:INFO:DEVICE:LAST_LOCATION'
    conn.hset(KEY, str(device_id), str(location))


def get_last_location(device_id):
    KEY = 'USER:INFO:DEVICE:LAST_LOCATION'
    location = conn.hget(KEY, str(device_id))
    return location

if __name__ == '__main__':

    # add_user('111111111',{'nickname':'test', 'phone':'18201634025', 'protail':'http://'},'北京')

    pass