#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午12:28
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from datamodels.role.models import Customer, RelationShip, mm_RelationShip

CUSTOMER_FIELDS = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                   'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                   'following_count', 'followers_count', 'blocked_count')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                  'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                  'following_count', 'followers_count', 'blocked_count')
        read_only_fields = ('account', 'user', 'id', 'im_token')


class CustomerListSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()

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
                  'account', 'wechat_id', 'intro', 'im_token',
                  'address_company', 'address_home', 'relation_status',
                  'following_count', 'followers_count', 'blocked_count', 'is_myself')


class CoustomerBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count')


class NormalCoustomerSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()

    def get_relation_status(self, obj):
        customer_id = self.context['request'].session['customer_id']
        if not hasattr(self, '_relation_map'):
            self._relation_map = mm_RelationShip.get_following_customer_ids_map(customer_id)
        return self._relation_map.get(obj.id, -1)

    def get_is_myself(self, obj):
        return obj.id == self.context['request'].session['customer_id']

    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count', 'relation_status',
            'is_myself')


class CustomerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'im_token',)


class BaseRelationShipSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer(source='to_customer')

    class Meta:
        model = RelationShip
        fields = ('id', 'customer', 'status')


class FollowingRelationShipSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer(source='to_customer')

    class Meta:
        model = RelationShip
        fields = ('id', 'customer', 'create_at', 'status')


class FollowersRelationShipSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer(source='from_customer')

    class Meta:
        model = RelationShip
        fields = ('id', 'customer', 'create_at', 'status')
