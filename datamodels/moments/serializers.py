#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 下午5:35
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
import json

from rest_framework import serializers

from datamodels.moments.models import Moments, Comments, Likes, Topic
from datamodels.role.serializers import CoustomerBaseInfoSerializer, CustomerSimpleSerializer, NormalCoustomerSerializer
from lib.fields import JsonField


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name', 'logo_url', 'create_at')


class BaseMomentSerializer(serializers.ModelSerializer):
    images = JsonField(required=False)
    topic = TopicSerializer(many=True, read_only=True)


class MomentsSerializer(BaseMomentSerializer):

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at',
                  'comment_total', 'like_total', 'is_hidden_name', 'address', 'function_type', 'topic')


class MomentsCreateSerializer(BaseMomentSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = Moments
        fields = ('id', 'customer_id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at',
                  'comment_total', 'like_total', 'is_hidden_name', 'address', 'function_type', 'topic')


class MomentsDetailSerializer(BaseMomentSerializer):
    customer = CoustomerBaseInfoSerializer()

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at', 'customer',
                  'comment_total', 'like_total', 'is_hidden_name', 'address', 'function_type', 'topic')


class NormalMomentsDetailSerializer(BaseMomentSerializer):
    customer = NormalCoustomerSerializer()

    class Meta:
        model = Moments
        fields = ('id', 'text', 'images', 'latitude', 'longitude',
                  'create_at', 'update_at', 'customer',
                  'comment_total', 'like_total', 'is_hidden_name', 'address', 'function_type', 'topic')


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
