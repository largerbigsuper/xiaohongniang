#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : veiwset.py
import requests
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import FilterSet, OrderingFilter, CharFilter, NumberFilter
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from LV import settings
from LV.settings_lv import Platform
from datamodels.role.api.serializers import CustomerBaseInfoSerializer, RecommedCustomerSerializer, \
    InviteRecordSerializer, CustomerRegisterSerializer, MiniprogramLoginSerializer, IndexTopCustomerSerializer, \
    CustomerListSerializer, IDCardCertificationSerializer
from datamodels.role.models import mm_Customer, mm_InviteRecord, mm_IDCardCertification
from datamodels.sms.models import mm_SMSCode
from datamodels.stats.models import mm_CustomerPoint, mm_CustomerBonusRecord
from lib import customer_login
from lib.common import HeadersKey
from lib.tools import gen_invite_code, decode_invite_code


class CustomerFilter(FilterSet):

    o = OrderingFilter(
        fields={
            'id': 'id',
            'last_request_at': 'last_request_at'
        },
    )

    class Meta:
        model = mm_Customer.model
        fields = {
            'gender': ['exact'],
            'age': ['exact', 'gte', 'lte'],
            'profession': ['exact'],
            'height': ['gte', 'lte'],
            'income': ['exact'],
            'education': ['exact'],
            'marital_status': ['exact'],
            'child_status': ['exact'],
            'years_to_marry': ['exact'],
        }


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerListSerializer
    filterset_class = CustomerFilter

    def get_queryset(self):
        return mm_Customer.exclude(gender=self.request.user.customer.gender)

    def filter_queryset(self, queryset):
        if 'q' in self.request.query_params:
            q = self.request.query_params['q']
            return queryset.exclude(Q(name='') | Q(account='')).filter(Q(name__icontains=q) | Q(account__icontains=q))
        return queryset

    def list(self, request, *args, **kwargs):
        if 'q' in kwargs:
            self.queryset = super().get_queryset().filter(Q(name__icontains=kwargs['q']) | Q(account__icontains=kwargs['q']))
        return super().list(request, *args, **kwargs)

    @action(detail=False, serializer_class=IndexTopCustomerSerializer)
    def service_top(self, request):
        """置顶人员"""
        queryset = mm_Customer.show_in_home_page()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        if invitecode:
            inviter_id = decode_invite_code(invitecode)
            mm_InviteRecord.add_record(inviter_id=inviter_id,
                                       invited_id=customer.id,
                                       platform=platform)
            # 添加邀请返现
            mm_CustomerBonusRecord.add_record(
                customer_id=inviter_id,
                from_customer_id=customer.id,
                action=mm_CustomerBonusRecord.Action_Enroll,
                amount=mm_CustomerBonusRecord.Award_Mapping[mm_CustomerBonusRecord.Action_Enroll],
                desc=mm_CustomerBonusRecord.template_enroll.format(customer.account)
            )

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

    @csrf_exempt
    @action(methods=['post'], detail=False, serializer_class=MiniprogramLoginSerializer, permission_classes=[])
    def login_miniprogram(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        wx_res = requests.get(settings.MinprogramSettings.LOGIN_URL + code)
        ret_json = wx_res.json()
        if 'openid' not in ret_json:
            return Response(data=ret_json, status=status.HTTP_400_BAD_REQUEST)
        openid = ret_json['openid']
        # session_key = ret_json['session_key']
        # unionid = ret_json.get('session_key')
        customer = mm_Customer.get_customer_by_miniprogram(openid)
        customer_login.login(request, customer.user)
        data = {
            'id': customer.id,
            'user_id': customer.user.id,
            'name': customer.name,
            'im_token': customer.im_token,
        }
        mm_CustomerPoint.add_action(request.session['customer_id'], mm_CustomerPoint.Action_Login)
        return Response(data=data)


class InviteRecordViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = InviteRecordSerializer

    def get_queryset(self):
        return mm_InviteRecord.get_customer_records(self.request.session['customer_id'])


class IDCardCertificationViewSet(mixins.CreateModelMixin, GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = IDCardCertificationSerializer

    queryset = mm_IDCardCertification.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = mm_IDCardCertification.update_or_create(customer_id=request.session['customer_id'],
                                                         defaults={
                                                             'realname': serializer.validated_data['realname'],
                                                             'idnumber': serializer.validated_data['idnumber']
                                                         }
                                                         )
        request.user.customer.is_idcard_verified = True
        request.user.customer.save()
        return Response(data=serializer.data)
