#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 上午9:39
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serialziers.py
from abc import ABC
from datetime import datetime

from rest_framework import serializers

from datamodels.products.models import mm_VirtualService, VirtualService, ServiceCertification
from datamodels.role.api.serializers import AdminCustomerListSerilizer
from lib.fields import JsonField


class BaseVirtualServiceSerializer(serializers.ModelSerializer):
    pricelist = JsonField()


class AdminVirtualServiceSerializer(BaseVirtualServiceSerializer):

    def validate_pricelist(self, value):
        mm_VirtualService.check_pricelist_format(value)
        return value

    class Meta:
        model = VirtualService
        fields = '__all__'


class VirtualServiceSerializer(BaseVirtualServiceSerializer):

    class Meta:
        model = VirtualService
        fields = '__all__'


class CustomerBuyServiceSerializer(serializers.Serializer):
    pay_type = serializers.IntegerField(initial=1, default=1, label='pay_type', help_text='支付平台: 支付宝==1',)
    pay_from = serializers.CharField(initial='APP', default='APP', label='pay_from', help_text='支付方式: APP==APP支付')
    price_index = serializers.IntegerField(initial=0, default=0, label='price_index',
                                           help_text='价格套餐: 价格套餐对应index, 默认：0')


class ServiceCertificationSerializer(serializers.ModelSerializer):

    virtual_service = VirtualServiceSerializer()
    expired = serializers.SerializerMethodField()

    def get_expired(self, obj):
        return obj.expired_at < datetime.now()

    class Meta:
        model = ServiceCertification
        fields = ('id', 'virtual_service', 'expired_at', 'create_at', 'expired')


class AdminServiceCertificationSerializer(ServiceCertificationSerializer):
    customer = AdminCustomerListSerilizer()

    class Meta:
        model = ServiceCertification
        fields = ('id', 'virtual_service', 'expired_at', 'create_at', 'expired', 'customer')
