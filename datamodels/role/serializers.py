#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 下午12:28
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from datamodels.role.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user_id', 'name', 'age', 'gender', 'avatar', 'login_tel', 'wechat_id')
        read_only_fields = ('login_tel',)

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            customer = Customer.objects.create(user=user, login_tel=validated_data['username'])
            return customer
