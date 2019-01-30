#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午6:21
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : tools.py
import json
import random
import string
from collections import defaultdict
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


def get_filename(filename):
    return filename.upper()


Flags = {'A', 'B', 'C', 'D', 'E', 'F'}


Char_Integer_Mapping = {c: ord(c) % 10 for c in set(string.ascii_uppercase) - Flags}
Integer_Char_Mapping = defaultdict(list)
[Integer_Char_Mapping[v].append(k) for k, v in Char_Integer_Mapping.items()]

"""
{4: ['T', 'J'],
 1: ['G', 'Q'],
 3: ['S', 'I'],
 0: ['P', 'Z'],
 6: ['L', 'V'],
 8: ['X', 'N'],
 2: ['R', 'H'],
 5: ['U', 'K'],
 9: ['Y', 'O'],
 7: ['W', 'M']}
"""


def gen_invite_code(customer_id, length=8):
    """
    根据customer_id 生成邀请码
    """
    if not isinstance(customer_id, int):
        raise TypeError('customer_id required a int value.')
    if len(str(customer_id)) > 8:
        raise ValueError('customer_id最大为8位整数')
    id_str = str(customer_id)
    suffix = ''.join([random.choice(Integer_Char_Mapping[int(i)]) for i in list(id_str)])
    prefix = ''.join([random.choice(list(Char_Integer_Mapping.keys())) for _ in range(length - len(suffix) - 1)])
    flag = random.choice(list(Flags))
    code = prefix + flag + suffix
    return code[-8:]


def decode_invite_code(invite_code):
    """
    根据邀请码推出customer_id
    """
    if not isinstance(invite_code, str):
        raise TypeError('invite_code required a str value')
    invite_code = invite_code.upper()
    _flag = list(set(invite_code) & Flags)[0]
    if _flag:
        id_str = invite_code.split(_flag)[-1]
    else:
        id_str = invite_code
    id_integer_str = ''.join([str(Char_Integer_Mapping[k]) for k in id_str])
    return int(id_integer_str)
