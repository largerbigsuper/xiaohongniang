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
    path('latest/lists/', views.LatestMomentsListView.as_view(), name='latest-list-moments'),
    path('<int:pk>/', views.MomentModifyView.as_view(), name='get-update-delete-my-moments'),
    path('detail/<int:pk>/', views.MomentsDetailView.as_view(), name='detail-moments'),
    path('customer/<int:pk>/lists/', views.CustomerMomentsListView.as_view(), name='list-momemts'),
    path('following/lists/', views.FollowingMomentsListView.as_view(), name='following-list-momemts'),
    path('search/', views.MomentSearchView.as_view(), name='search-momemts'),
    path('<int:pk>/comment/', views.CommentView.as_view(), name='add-lists-comment'),
    path('comment/<int:pk>/', views.ReplyOrDeleteCommentView.as_view(), name='reply-comment'),
    path('<int:pk>/likes/', views.LikesView.as_view(), name='add-lists-destory-likes'),
    path('topic/', views.TopicListView.as_view(), name='create-lists-topic'),
    path('topic/<int:pk>/', views.TopicView.as_view(), name='get-update-delete-topic'),
    path('topic/<int:pk>/', views.TopicView.as_view(), name='get-update-delete-topic'),
    path('topic/<int:pk>/chatgroup/', views.TopicChatGroupView.as_view(), name='topic-chat-group'),
]
