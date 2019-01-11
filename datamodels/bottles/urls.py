#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 下午10:13
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : urls.py
from django.urls import path

from datamodels.bottles import views

urlpatterns = [
    path('', views.MyBottleView.as_view(), name='create-list-bottles'),
    path('<int:pk>/', views.BottleDeleteView.as_view(), name='delete-bottles'),
    path('pick/', views.PickOneBottleView.as_view(), name='pick-one-bottle'),
    path('picked/lists/', views.PickedBottlesView.as_view(), name='picked-bottles'),
    path('picked/<int:pk>/', views.DeletePickedBolltleView.as_view(), name='delete-one-picked-bottle'),
]
