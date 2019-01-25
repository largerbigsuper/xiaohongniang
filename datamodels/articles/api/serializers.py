#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/25 下午3:51
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : serializers.py
from rest_framework import serializers

from datamodels.articles.models import Article, Tag


class TagSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class AdminTagSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'level')


class AdminArticleSerializer(serializers.ModelSerializer):
    tag = TagSerialzier()

    class Meta:
        model = Article
        fields = ('category', 'headline', 'content', 'create_at', 'is_published', 'tag')


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('category', 'headline', 'content', 'create_at')