#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 下午11:50
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from datamodels.notices.api.serializers import MyDemandListSerializer, DemandToMeListSrializer, \
    ReplyDemandSerializer, MyWechatCardSerializer, DemandSerializer
from datamodels.notices.models import mm_Demand, mm_WechatCard
from datamodels.products.models import mm_VirtualService


class DemandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = MyDemandListSerializer
    queryset = mm_Demand.all()

    # def get_queryset(self):
    #     return mm_Demand.filter(customer_id=self.request.session['customer_id'])

    @action(methods=['post'], serializer_class=DemandSerializer, detail=False)
    def add_ask(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        demand_type = serializer.validated_data['demand_type']
        if demand_type == 0:  # 申请微信
            serializer.save(customer=request.user.customer, demand_type=mm_Demand.Type_Ask_Wechat)
            return Response()
        elif demand_type == 1:

            if request.user.customer.online_card_count < 1:
                data = {
                    'detail': '无可用线上服务卡'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        elif demand_type == 2:
            if request.user.customer.offline_card_count < 1:
                data = {
                    'detail': '无可用线下服务卡'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            service_type = mm_VirtualService.Demand_Type_2_Service_Type.get(demand_type, 0)
            mm_VirtualService.modify_card(request.session['customer_id'], service_type, -1)
            serializer.save(customer=request.user.customer, demand_type=demand_type)
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

    @action(methods=['put'], serializer_class=ReplyDemandSerializer, detail=True)
    def reply(self, requset, pk=None):
        customer_id = requset.session['customer_id']
        self.queryset = mm_Demand.received(customer_id)
        obj = self.get_object()
        if obj.status == mm_Demand.Status_Refused:
            return Response()
        serializer = self.serializer_class(obj, data=requset.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if obj.demand_type == mm_Demand.Type_Ask_Wechat:
            if serializer.validated_data['status'] == mm_Demand.Status_Accepted:
                # 更新申请人微信名片
                mm_WechatCard.add_wechat(obj.customer_id, requset.user.customer.id, requset.user.customer.wechat_id)
                # 更新被申请人的名片列表
                mm_WechatCard.add_wechat(requset.user.customer.id, obj.customer_id, obj.customer.wechat_id)
            elif serializer.validated_data['status'] == mm_Demand.Status_Refused:
                pass
            else:
                pass
        else:
            if serializer.validated_data['status'] == mm_Demand.Status_Refused:  # 返回线上或线下服务卡
                service_type = mm_VirtualService.Demand_Type_2_Service_Type.get(obj.demand_type, 0)
                mm_VirtualService.modify_card(obj.customer_id, service_type, 1)

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
