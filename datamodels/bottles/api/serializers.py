#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午7:17
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.bottles.models import Bottle
from datamodels.role.api.serializers import CustomerBaseInfoSerializer, AdminCustomerListSerilizer


class BottleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at')


class PickedBottleSerialzier(serializers.ModelSerializer):
    customer = CustomerBaseInfoSerializer()

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at', 'customer', 'pick_at')


class BottleDetailSerializer(serializers.ModelSerializer):
    customer = CustomerBaseInfoSerializer()

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at', 'customer')


class AdminBottleSerializer(serializers.ModelSerializer):
    customer = AdminCustomerListSerilizer()
    picker = AdminCustomerListSerilizer()

    class Meta:
        model = Bottle
        fields = ('id', 'text', 'create_at', 'customer', 'picker', 'pick_at')
