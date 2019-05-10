#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/29 下午8:26
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : viewsets.py
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from datamodels.sms.api.serializers import SMSSerializer
from datamodels.sms.models import mm_SMSCode
from lib.aliyun_sms import gen_code, send_simple_code
from lib.exceptions import SMSExcecption
from lib.middleware import CsrfExemptSessionAuthentication
from lib.tools import Tool


class SMSViewSet(mixins.CreateModelMixin, GenericViewSet):

    permission_classes = []
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = SMSSerializer

    def create(self, request, *args, **kwargs):
        Tool.required_params(request, ['account'])
        account = request.data.get('account')
        code = gen_code()
        if not mm_SMSCode.can_get_new_code(tel=account):
            raise SMSExcecption('请过几分钟尝试')
        response = send_simple_code(account, code)
        if response['Code'] == 'OK':
            mm_SMSCode.add(account, code)
            return Response(Tool.format_data())
        else:
            raise SMSExcecption(response['Message'])
