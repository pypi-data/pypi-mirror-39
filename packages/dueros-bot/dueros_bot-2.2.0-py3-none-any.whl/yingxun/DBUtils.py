#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018-12-08

"""
    desc:pass
"""
import pymysql


class BaseDao(object):

    def __init__(self):
        self.conn = pymysql.connect('localhost', 'yingxun', '12341234', 'BOT_YINGXUN', charset='utf8')


class UserDao(BaseDao):

    def add_user(self, user):
        """
        添加
        :param user:
        :return:
        """
        if isinstance(user, User):
            cursor = self.conn.cursor()
            sql = 'INSERT INTO TBL_YINGXUN_USER(DEVICE_ID, NICK_NAME, PHONE, PORTRAIT, LOCATION) ' \
                  'VALUES (%s, %s, %s, %s, %s);'
            try:
                cursor.execute(sql, (user.device_id, user.nick_name, user.phone, user.protrait, user.location))
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
            self.conn.close()

    def update_user_by_device_id(self, user):
        """
        更新
        :param user:
        :return:
        """
        if isinstance(user, User):
            cursor = self.conn.cursor()
            sql = 'UPDATE TBL_YINGXUN_USER SET '
            if hasattr(user, 'nick_name') and user.nick_name is not None:
                sql = sql + ' NICK_NAME = %s, ' % user.nick_name
            if hasattr(user, 'phone') and user.phone is not None:
                sql = sql + ' PHONE = %s, ' % user.phone
            if hasattr(user, 'portrait') and user.protrait is not None:
                sql = sql + ' PORTRAIT = %s, ' % user.portrait
            if hasattr(user, 'location') and user.location is not None:
                sql = sql + ' LOCATION = %s ,' % user.location
            sql = sql[0: len(sql) - 2]
            sql = sql + ' WHERE DEVICE_ID = %s' % user.device_id
            try:
                cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)
                self.conn.rollback()
            self.conn.close()

    def select_user_by_device_id(self, device_id):
        """
        查询
        :param device_id:
        :return:
        """
        cursor = self.conn.cursor()
        sql = 'SELECT DEVICE_ID, NICK_NAME, PHONE, PORTRAIT, LOCATION FROM TBL_YINGXUN_USER WHERE DEVICE_ID = %s;'
        cursor.execute(sql, (device_id))
        result = cursor.fetchone()
        cursor.close()
        self.conn.close()
        user = User(result)
        return user


class User(object):

    def __init__(self):
        self.device_id = ''
        self.nick_name = ''
        self.phone = ''
        self.protrait = ''
        self.location = ''

    def __init__(self, args=None):
        if args:
            self.device_id = args[0]
            self.nick_name = args[1]
            self.phone = args[2]
            self.protrait = args[3]
            self.location = args[4]


if __name__ == '__main__':

    user_dao = UserDao()
    # user_dao.select_user_by_device_id('aaa')
    user = User()
    user.device_id = '111'
    user.nick_name = '5555666'
    user.location = None
    # user.phone ='1820123123'
    # user.protrait = 'http://wwww.baidu.com'
    # user.location = '北京'
    # user_dao.add_user(user)
    user_dao.update_user_by_device_id(user)
    # a = 'aaa,dfsdf,'
    # print(a[0: len(a)-1])
    pass