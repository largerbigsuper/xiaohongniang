#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 上午10:27
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from datamodels.stats.api.serializers import PointSerializer, AdminPointSerializer, MessageTempalteSerializer
from datamodels.stats.models import mm_CustomerPoint, CustomerPoint, mm_MessageTemplate


class PointFilter(filters.FilterSet):

    class Meta:
        model = CustomerPoint
        fields = {
            'customer_id': ['exact'],
            'customer__name': ['icontains'],
            'create_at': ['lte', 'gte'],
            'action': ['exact'],
            'in_or_out': ['exact']
        }


class PointViewSet(mixins.ListModelMixin,
                   GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = PointSerializer

    def get_queryset(self):
        return mm_CustomerPoint.filter(customer_id=self.request.session['customer_id'])


class MessageTemplateViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = MessageTempalteSerializer

    def get_queryset(self):
        return mm_MessageTemplate.my_templates(self.request.session['customer_id'])

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.session['customer_id'])


class AdminPointViewSet(mixins.ListModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminPointSerializer
    filter_class = PointFilter
    queryset = mm_CustomerPoint.all()
