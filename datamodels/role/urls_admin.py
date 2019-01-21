#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 下午10:55
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls_admin.py
from django.urls import path

from datamodels.role import views_admin

urlpatterns = [
    path('certifications/', views_admin.AdminCertificationListView.as_view()),
    path('certifications/<int:pk>/', views_admin.ModifyCertificationView.as_view()),
]
