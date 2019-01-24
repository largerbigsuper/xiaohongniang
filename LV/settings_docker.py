#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 下午2:54
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : settings_docker.py


class AliYunSMS:
    ACCESS_KEY_ID = "LTAIPQYeKTLNiPUv"
    ACCESS_KEY_SECRET = "wHBmEIr1YNp6rNr8zrK9cjFK1gJsLa"
    SMS_TEMPLATE_NAME = '正能科技'
    SMS_TEMPLATE_ID = 'SMS_152210626'


class QiNiuSettings:
    ACCESS_KEY = 'YU8-GbpmWJ_8UEdBc7VTv4n_eku3zlgoHuUI2l9D'
    SECRET_KEY = 'Mkms7UphbEH4sWdkWoEnqk0PCjD3V84rIZ3EuL_H'
    BUCKET_NAME_DICT = {
        'image': 'img3-workspace',
    }
    BUCKET_DOMAIN_DICT = {
        'image': 'http://pkwzlsa8z.bkt.clouddn.com/'
    }


class RongYunSettings:
    APP_KEY = 'k51hidwqk404b'
    APP_SECRET = 'JV6ZKZWpM4TZ'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'NAME': 'lv_web',
        'PASSWORD': 'lv_web_password',
        'HOST': 'db',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET CHARACTER SET utf8mb4',
            'charset': 'utf8mb4',
        }
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
