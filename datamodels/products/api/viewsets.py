#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 上午9:39
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
import traceback

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from datamodels.products.api.serialziers import AdminVirtualServiceSerializer, CustomerBuyServiceSerializer, \
    VirtualServiceSerializer, ServiceCertificationSerializer, AdminServiceCertificationSerializer
from datamodels.products.models import mm_VirtualService, mm_AlipayOrder, mm_ServiceCertification


class AdminVirtualServiceViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminVirtualServiceSerializer
    queryset = mm_VirtualService.all()


class CustomerVirtualServiceViewSet(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = VirtualServiceSerializer
    queryset = mm_VirtualService.all()

    @action(methods=['post'], detail=True, serializer_class=CustomerBuyServiceSerializer)
    def buy(self, request, pk=None):
        params_serializer = CustomerBuyServiceSerializer(data=request.data)
        params_serializer.is_valid(raise_exception=True)
        pay_type = params_serializer.validated_data['pay_type']
        pay_from = params_serializer.validated_data['pay_from']
        price_index = params_serializer.validated_data['price_index']
        service_id = pk
        customer_id = request.session['customer_id']
        order_string = None
        try:
            if pay_type == 1:  # 支付宝
                if pay_from == 'APP':
                    order_string = mm_AlipayOrder.create_order(customer_id, service_id, price_index)
            data = {
                'order_string': order_string
            }
            return Response(data)
        except:
            error_msg = traceback.format_exc()
            data = {
                'detail': error_msg
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, serializer_class=ServiceCertificationSerializer)
    def mine(self, request):
        self.queryset = mm_ServiceCertification.get_customer_certifications(request.session['customer_id'])
        return super().list(request)


class AdminServiceCertificationViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminServiceCertificationSerializer
    queryset = mm_ServiceCertification.all()


