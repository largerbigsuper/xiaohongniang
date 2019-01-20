#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 下午9:51
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.feedback import views

urlpatterns = [
    path('', views.AddFeedBackView.as_view(), name='add-feedback'),
    path('reports/', views.AddReportView.as_view(), name='add-report'),
]
