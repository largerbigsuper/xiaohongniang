#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : veiwset.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from LV.settings_lv import Platform
from datamodels.role.api.serializers import CustomerBaseInfoSerializer, RecommedCustomerSerializer, \
    InviteRecordSerializer, CustomerRegisterSerializer
from datamodels.role.models import mm_Customer, mm_InviteRecord
from datamodels.sms.models import mm_SMSCode
from lib import customer_login
from lib.common import HeadersKey
from lib.tools import gen_invite_code, decode_invite_code


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = mm_Customer.all()
    serializer_class = CustomerBaseInfoSerializer

    @action(detail=False)
    def service_top(self, request):
        """置顶人员"""
        self.queryset = mm_Customer.show_in_home_page()
        return super().list(request)

    @action(detail=False, serializer_class=RecommedCustomerSerializer)
    def recommend(self, request):
        """新人推荐"""
        self.queryset = mm_Customer.recommend_customers(request.user.customer)
        return super().list(request)

    @csrf_exempt
    @action(methods=['post'], detail=False, serializer_class=CustomerRegisterSerializer, permission_classes=[])
    def enroll(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.validated_data['account']
        password = serializer.validated_data['password']
        code = serializer.validated_data['code']
        mm_SMSCode.is_effective(account, code)
        customer = mm_Customer.add(account, password)
        customer_login.login(request, customer.user)
        invitecode = request.query_params.get('invitecode')
        platform = request.META.get(HeadersKey.HTTP_OS, Platform.WEB)
        # TODO 添加邀请关系
        if invitecode:
            inviter_id = decode_invite_code(invitecode)
            mm_InviteRecord.add_record(inviter_id=inviter_id,
                                       invited_id=customer.id,
                                       platform=platform)
        data = dict(account=account, id=customer.id, user_id=customer.user.id)
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False)
    def invitecode(self, request):
        if not request.user.customer.invitecode:
            request.user.customer.invitecode = gen_invite_code(request.user.customer.id)
            request.user.customer.save()
        data = {
            'invitecode': request.user.customer.invitecode
        }
        return Response(data=data)


class InviteRecordViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = InviteRecordSerializer

    def get_queryset(self):
        return mm_InviteRecord.get_customer_records(self.request.session['customer_id'])

