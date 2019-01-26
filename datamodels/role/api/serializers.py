#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

from datamodels.role.models import Customer
from lib.fields import JsonField


Customer_Fields = ['id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                   'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                   'following_count', 'followers_count', 'blocked_count',
                   'is_manager', 'is_shop_keeper',
                   'skills', 'is_show_skill',
                   'is_rut', 'expect_desc',
                   'birthday', 'height',
                   'profession', 'education', 'income', 'marital_status', 'child_status', 'years_to_marry', 'score',
                   'condition',
                   'images'
                   ]

Base_Info_fields = ['id', 'name', 'age', 'gender', 'avatar_url']
Recommend_Info_fields = Base_Info_fields + ['height']
Admin_Info_Fields = ['id', 'user_id', 'name', 'gender', 'account']


class BaseCustomerSerialzier(serializers.ModelSerializer):
    condition = JsonField(required=False)
    images = JsonField(required=False)


class CustomerSerializer(BaseCustomerSerialzier):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                  'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                  'following_count', 'followers_count', 'blocked_count',
                  'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
                  'expect_desc',
                  'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
                  'child_status', 'years_to_marry', 'score', 'condition', 'images'
                  )
        read_only_fields = ('account', 'user', 'id', 'im_token')


class CustomerBaseInfoSerializer(BaseCustomerSerialzier):
    class Meta:
        model = Customer
        fields = tuple(Base_Info_fields)


class RecommedCustomerSerializer(BaseCustomerSerialzier):

    class Meta:
        model = Customer
        fields = Recommend_Info_fields


class AdminCustomerListSerilizer(BaseCustomerSerialzier):
    class Meta:
        model = Customer
        fields = tuple(Admin_Info_Fields)


class CustomerLoginSerilizer(serializers.Serializer):
    account = serializers.CharField(min_length=11, help_text='账号')
    password = serializers.CharField(min_length=6, help_text='密码')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', )


class CustomerWithDrawSerializer(serializers.ModelSerializer):

    amount = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ('id', 'amount')
