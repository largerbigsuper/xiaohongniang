#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 下午1:36
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : task.py
from celery import shared_task


@shared_task
def hello():
    print('Hello there!')