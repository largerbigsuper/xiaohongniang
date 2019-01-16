#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午12:28
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from datetime import datetime

from django.core.cache import cache
from rest_framework import serializers

from datamodels.role.models import Customer, RelationShip, mm_RelationShip
from lib.fields import JsonField

CUSTOMER_FIELDS = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                   'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                   'following_count', 'followers_count', 'blocked_count')


class CustomerSerializer(serializers.ModelSerializer):
    profession = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()
    marital_status = serializers.SerializerMethodField()
    child_status = serializers.SerializerMethodField()
    condition = JsonField(required=False)

    def get_profession(self, obj):
        return obj.get_profession_display()

    def get_education(self, obj):
        return obj.get_education_display()

    def get_income(self, obj):
        return obj.get_income_display()

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    def get_child_status(self, obj):
        return obj.get_child_status_display()

    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                  'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                  'following_count', 'followers_count', 'blocked_count',
                  'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
                  'expect_desc',
                  'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
                  'child_status', 'years_to_marry', 'score', 'condition'
                  )
        read_only_fields = ('account', 'user', 'id', 'im_token')


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
                  'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut', 'last_request_at'
                  )


class CustomerHasSkillsListSerializer(serializers.ModelSerializer):
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
                  'skills',
                  )


class CustomerSingleListSerializer(serializers.ModelSerializer):
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
                  'expect_desc',
                  )


class CoustomerBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count',
            'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut'
        )


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
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count', 'relation_status',
            'is_myself', 'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut')


class NormalCoustomerDetailSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()
    marital_status = serializers.SerializerMethodField()
    child_status = serializers.SerializerMethodField()
    condition = JsonField(required=False)

    def get_relation_status(self, obj):
        customer_id = self.context['request'].session['customer_id']
        if not hasattr(self, '_relation_map'):
            self._relation_map = mm_RelationShip.get_following_customer_ids_map(customer_id)
        return self._relation_map.get(obj.id, -1)

    def get_is_myself(self, obj):
        return obj.id == self.context['request'].session['customer_id']

    def get_profession(self, obj):
        return obj.get_profession_display()

    def get_education(self, obj):
        return obj.get_education_display()

    def get_income(self, obj):
        return obj.get_income_display()

    def get_marital_status(self, obj):
        return obj.get_marital_status_display()

    def get_child_status(self, obj):
        return obj.get_child_status_display()

    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count', 'relation_status',
            'is_myself', 'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
            'expect_desc',
            'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
            'child_status', 'years_to_marry', 'score', 'condition'
        )


class CoustomerDistanceSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    def get_relation_status(self, obj):
        customer_id = self.context['request'].session['customer_id']
        if not hasattr(self, '_relation_map'):
            self._relation_map = mm_RelationShip.get_following_customer_ids_map(customer_id)
        return self._relation_map.get(obj.id, -1)

    def get_is_myself(self, obj):
        return obj.id == self.context['request'].session['customer_id']

    def get_distance(self, obj):
        return obj.distance

    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count', 'relation_status',
            'is_myself', 'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut', 'distance',
            'last_request_at'
        )


class CustomerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'im_token',
                  'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut')


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
