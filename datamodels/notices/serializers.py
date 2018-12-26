#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 下午12:28
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.role.serializers import CustomerSimpleSerializer
from datamodels.notices.models import Notice, ACTION_TYPE_TO_RESULT


class NoticeSerializer(serializers.ModelSerializer):
    from_customer = CustomerSimpleSerializer()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        name = obj.from_customer.name
        action = obj.get_action_type_display()
        object_type = ACTION_TYPE_TO_RESULT[obj.action_type]
        return '{name}{action}了你的{object_type}'.format(name=name, action=action, object_type=object_type)

    class Meta:
        model = Notice
        fields = ('id', 'action_type', 'object_id', 'result_id', 'from_customer', 'create_at', 'text')
