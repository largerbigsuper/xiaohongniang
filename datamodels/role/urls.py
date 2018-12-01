#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午7:01
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : url.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_register),
    path('login', views.customer_login),
    path('logout', views.customer_logout),
]
