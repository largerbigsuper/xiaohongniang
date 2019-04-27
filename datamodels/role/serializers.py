#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午12:28
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from datetime import datetime

from django.core.cache import cache
from rest_framework import serializers

from datamodels.role.models import Customer, RelationShip, mm_RelationShip, Certification
from lib.fields import JsonField


class CustomerSerializer(serializers.ModelSerializer):
    condition = JsonField(required=False)
    images = JsonField(required=False)

    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account',
                  'wechat_id', 'intro', 'address_home', 'address_company', 'im_token',
                  'following_count', 'followers_count', 'blocked_count', 'following_both_count',
                  'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
                  'expect_desc',
                  'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
                  'child_status', 'years_to_marry', 'score', 'condition', 'images',
                  'service_vip_expired_at', 'service_show_index_expired_at', 'invitecode',
                  'online_card_count', 'offline_card_count', 'is_idcard_verified'
                  )
        read_only_fields = ('account', 'user', 'id', 'im_token',
                            'service_vip_expired_at', 'service_show_index_expired_at')


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
                  'service_vip_expired_at', 'is_idcard_verified'
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
                  'service_vip_expired_at', 'is_idcard_verified'
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
                  'service_vip_expired_at', 'is_idcard_verified'
                  )


class CoustomerBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'wechat_id', 'intro', 'address_home',
            'address_company', 'im_token', 'following_count', 'followers_count', 'blocked_count',
            'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut',
            'service_vip_expired_at', 'is_idcard_verified'
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
            'is_myself', 'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
            'service_vip_expired_at', 'is_idcard_verified'
        )


class NormalCoustomerDetailSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()
    is_myself = serializers.SerializerMethodField()
    condition = JsonField(required=False)
    images = JsonField(required=False)

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
            'is_myself', 'is_manager', 'is_shop_keeper', 'skills', 'is_show_skill', 'is_rut',
            'expect_desc',
            'birthday', 'height', 'profession', 'education', 'income', 'marital_status',
            'child_status', 'years_to_marry', 'score', 'condition', 'images',
            'service_vip_expired_at', 'is_idcard_verified'
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
            'last_request_at',
            'service_vip_expired_at', 'is_idcard_verified'
        )


class CustomerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'im_token',
                  'is_manager', 'is_shop_keeper', 'is_show_skill', 'is_rut',
                  'service_vip_expired_at', 'is_idcard_verified'
                  )


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


class CertificationSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    images = JsonField(required=False)

    class Meta:
        model = Certification
        fields = ('id', 'customer_id', 'property_type', 'images', 'status', 'modify_at', 'create_at')
        read_only_fields = ('status', 'modify_at')


class AdminCertificationSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer()
    images = JsonField(required=False)

    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('id', 'customer', 'property_type', 'images', 'create_at')
        modify_fields = ('status', 'modify_at')
