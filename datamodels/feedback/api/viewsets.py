#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 下午5:47
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from datamodels.feedback.api.serializers import AdminFeedBackSerializer, AdminReportSerializer
from datamodels.feedback.models import mm_FeedBack, mm_Report


class AdminFeedBackViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminFeedBackSerializer
    queryset = mm_FeedBack.all()


class AdminReportViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminReportSerializer
    queryset = mm_Report.all()
