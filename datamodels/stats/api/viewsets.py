#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/26 上午10:27
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from django.db.models import Sum
from rest_framework import mixins, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from datamodels.role.models import mm_InviteRecord
from datamodels.stats.api.serializers import PointSerializer, AdminPointSerializer, MessageTempalteSerializer, \
    CustomerBonusRecordSerializer, WithDrawRecordSerializer, CustomerChatRecordSerailizer
from datamodels.stats.models import mm_CustomerPoint, CustomerPoint, mm_MessageTemplate, mm_CustomerBonusRecord, \
    mm_WithDrawRecord, mm_CustomerChatRecord


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
    queryset = mm_MessageTemplate.all()

    # def get_queryset(self):
    #     return mm_MessageTemplate.my_templates(self.request.session['customer_id'])

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.session['customer_id'])


class AdminPointViewSet(mixins.ListModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminPointSerializer
    filter_class = PointFilter
    queryset = mm_CustomerPoint.all()


class CustomerBonusRecordViewSet(mixins.ListModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerBonusRecordSerializer

    def get_queryset(self):
        return mm_CustomerBonusRecord.filter(customer_id=self.request.session['customer_id'])


class WithDrawRecordViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = WithDrawRecordSerializer

    def get_queryset(self):
        return mm_WithDrawRecord.filter(customer_id=self.request.session['customer_id'])

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.session['customer_id'])

    def create(self, request, *args, **kwargs):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        amount = serailizer.validated_data['amount']
        if amount > mm_CustomerBonusRecord.get_total_point(request.session['customer_id']):
            data = {
                'detail': '余额不足'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().create(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def detail_info(self, request):
        customer_id = request.session['customer_id']
        invited_count = mm_InviteRecord.filter(inviter_id=request.session['customer_id']).count()
        customer_buy_count = mm_CustomerBonusRecord.get_buy_customer_count(customer_id)
        toatl_available = mm_CustomerBonusRecord.get_total_point(customer_id)
        total_handing = mm_WithDrawRecord.filter(status=mm_WithDrawRecord.Status_Submited).aggregate(Sum('amount'))['amount__sum']
        total_changed = mm_WithDrawRecord.filter(status=mm_WithDrawRecord.Status_Done).aggregate(Sum('amount'))['amount__sum']
        data = {
            'invited_count': invited_count,
            'customer_buy_count': customer_buy_count,
            'toatl_available': toatl_available,
            'total_handing': total_handing if total_handing else 0,
            'total_changed': total_changed if total_changed else 0,
        }
        return Response(data=data)


class CustomerChatRecordViewSet(mixins.ListModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerChatRecordSerailizer

    def get_queryset(self):
        return mm_CustomerChatRecord.filter(customer_id=self.request.session['customer_id'])

    @action(methods=['get'], detail=False)
    def record_list(self, request):
        record_list = mm_CustomerChatRecord.get_record_list(self.request.session['customer_id'])
        data = {
            'record_list': record_list
        }
        return Response(data=data)

    @action(methods=['post'], detail=False)
    def upload_record(self, request):
        serailizer = self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        mm_CustomerChatRecord.add_record(request.session['customer_id'],  serailizer.validated_data['user_id'])
        return Response()
