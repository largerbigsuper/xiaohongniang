#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 下午10:00
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : views.py
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from LV import handan_global_config
from LV.settings import QiNiuSettings
from datamodels.role.models import mm_Customer
from lib.common import CacheKey
from lib.im import IMServe
from lib.qiniucloud import QiniuServe
from lib.tools import Tool


class UploadTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        Tool.param_in_options(request, 'file_type', ['image'])
        file_type = request.query_params.get('file_type', 'image')
        bucket_name = QiniuServe.get_bucket_name(file_type)
        token = QiniuServe.gen_app_upload_token(bucket_name)
        data = {'token': token}
        return Response(Tool.format_data(data))


class ImTokenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = IMServe.gen_token(request.user.customer.id, request.user.customer.name, request.user.customer.avatar_url)
        request.user.customer.im_token = data['token']
        request.user.customer.save()
        return Response(Tool.format_data(data))


class APPConfigView(APIView):

    def get(self, request):
        
        BASE_USER_COUNT = 1000
        user_total = cache.get(CacheKey.user_total)
        if user_total is None:
            user_total = mm_Customer.all().count()
            cache.set(CacheKey.user_total, user_total, 60 * 5)
        user_total += BASE_USER_COUNT
        app_config = {
            'version': '1.0.3',
            'url': 'http://pkqiei3s2.bkt.clouddn.com/app-release-xueqiu',
            'desc': '修复图片显示问题，更换雪球logo',
            'music': 'http://oys4026ng.bkt.clouddn.com/musiclight.mp3',
            'user_total': user_total,
            'image_domain': QiNiuSettings.BUCKET_DOMAIN_DICT['image'],
            'chat_times_limit': settings.NORNAML_CUSTOMER_CHAT_TIMES_LIMIT_PER_DAY,
            'kefuid': mm_Customer.get_kefu_id(),
            'isNeedVerified': handan_global_config.IsNeedVerified,
            'next_app_version': handan_global_config.Next_APP_Version,
            'version_ios': handan_global_config.CURRENT_APP_VERSION_IOS,
            'version_android': handan_global_config.CURRENT_APP_VERSION_ANDROID,


        }
        return Response(Tool.format_data(app_config))


def protocol(request):
    return render(request, 'protocol.html')


def register(request):
    return render(request, 'register/register.html')


def about_us(request):
    return render(request, 'about_us.html')
