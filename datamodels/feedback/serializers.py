#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 下午9:41
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.feedback.models import FeedBack, Report
from datamodels.role.serializers import CustomerSimpleSerializer
from lib.fields import JsonField


class FeedBackSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = FeedBack
        fields = ('id', 'customer_id', 'content', 'create_at', 'deal_status')


class BaseReportSerializer(serializers.ModelSerializer):
    images = JsonField(required=False)


class ReportSerializer(BaseReportSerializer):
    customer_id = serializers.IntegerField()
    to_customer_id = serializers.IntegerField()

    class Meta:
        model = Report
        fields = ('id', 'customer_id', 'to_customer_id', 'report_type', 'detail', 'images', 'deal_status', 'create_at')


class ReportListSerializer(BaseReportSerializer):
    to_customer = CustomerSimpleSerializer()

    class Meta:
        model = Report
        fields = ('id', 'to_customer', 'report_type', 'detail', 'images', 'deal_status', 'create_at')
