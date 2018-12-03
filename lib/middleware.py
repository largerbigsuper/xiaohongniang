#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午9:33
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : middleware.py
from django.http import JsonResponse

from lib.exceptions import LVError


class ResponseFormateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_exception(self, request, exception):
        # if isinstance(exception, LVError):
        #     return JsonResponse(dict(code=exception.code, msg=exception.msg))
        # else:
        #     return None
