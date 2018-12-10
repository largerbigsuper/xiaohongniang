#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 下午10:00
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from lib.im import IMServe
from lib.qiniucloud import QiniuServe
from lib.tools import Tool


class UploadTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        Tool.required_params(request, ['file_name'])
        Tool.param_in_options(request, 'file_type', ['image'])
        file_type = request.query_params.get('file_type', 'image')
        file_name = request.query_params.get('file_name')
        bucket_name = QiniuServe.get_bucket_name(file_type)
        token = QiniuServe.gen_app_upload_token(bucket_name, file_name, request.user.id)
        data = {'token': token}
        return Response(Tool.format_data(data))


class ImTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = IMServe.gen_token(request.user.id, request.user.customer.name, request.user.customer.avatar_url)
        request.user.customer.im_token = data['token']
        request.user.customer.save()
        return Response(Tool.format_data(data))



