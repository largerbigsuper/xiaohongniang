#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午11:31
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : exceptions.py
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class LVError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Customer Error.')
    default_code = 'customer_error'
