#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 下午11:50
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.notices.models import Demand, WechatCard
from datamodels.role.api.serializers import CustomerBaseInfoSerializer
from datamodels.role.models import mm_Customer


class DemandCreateSerializer(serializers.ModelSerializer):
    to_customer_id = serializers.PrimaryKeyRelatedField(source='to_customer', queryset=mm_Customer.all(),)

    class Meta:
        model = Demand
        fields = ('id', 'to_customer_id')


class MyDemandListSerializer(serializers.ModelSerializer):
    to_customer = CustomerBaseInfoSerializer(read_only=True)

    class Meta:
        model = Demand
        fields = ('id', 'to_customer', 'status', 'create_at')


class DemandToMeListSrializer(serializers.ModelSerializer):
    customer = CustomerBaseInfoSerializer(read_only=True)

    class Meta:
        model = Demand
        fields = ('id', 'customer', 'status', 'create_at')


class ReplyDemandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Demand
        fields = ('status',)


class MyWechatCardSerializer(serializers.ModelSerializer):
    accepted_customer = CustomerBaseInfoSerializer(read_only=True)

    class Meta:
        model = WechatCard
        fields = ('id', 'accepted_customer', 'wechat', 'create_at')
