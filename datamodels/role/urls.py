#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午7:01
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : url.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

from datamodels.role import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', csrf_exempt(views.LogoutView.as_view())),
    path('enroll/', views.RegisterView.as_view()),
    path('password/', views.PasswordResetView.as_view()),
    path('<int:pk>/', views.CustomerDetail.as_view()),
]
