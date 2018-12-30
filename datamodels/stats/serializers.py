#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 下午9:24
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.role.serializers import CustomerSimpleSerializer
from datamodels.stats.models import OperationRecord


class OpreationRecordListSerilizer(serializers.ModelSerializer):
    customer = CustomerSimpleSerializer(source='from_customer')

    class Meta:
        model = OperationRecord
        fields = ('customer', 'create_at')
