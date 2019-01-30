#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/22 下午7:17
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as filters

from datamodels.bottles.api.serializers import BottleSerializer, BottleDetailSerializer, PickedBottlesSerializer, \
    AdminBottleSerializer
from datamodels.bottles.models import mm_Bottles, mm_BottlePickerRelation, Bottle
from datamodels.stats.models import mm_CustomerPoint
from lib import messages
from lib.viewsets import AdminViewSet


class BottlesFilter(filters.FilterSet):
    class Meta:
        model = Bottle
        fields = {
            'text': ['icontains'],
            'create_at': ['iexact', 'gte', 'lte']
        }


class BottlesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = BottleDetailSerializer

    def get_queryset(self):
        return mm_Bottles.exclude(customer=self.request.user.customer)

    @action(methods=['get'], detail=False)
    def pickone(self, request):
        """捡瓶子"""
        bottle = mm_Bottles.optional_bottles(request.user.customer.id).first()
        if bottle:
            mm_BottlePickerRelation.create(bottle=bottle, customer=request.user.customer)
            serializer = self.serializer_class(bottle, context={'request': request})
            mm_CustomerPoint.add_action(self.request.user.customer.id, mm_CustomerPoint.Action_Pick_Bottle)
            return Response(serializer.data)
        else:
            return Response(data={'detail': messages.NO_DATA}, status=status.HTTP_400_BAD_REQUEST)


class MyBottlesViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = BottleSerializer

    def get_queryset(self):
        return mm_Bottles.filter(customer=self.request.user.customer)

    def get_serializer_class(self):
        if self.serializer_class:
            return self.serializer_class

    def perform_create(self, serializer):
        mm_CustomerPoint.add_action(self.request.user.customer.id, mm_CustomerPoint.Action_Add_Bottle)
        serializer.save(customer=self.request.user.customer)


class PickedBottlesViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                           mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = PickedBottlesSerializer

    def get_queryset(self):
        return mm_BottlePickerRelation.filter(customer_id=self.request.session['customer_id'])


class AdminBottlesViewSet(AdminViewSet):
    # permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = AdminBottleSerializer
    queryset = mm_Bottles.all()
    filterset_class = BottlesFilter
