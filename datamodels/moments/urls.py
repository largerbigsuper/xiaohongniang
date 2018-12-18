#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 下午6:16
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.moments import views

urlpatterns = [
    path('', views.MomentsListView.as_view(), name='create-my-moments'),
    path('lists/', views.MomentsListView.as_view(), name='list-my-moments'),
    path('<int:pk>/', views.MomentModifyView.as_view(), name='get-update-delete-my-moments'),
    path('detail/<int:pk>/', views.MomentsDetailView.as_view(), name='detail-moments'),
    path('customer/<int:pk>/lists/', views.CustomerMomentsListView.as_view(), name='list-momemts'),
]
