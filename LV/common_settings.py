#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 上午11:58
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : common_settings.py


class AliYunSMS:
    ACCESS_KEY_ID = "LTAIPQYeKTLNiPUv"
    ACCESS_KEY_SECRET = "wHBmEIr1YNp6rNr8zrK9cjFK1gJsLa"
    SMS_TEMPLATE_NAME = '正能科技'
    SMS_TEMPLATE_ID = 'SMS_152210626'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'NAME': 'lv',
        'PASSWORD': 'Password123/',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {

        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}