#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午7:17
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.bottles.models import Bottle, BottlePickerRelation
from datamodels.role.api.serializers import CustomerBaseInfoSerializer


class BottleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at')


class BottleDetailSerializer(serializers.ModelSerializer):
    customer = CustomerBaseInfoSerializer()

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at', 'customer')


class PickedBottlesSerializer(serializers.ModelSerializer):
    bottle = BottleDetailSerializer()

    class Meta:
        model = BottlePickerRelation
        fields = ('id', 'bottle', 'create_at')
