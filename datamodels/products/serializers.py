#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 上午10:39
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.products.models import VirtualService, mm_VirtualService
from lib.fields import JsonField


class BaseVirtualServiceSerializer(serializers.ModelSerializer):
    pricelist = JsonField()


class VirtualServiceSerializer(BaseVirtualServiceSerializer):

    def validate_pricelist(self, value):
        mm_VirtualService.check_pricelist_format(value)
        return value

    class Meta:
        model = VirtualService
        fields = '__all__'
