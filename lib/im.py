#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/9 下午7:39
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : im.py
from rest_framework.exceptions import APIException
from rongcloud import RongCloud

from LV.settings import RongYunSettings


class IMServe:
    app_key = RongYunSettings.APP_KEY
    app_secret = RongYunSettings.APP_SECRET
    server = RongCloud(app_key, app_secret)

    @classmethod
    def gen_token(cls, user_id, name, avatar_url='https://www.rongcloud.cn/images/logo.png'):
        """
        生成融云token
        >>> import os
        >>> from rongcloud import RongCloud
        >>> app_key = os.environ['APP_KEY']
        >>> app_secret = os.environ['APP_SECRET']
        >>> rcloud = RongCloud(app_key, app_secret)
        :param user_id: 用户user_id, 融云内唯一标识
        :param name: 用户名
        :param avatar_url: 头像地址
        :return:
        """
        response = cls.server.User.getToken(userId=user_id, name=name, portraitUri=avatar_url)
        if response.status == 200:
            return {'token': response.result['token']}
        else:
            raise APIException(response.result['errorMessage'])

    @classmethod
    def refresh_token(cls, user_id, name, avatar_url='https://www.rongcloud.cn/images/logo.png'):
        response = cls.server.User.refresh(userId=user_id, name=name, portraitUri=avatar_url)
        if not response.status == 200:
            raise APIException(response.result['errorMessage'])

    @classmethod
    def create_group(cls, customer_id, group_id, group_name):
        response = cls.server.Group.create(customer_id, group_id, group_name)
        if not response.status == 200:
            raise APIException(response.result['errorMessage'])

    @classmethod
    def destory_group(cls, customer_id, group_id):
        cls.server.Group.dismiss(customer_id, group_id)

    @classmethod
    def join_group(cls, customer_id, group_id, group_name):
        response = cls.server.Group.join(customer_id, group_id, group_name)
        if not response.status == 200:
            raise APIException(response.result['errorMessage'])

    @classmethod
    def leave_group(cls, user_id, group_id):
        response = cls.server.Group.quit(user_id, group_id)
        if not response.status == 200:
            raise APIException(response.result['errorMessage'])
