#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午11:31
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : exceptions.py
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class SMSExcecption(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('获取验证码失败')
    default_code = '获取验证码失败'


class LoginException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('账号或密码不正确')
    default_code = '账号或密码不正确'


class DBException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('数据异常')
    default_code = '数据异常'


class ParamException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('参数错误')
    default_code = '参数错误'
