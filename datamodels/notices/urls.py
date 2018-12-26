#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/26 下午12:58
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.notices import views


urlpatterns = [
    path('unread/', views.NoticeListView.as_view(), name='unread-notices'),
    path('<int:pk>/', views.SetNoticeStatusView.as_view(), name='set-read-notices'),
]
