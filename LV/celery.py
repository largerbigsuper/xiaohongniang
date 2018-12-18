#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 下午1:27
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LV.settings')

app = Celery('LV')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # # Executes every Monday morning at 7:30 a.m.
    # 'add-every-monday-morning': {
    #     'task': 'tasks.add',
    #     'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'args': (16, 16),
    # },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
