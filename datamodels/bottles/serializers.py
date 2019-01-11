#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 下午10:00
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.bottles.models import Bottle
from datamodels.role.serializers import NormalCoustomerSerializer


class CreateBottleSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at', 'customer_id')


class NormalBottleSerializer(serializers.ModelSerializer):
    customer = NormalCoustomerSerializer()

    class Meta:
        model = Bottle
        fields = ('id', 'customer', 'text', 'create_at')
