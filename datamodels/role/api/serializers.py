#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from datetime import datetime

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import serializers

from datamodels.role.models import Customer, InviteRecord, mm_RelationShip
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

Base_Info_fields = ['id', 'name', 'age', 'gender', 'avatar_url', 'height']
Index_Top_Info_fields = Base_Info_fields + ['address_home']
Recommend_Info_fields = Base_Info_fields + ['height']
Admin_Info_Fields = ['id', 'user_id', 'name', 'gender', 'account']


class CustomerListSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()
    last_request_at = serializers.SerializerMethodField()

    def get_last_request_at(self, obj):
        key = mm_RelationShip.customer_last_request % obj.id
        v = cache.get(key)
        t = datetime.fromtimestamp(v) if v else obj.last_request_at
        if t:
            return t.isoformat()
        else:
            return None

    def get_relation_status(self, obj):
        customer_id = self.context['request'].session['customer_id']
        if not hasattr(self, '_relation_map'):
            self._relation_map = mm_RelationShip.get_following_customer_ids_map(customer_id)
        return self._relation_map.get(obj.id, -1)

    def get_is_myself(self, obj):
        return obj.id == self.context['request'].session['customer_id']

    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url',
                  'wechat_id', 'intro', 'im_token',
                  'address_company', 'address_home', 'relation_status',
                  'following_count', 'followers_count', 'blocked_count', 'is_myself',
                  'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut', 'last_request_at',
                  'service_vip_expired_at', 'height',
                  )


class BaseCustomerSerialzier(serializers.ModelSerializer):
    condition = JsonField(required=False)
    images = JsonField(required=False)


class CustomerProfileSerialier(BaseCustomerSerialzier):

    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'account', 'im_token',
                  'following_count', 'followers_count', 'blocked_count',
                  'is_manager', 'is_shop_keeper',
                  'service_vip_expired_at', 'service_show_index_expired_at', 'invitecode',
                  'name', 'age', 'gender', 'avatar_url',
                  'wechat_id', 'intro', 'address_home', 'address_company',
                  'skills', 'is_show_skill', 'is_rut',
                  'expect_desc',
                  'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
                  'child_status', 'years_to_marry', 'score', 'condition', 'images',
                  )

        read_only_fields = ('id', 'user_id', 'account', 'im_token',
                            'following_count', 'followers_count', 'blocked_count',
                            'is_manager', 'is_shop_keeper',
                            'service_vip_expired_at', 'service_show_index_expired_at', 'invitecode',)
        extra_kwargs = {name: {'required': False} for name in list(set(fields) - set(read_only_fields))}
        extra_kwargs['images']['initial'] = '[]'
        extra_kwargs['condition']['initial'] = '{}'


class CustomerBaseInfoSerializer(BaseCustomerSerialzier):
    class Meta:
        model = Customer
        fields = tuple(Base_Info_fields)


class RecommedCustomerSerializer(BaseCustomerSerialzier):

    class Meta:
        model = Customer
        fields = Recommend_Info_fields


class IndexTopCustomerSerializer(BaseCustomerSerialzier):

    class Meta:
        model = Customer
        fields = Index_Top_Info_fields


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


class CustomerRegisterSerializer(serializers.Serializer):

    account = serializers.CharField(max_length=11, min_length=11)
    password = serializers.CharField()
    code = serializers.CharField(max_length=4)
    # invitecode = serializers.CharField(required=False)


class MiniprogramLoginSerializer(serializers.Serializer):

    code = serializers.CharField()


class InviteRecordSerializer(serializers.ModelSerializer):

    invited = CustomerBaseInfoSerializer()

    class Meta:
        model = InviteRecord
        fields = ['id', 'invited', 'platform', 'create_at']


class AdminInviteRecordSerializer(serializers.ModelSerializer):

    inviter = CustomerBaseInfoSerializer()
    invited = CustomerBaseInfoSerializer()

    class Meta:
        model = InviteRecord
        fields = ['id', 'inviter', 'invited', 'platform', 'create_at']

