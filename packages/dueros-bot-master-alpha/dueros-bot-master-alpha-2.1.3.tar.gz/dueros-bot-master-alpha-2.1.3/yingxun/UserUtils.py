#!/usr/bin/env python3
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

conn = redis.Redis('106.12.27.65', port=7379, password='yaserongyao123', decode_responses=True, db=0)


def add_user(device_id, user_info, location=''):
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
        update_user_info(device_id, user_info, location)
    else:
        user_info['deviceId'] = device_id
        user_info['location'] = location
        # info = {
        #     'deviceId': device_id,
        #     'nick_name': nick_name,
        #     'phone': phone,
        #     'email': email,
        #     'portrait': portrait,
        #     'locationInfo': location
        # }
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

class A:
    def a(self, name):
        print('a')
if __name__ == '__main__':

    b = A()
    a = b.a.__code__.co_argcount
    print(a)
    # add_user('111111111',{'nickname':'test', 'phone':'18201634025', 'protail':'http://'},'北京')

    def a():
        def b():
            print('b')
        return b()
    a()
    pass