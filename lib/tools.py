#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午6:21
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : tools.py
from django.core.handlers.wsgi import WSGIRequest

from lib.exceptions import LVError


class Tool:

    @staticmethod
    def required_params(request: WSGIRequest, required_params: list) -> None:
        if isinstance(required_params, str):
            _params = [required_params]
        else:
            _params = required_params
        data_dict = request.query_params if request.method == 'GET' else request.data
        lacked_params = [key for key in _params if key not in data_dict.keys()]
        if lacked_params:
            raise LVError('缺少参数%s' % lacked_params)

    @staticmethod
    def param_in_options(request: WSGIRequest, key, options):
        data_dict = request.query_params if request.method == 'GET' else request.data
        value = data_dict.get(key)
        if not value:
            return
        if isinstance(options, (list, tuple)):
            if value not in options:
                raise LVError('参数%s可选值为：%s' % (key, options))
        else:
            return

    @staticmethod
    def format_data(data=None, msg='OK'):
        _data = {
            'msg': msg,
            'data': data
        }
        return _data
