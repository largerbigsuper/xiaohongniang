#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 下午5:24
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from datamodels.moments.api.serializers import AdminTopicSerializer, AdminMomentsSerializer
from datamodels.moments.models import mm_Topic, mm_Moments


class AdminTopicViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminTopicSerializer
    queryset = mm_Topic.all()


class AdminMomentsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminMomentsSerializer
    queryset = mm_Moments.all()
