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
from datamodels.notices.api.viewsets import DemandViewSet, MyWechatCardViewSet
from datamodels.products.api.viewsets import AdminVirtualServiceViewSet, CustomerVirtualServiceViewSet, \
    AdminServiceCertificationViewSet, SkuViewSet, SkuExchageViewSet
from datamodels.role.api.viewsets import  CustomerViewSet, InviteRecordViewSet
from datamodels.role.api.viewset_admin import AdminInviteRecordViewSet, AdminOpreationViewSet, AdminCustomerViewSet
from datamodels.stats.api.viewsets import PointViewSet, AdminPointViewSet, MessageTemplateViewSet, \
    CustomerBonusRecordViewSet, WithDrawRecordViewSet

router = routers.DefaultRouter()
router.register('bottles', BottlesViewSet, base_name='bottles')
router.register('bottles-mine', MyBottlesViewSet, base_name='bottles-mine')
router.register('bottles-picked', PickedBottlesViewSet, base_name='bottles-picked')
router.register('virtual-services', CustomerVirtualServiceViewSet, base_name='virtual-services')
router.register('articles', ArticleViewSet, base_name='article')
router.register('points', PointViewSet, base_name='point')
router.register('customers', CustomerViewSet, base_name='customer')
router.register('invite-records', InviteRecordViewSet, base_name='invite-record')
router.register('demands', DemandViewSet, base_name='demand')
router.register('wechatcards', MyWechatCardViewSet, base_name='wechatcard')
router.register('message-templates', MessageTemplateViewSet, base_name='message-tempalte')
router.register('skus', SkuViewSet, base_name='sku')
router.register('sku-exchages', SkuExchageViewSet, base_name='sku-exchage')
router.register('bonus', CustomerBonusRecordViewSet, base_name='bonus')
router.register('withdraw', WithDrawRecordViewSet, base_name='withdraw')


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
router.register('admin/points', AdminPointViewSet, base_name='admin-point')
router.register('admin/invite-records', AdminInviteRecordViewSet, base_name='admin-invite-record')


