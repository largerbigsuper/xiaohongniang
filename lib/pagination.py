#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/16 下午3:03
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : pagination.py
from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response

from lib.tools import Tool


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(Tool.format_data(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_count', self.page.paginator.num_pages),
            ('results', data)
        ])))
