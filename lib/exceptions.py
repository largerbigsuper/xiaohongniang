#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午11:31
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : exceptions.py


class LVException(Exception):

    def __init__(self, msg, code=1):
        self.msg = msg
        self.code = code
