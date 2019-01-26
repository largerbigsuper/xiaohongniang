#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : veiwset.py
from django.contrib.auth import authenticate, logout as system_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from datamodels.role.api.serializers import AdminCustomerListSerilizer, CustomerLoginSerilizer, UserSerializer, \
    CustomerWithDrawSerializer
from datamodels.role.models import mm_Customer, Customer
from datamodels.stats.models import mm_CustomerPoint
from lib import customer_login
from lib.exceptions import LoginException
from lib.viewsets import AdminViewSet


class CustomerFilter(filters.FilterSet):

    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'name': ['icontains'],
            'age': ['exact', 'gte', 'lte'],
            'gender': ['exact'],
            'account': ['icontains'],
        }


class AdminCustomerViewSet(AdminViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = mm_Customer.all()
    serializer_class = AdminCustomerListSerilizer
    filter_class = CustomerFilter

    @action(methods=['post'], detail=True, serializer_class=CustomerWithDrawSerializer)
    def withdraw(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = mm_CustomerPoint.withdraw(customer_id=pk,
                                         operator_id=request.user.id,
                                         amount=serializer.validated_data['amount'])
        if data:
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response()


class AdminOpreationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @action(methods=['post'], detail=False, permission_classes=(), serializer_class=CustomerLoginSerilizer)
    def login(self, request):
        login_serializer = CustomerLoginSerilizer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        try:
            username = login_serializer.validated_data['account']
            password = login_serializer.validated_data['password']
            user = authenticate(request=request, username=username, password=password, is_staff=True)
            if user:
                customer_login.login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                raise LoginException('账号或密码错误')
        except Customer.DoesNotExist:
            raise LoginException('账号不存在')

    @csrf_exempt
    @action(detail=False)
    def logout(self, request):
        system_logout(request)
        return Response()


