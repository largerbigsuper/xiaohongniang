#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午6:21
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : tools.py
import json
from math import cos, sin, asin, pi

from rest_framework.exceptions import ParseError
from rest_framework.request import Request


class Tool:

    @staticmethod
    def required_params(request: Request, required_params: list) -> None:
        if isinstance(required_params, str):
            _params = [required_params]
        else:
            _params = required_params
        data_dict = request.query_params if request.method == 'GET' else request.data
        lacked_params = [key for key in _params if key not in data_dict.keys()]
        if lacked_params:
            raise ParseError('%s参数缺少' % lacked_params)

    @staticmethod
    def param_in_options(request: Request, key, options):
        data_dict = request.query_params if request.method == 'GET' else request.data
        value = data_dict.get(key)
        if not value:
            return
        if isinstance(options, (list, tuple)):
            if value not in options:
                raise ParseError('%s可选值为：%s' % (key, options))
        else:
            return

    @staticmethod
    def param_is_json(request, key):
        data_dict = request.query_params if request.method == 'GET' else request.data
        try:
            result = json.loads(data_dict.get(key, '[]'))
            if not isinstance(result, (dict, list)):
                raise ParseError('%s格式应为json' % key)
        except:
            raise ParseError('%s格式应为json' % key)

    @staticmethod
    def format_data(data=None, msg='OK'):
        _data = {
            'msg': msg,
            'data': data
        }
        return _data

    @staticmethod
    def get_lon_lat_range(lat, lng, distance):
        """
        计算精度，维度范围
        :param lat: 纬度
        :param lng: 经度
        :param distance: 范围距离
        :return:
        """
        r = 6371  # 地球半径千米
        distance /= 1000
        dlng = 2 * asin(sin(distance / (2 * r)) / cos(lat * pi / 180))
        dlng = dlng * 180 / pi
        dlat = distance/r
        dlat = dlat * 180 / pi
        return sorted((lat - dlat, lat + dlat)), sorted((lng - dlng, lng + dlng))
        # left - top: (lat + dlat, lng - dlng)
        # right - top: (lat + dlat, lng + dlng)
        # left - bottom: (lat - dlat, lng - dlng)
        # right - bottom: (lat - dlat, lng + dlng)
