#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 下午2:03
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : fields.py
from rest_framework import fields
from rest_framework.utils import json


class JsonField(fields.JSONField):

    def __init__(self, *args, **kwargs):
        self.binary = kwargs.pop('binary', True)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            json.dumps(data)
        except (TypeError, ValueError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            self.fail('invalid')
