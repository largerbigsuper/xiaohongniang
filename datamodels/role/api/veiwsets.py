#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:25
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : veiwset.py
from rest_framework import viewsets

from datamodels.role.api.serializers import CustomerSerializer
from datamodels.role.models import mm_Customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = mm_Customer.all()
    serializer_class = CustomerSerializer
