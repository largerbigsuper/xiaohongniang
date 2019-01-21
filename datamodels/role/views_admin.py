#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 下午10:30
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : views_admin.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from datamodels.role.models import mm_Certification
from datamodels.role.serializers import AdminCertificationSerializer
from lib.tools import Tool


class AdminCertificationListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminCertificationSerializer

    def get_queryset(self):
        f = {}
        if 'property_type' in self.request.query_params:
            f['property_type'] = self.request.query_params['property_type']
        if 'status' in self.request.query_params:
            f['status'] = self.request.query_params['status']
        return mm_Certification.filter(**f)


class ModifyCertificationView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminCertificationSerializer

    def get_queryset(self):
        return mm_Certification.all()

    def update(self, request, *args, **kwargs):
        certification = self.get_object()
        serializers = self.serializer_class(certification, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
