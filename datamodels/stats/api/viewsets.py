#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 上午10:27
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from datamodels.stats.api.serializers import PointSerializer, AdminPointSerializer
from datamodels.stats.models import mm_CustomerPoint


class PointViewSet(mixins.ListModelMixin,
                   GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = PointSerializer

    def get_queryset(self):
        return mm_CustomerPoint.filter(customer_id=self.request.session['customer_id'])


class AdminPointViewSet(mixins.ListModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminPointSerializer
    queryset = mm_CustomerPoint.all()
