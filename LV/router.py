#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午1:37
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : router.py
from rest_framework import routers

from datamodels.bottles.api.viewsets import BottlesViewSet, PickedBottlesViewSet, MyBottlesViewSet
from datamodels.role.api.veiwsets import CustomerViewSet

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, base_name='customer')
router.register('bottles', BottlesViewSet, base_name='bottles')
router.register('bottles-mine', MyBottlesViewSet, base_name='bottles-mine')
router.register('bottles-picked', PickedBottlesViewSet, base_name='bottles-picked')
