#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午9:33
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : middleware.py
import datetime
import json
import time

from django.core.cache import cache
from rest_framework.authentication import SessionAuthentication

from lib.common import CacheKey, HeadersKey


class ResponseFormateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # 最近访问更新
        if request.user.is_authenticated:
            customer_id = request.session.get('customer_id')
            if not customer_id:
                if request.user.customer:
                    request.session['customer_id'] = request.user.customer.id
            _now = time.mktime(datetime.datetime.now().timetuple())
            _last = request.session.get('last_requst_at')
            customer_id = request.session['customer_id']
            key = CacheKey.customer_last_request % customer_id
            cache.set(key, _now, 2 * 7 * 24 * 60 * 60)
            if isinstance(_last, datetime.datetime):  # 数据库中读取的session是datetime格式，需进行转化；redis中不能存储datetime格式数据
                _last = time.mktime(_last.timetuple())
                request.session['last_requst_at'] = _last
            if _last:
                if _last + 5 * 60 < _now:
                    request.session['last_requst_at'] = _now
                    request.user.customer.last_request_at = datetime.datetime.fromtimestamp(_now)
                    request.user.customer.save()
            else:
                request.session['last_requst_at'] = _now
                request.user.customer.last_request_at = datetime.datetime.fromtimestamp(_now)
                latitude = float(request.META.get(HeadersKey.HTTP_LATITUDE, 0))
                longitude = float(request.META.get(HeadersKey.HTTP_LONGITUDE, 0))
                request.user.customer.latitude = latitude
                request.user.customer.longitude = longitude
                request.user.customer.save()

        return response

    # def process_exception(self, request, exception):
        # if isinstance(exception, LVError):
        #     return JsonResponse(dict(code=exception.code, msg=exception.msg))
        # else:
        #     return None


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return
