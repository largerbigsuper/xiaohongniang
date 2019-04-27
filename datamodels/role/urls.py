#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午7:01
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : url.py
from django.urls import path

from datamodels.role import views

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('enroll/', views.RegisterView.as_view()),
    path('password/', views.PasswordResetView.as_view()),
    path('profile/', views.CustomerProfile.as_view()),
    path('<int:pk>/', views.CustomerDetail.as_view()),
    path('following/', views.MyFollowerView.as_view()),
    path('followinglist/', views.MyFollowingList.as_view()),
    path('followerslist/', views.MyFollowersList.as_view()),
    path('bothfolowinglist/', views.BothFollowingList.as_view()),
    path('lists/', views.CustomerList.as_view()),
    path('active/lists/', views.ActiveCustomerList.as_view()),
    path('has_skills/lists/', views.CustomerWithSkillsList.as_view()),
    path('single/lists/', views.CustomerSingleList.as_view()),
    path('unknown/lists/', views.UnfollowingList.as_view()),
    path('search/', views.CustomerSearchView.as_view()),
    path('around/', views.AroundCustomerView.as_view()),
    path('certifications/', views.CustomerCertificationView.as_view()),
    path('certifications/<int:pk>/', views.ModifyCertificationView.as_view()),
]
