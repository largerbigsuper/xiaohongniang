#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 下午1:17
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.products import views

urlpatterns = [
    path('alipay/notify/', views.AliPayNotifyView.as_view()),
]
