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


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        # fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar', 'account', 'wechat_id')
        read_only_fields = ('account', 'user', 'id', 'im_token')

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            customer = Customer.objects.create(user=user, login_tel=validated_data['username'])
            return customer


class CustomerListSerializer(serializers.ModelSerializer):
    relation_status = serializers.SerializerMethodField()

    def get_relation_status(self, obj):
        customer_id = self.context['request'].session['customer_id']
        if not hasattr(self, '_relation_map'):
            self._relation_map = mm_RelationShip.get_following_customer_ids_map(customer_id)
        return self._relation_map.get(obj.id, -1)

    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar_url', 'account', 'wechat_id', 'relation_status')


class CoustomerBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name')


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
