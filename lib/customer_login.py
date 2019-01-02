#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 上午10:31
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : customer_login.py
import time
from datetime import datetime

from django.contrib.auth import login as system_login
from django.core.cache import cache

from lib.common import CacheKey, HeadersKey


def login(request, user):
    system_login(request, user)
    request.session['user_id'] = user.id
    request.session['customer_id'] = user.customer.id
    last_requst_at = time.mktime(datetime.now().timetuple())
    request.session['last_requst_at'] = last_requst_at
    key = CacheKey.customer_last_request % user.customer.id
    cache.set(key, last_requst_at, 2 * 7 * 24 * 60 * 60)
    latitude = float(request.META.get(HeadersKey.HTTP_LATITUDE, 0))
    longitude = float(request.META.get(HeadersKey.HTTP_LONGITUDE, 0))
    user.customer.latitude = latitude
    user.customer.longitude = longitude
    user.customer.save()

