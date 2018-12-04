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
        lacked_params = [key for key in _params if key not in request.data.keys()]
        if lacked_params:
            raise LVError('缺少参数%s' % lacked_params)
