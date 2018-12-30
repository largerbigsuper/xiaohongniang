#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午12:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : common.py
from django.db.models import Manager


class CacheKey:
    customer_last_request           = 'lq_%s'  # 最后一次请求时间 customer_id
    user_total                      = 'user_total'  # 用户总数


class BaseManger(Manager, CacheKey):
    pass