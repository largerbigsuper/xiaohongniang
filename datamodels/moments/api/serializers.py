#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 下午5:23
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.moments.models import Moments, Topic
from datamodels.role.api.serializers import AdminCustomerListSerilizer
from lib.fields import JsonField

Admin_Moments_Fields = ['id', 'text', 'images', 'customer',
                        'comment_total', 'like_total', 'create_at',
                        'is_hidden_name', 'function_type', 'topic']


class AdminTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name', 'logo_url', 'create_at', 'order_num', 'desc')


class AdminMomentsSerializer(serializers.ModelSerializer):
    customer = AdminCustomerListSerilizer()
    topic = AdminTopicSerializer(many=True)
    images = JsonField()

    class Meta:
        model = Moments
        fields = tuple(Admin_Moments_Fields)
