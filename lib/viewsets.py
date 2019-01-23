#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 下午3:44
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet


class AdminViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
