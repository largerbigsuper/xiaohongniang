#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 下午9:41
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.feedback.models import FeedBack


class FeedBackSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = FeedBack
        fields = ('id', 'customer_id', 'content', 'create_at', 'deal_status')
