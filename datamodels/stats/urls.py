#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 下午9:24
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.stats import views


urlpatterns = [
    path('visitors/', views.OpreationRecordListView.as_view(), name='my-visitors'),
    path('records/unread/', views.UnreadTotalOpreationRecordView.as_view(), name='my-visitors-unread'),
]
