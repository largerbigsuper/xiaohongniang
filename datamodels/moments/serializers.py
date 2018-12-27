#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 下午5:35
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
import json

from rest_framework import serializers

from datamodels.moments.models import Moments, Comments, Likes
from datamodels.role.serializers import CoustomerBaseInfoSerializer, CustomerSimpleSerializer, NormalCoustomerSerializer


class MomentsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(source='images')

    def get_images(self, obj):
        return json.loads(obj.images)

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at',
                  'comment_total', 'like_total', 'is_hidden_name', 'address')


class MomentsDetailSerializer(serializers.ModelSerializer):
    customer = CoustomerBaseInfoSerializer()
    images = serializers.SerializerMethodField(source='images')

    def get_images(self, obj):
        return json.loads(obj.images)

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at', 'customer',
                  'comment_total', 'like_total', 'is_hidden_name', 'address')


class NormalMomentsDetailSerializer(serializers.ModelSerializer):
    customer = NormalCoustomerSerializer()
    images = serializers.SerializerMethodField(source='images')

    def get_images(self, obj):
        return json.loads(obj.images)

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at', 'customer',
                  'comment_total', 'like_total', 'is_hidden_name', 'address')


class CommentSerializer(serializers.ModelSerializer):
    moment_id = serializers.IntegerField(write_only=True)
    from_customer_id = serializers.IntegerField(write_only=True)
    reply_to_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    to_customer_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = Comments
        fields = ('id', 'moment_id', 'from_customer_id', 'reply_to_id', 'text', 'create_at', 'to_customer_id')


class CommentListSerializer(serializers.ModelSerializer):
    from_customer = CustomerSimpleSerializer()
    reply_to_id = serializers.IntegerField()
    to_customer = CustomerSimpleSerializer()

    class Meta:
        model = Comments
        fields = ('id', 'from_customer', 'reply_to_id', 'text', 'create_at', 'to_customer')


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ('id',)


class LikeListSerialzier(serializers.ModelSerializer):
    customer = CustomerSimpleSerializer()

    class Meta:
        model = Likes
        fields = ('id', 'customer', 'create_at')
