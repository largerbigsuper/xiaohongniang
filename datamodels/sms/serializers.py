#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午7:41
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.sms.models import SMSCode


class SMSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCode
