#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 下午11:50
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from datamodels.notices.api.serializers import MyDemandListSerializer, DemandCreateSerializer, DemandToMeListSrializer, \
    ReplyDemandSerializer, MyWechatCardSerializer
from datamodels.notices.models import mm_Demand, mm_WechatCard


class DemandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = MyDemandListSerializer

    def get_queryset(self):
        return mm_Demand.received(self.request.session['customer_id'])

    @action(methods=['post'], serializer_class=DemandCreateSerializer, detail=False)
    def ask_wechat(self, request):
        """申请微信"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user.customer)
        return Response()

    @action(methods=['post'], serializer_class=DemandCreateSerializer, detail=False)
    def ask_date(self, request):
        """帮我约"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user.customer, demand_type=mm_Demand.Type_Make_Date)
        return Response()

    @action(detail=False)
    def mine(self, request, *args, **kwargs):
        demand_type = int(request.query_params.get('demand_type', mm_Demand.Type_Ask_Wechat))
        self.queryset = mm_Demand.filter(customer_id=request.session['customer_id'], demand_type=demand_type)
        return super().list(request, *args, **kwargs)

    @action(serializer_class=DemandToMeListSrializer, detail=False)
    def received(self, request, *args, **kwargs):
        demand_type = int(request.query_params.get('demand_type', mm_Demand.Type_Ask_Wechat))
        self.queryset = mm_Demand.received(request.session['customer_id'], demand_type=demand_type)
        return super().list(request, *args, **kwargs)

    @action(methods=['put'],serializer_class=ReplyDemandSerializer, detail=True)
    def reply(self, requset, pk=None):
        customer_id = requset.session['customer_id']
        self.queryset = mm_Demand.received(customer_id)
        obj = self.get_object()
        serializer = self.serializer_class(obj, data=requset.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if obj.demand_type == mm_Demand.Type_Ask_Wechat:
            if serializer.validated_data['status'] == mm_Demand.Status_Accepted:
                mm_WechatCard.add_wechat(obj.customer_id, customer_id, obj.customer.wechat_id)
            elif serializer.validated_data['status'] == mm_Demand.Status_Refused:
                pass
            else:
                pass
        else:
            pass

        return Response()

    @action(detail=False, serializer_class=None)
    def unread(self, request):
        demand_type = int(request.query_params.get('demand_type', mm_Demand.Type_Ask_Wechat))
        count = mm_Demand.received(customer_id=request.session['customer_id'],
                                   demand_type=demand_type,
                                   status=mm_Demand.Status_Need_Reply).count()
        data = {
            'count': count
        }
        return Response(data=data)


class MyWechatCardViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = MyWechatCardSerializer

    def get_queryset(self):
        return mm_WechatCard.mycards(self.request.session['customer_id'])
