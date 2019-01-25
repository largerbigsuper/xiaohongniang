#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 下午3:51
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from datamodels.articles.api.serializers import AdminArticleSerializer, ArticleSerializer, AdminTagSerialzier
from datamodels.articles.models import mm_Article, mm_Tag, Article


class ArticleFilter(filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'category': ['exact'],
            'headline': ['icontains'],
            'content': ['icontains'],
            'create_at': ['gte', 'lte', 'exact'],
        }


class AdminArticleFilter(filters.FilterSet):

    class Meta:
        model = Article
        fields = {
            'category': ['exact'],
            'headline': ['icontains'],
            'content': ['icontains'],
            'create_at': ['gte', 'lte', 'exact'],
            'is_published': ['exact'],
        }


class AdminTagViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAuthenticated)
    serializer_class = AdminTagSerialzier
    queryset = mm_Tag.all()

    def create(self, request, *args, **kwargs):
        tag, created = mm_Tag.update_or_create(name=request.data['name'],
                                               defaults={"level": request.data.get('level', 0)}
                                               )
        serializer = self.serializer_class(tag)
        return Response(data=serializer.data)


class AdminArticleViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminArticleSerializer
    queryset = mm_Article.all()
    filter_class = AdminArticleFilter

    def perform_create(self, serializer):
        tag_name = serializer.validated_data['tag']['name']
        tag = mm_Tag.get_or_create(name=tag_name.replace(' ', ''))[0]
        serializer.save(editor=self.request.user.customer, tag=tag)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        tag_name = serializer.validated_data['tag']['name']
        tag = mm_Tag.get_or_create(name=tag_name.replace(' ', ''))[0]
        serializer.save(editor=self.request.user.customer, tag=tag)


class ArticleViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):

    serializer_class = ArticleSerializer
    queryset = mm_Article.filter(is_published=True)
    filter_class = ArticleFilter

