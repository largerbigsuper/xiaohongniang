#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 下午5:35
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
import json

from rest_framework import serializers

from datamodels.moments.models import Moments
from datamodels.role.serializers import CoustomerBaseInfoSerializer


class MomentsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(source='images')

    def get_images(self, obj):
        return json.loads(obj.images)

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude', 'create_at', 'update_at')


class MomentsDetailSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer()
    images = serializers.SerializerMethodField(source='images')

    def get_images(self, obj):
        return json.loads(obj.images)

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude', 'create_at', 'update_at', 'customer')






