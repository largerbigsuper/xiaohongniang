#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 下午5:47
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.feedback.models import FeedBack, Report
from datamodels.role.api.serializers import AdminCustomerListSerilizer
from lib.fields import JsonField


class AdminFeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedBack
        fields = ('id', 'customer', 'content', 'create_at', 'deal_status')


class AdminReportSerializer(serializers.ModelSerializer):
    customer = AdminCustomerListSerilizer
    to_customer = AdminCustomerListSerilizer
    images = JsonField()

    class Meta:
        model = Report
        fields = ('id', 'customer', 'to_customer', 'report_type', 'detail', 'images',
                  'deal_status', 'create_at')
