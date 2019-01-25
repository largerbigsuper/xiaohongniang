#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:37
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : router.py
from rest_framework import routers

from datamodels.articles.api.viewsets import AdminArticleViewSet, ArticleViewSet, AdminTagViewSet
from datamodels.bottles.api.viewsets import BottlesViewSet, PickedBottlesViewSet, MyBottlesViewSet, AdminBottlesViewSet
from datamodels.feedback.api.viewsets import AdminReportViewSet, AdminFeedBackViewSet
from datamodels.moments.api.viewsets import AdminTopicViewSet, AdminMomentsViewSet
from datamodels.products.api.viewsets import AdminVirtualServiceViewSet, CustomerVirtualServiceViewSet, \
    AdminServiceCertificationViewSet
from datamodels.role.api.veiwsets import AdminCustomerViewSet, AdminOpreationViewSet

router = routers.DefaultRouter()
router.register('bottles', BottlesViewSet, base_name='bottles')
router.register('bottles-mine', MyBottlesViewSet, base_name='bottles-mine')
router.register('bottles-picked', PickedBottlesViewSet, base_name='bottles-picked')
router.register('virtual-services', CustomerVirtualServiceViewSet, base_name='virtual-services')
router.register('articles', ArticleViewSet, base_name='article')

router.register('admin/op', AdminOpreationViewSet, base_name='admin-op')
router.register('admin/customers', AdminCustomerViewSet, base_name='admin-customers')
router.register('admin/bottles', AdminBottlesViewSet, base_name='admin-bottles')
router.register('admin/topics', AdminTopicViewSet, base_name='admin-topics')
router.register('admin/moments', AdminMomentsViewSet, base_name='admin-moments')
router.register('admin/feedbacks', AdminFeedBackViewSet, base_name='admin-feedbacks')
router.register('admin/reports', AdminReportViewSet, base_name='admin-reports')
router.register('admin/virtual-services', AdminVirtualServiceViewSet, base_name='admin-virtual-service')
router.register('admin/customer-services', AdminServiceCertificationViewSet, base_name='admin-virtual-service')
router.register('admin/tags', AdminTagViewSet, base_name='admin-tag')
router.register('admin/articles', AdminArticleViewSet, base_name='admin-article')

