#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 下午8:29
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers


class SMSSerializer(serializers.Serializer):

    account = serializers.CharField()

