#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 上午12:39
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : handlers.py
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['status_code'] = response.status_code

    return response

