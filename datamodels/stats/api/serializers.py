#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 上午10:27
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.role.api.serializers import AdminCustomerListSerilizer
from datamodels.role.models import Customer
from datamodels.stats.models import CustomerPoint, MessageTemplate, CustomerBonusRecord, WithDrawRecord


class PointSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerPoint
        fields = ('id', 'desc', 'amount', 'total_left', 'in_or_out', 'create_at')


class AdminPointSerializer(serializers.ModelSerializer):
    customer = AdminCustomerListSerilizer()

    class Meta:
        model = CustomerPoint
        fields = ('customer', 'in_or_out', 'amount', 'total_left', 'action', 'desc', 'create_at', )


class MessageTempalteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageTemplate
        fields = ('id', 'text', 'create_at')


class CustomerBonusRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerBonusRecord
        fields = ('id', 'desc', 'amount', 'total_left', 'in_or_out', 'create_at', 'from_customer')


class WithDrawRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = WithDrawRecord
        fields = ('id', 'amount', 'status', 'create_at')
        read_only_fields = ('status', )


class CustomerChatRecordSerailizer(serializers.Serializer):

    user_id = serializers.IntegerField()