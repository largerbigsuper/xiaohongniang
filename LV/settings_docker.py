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


QINIU_ACCESS_KEY = QiNiuSettings.ACCESS_KEY
QINIU_SECRET_KEY = QiNiuSettings.SECRET_KEY
QINIU_BUCKET_NAME = QiNiuSettings.BUCKET_NAME_DICT['image']
QINIU_BUCKET_DOMAIN = QiNiuSettings.BUCKET_DOMAIN_DICT['image']
QINIU_SECURE_URL = False


class RongYunSettings:
    APP_KEY = 'k51hidwqk404b'
    APP_SECRET = 'JV6ZKZWpM4TZ'


class AlipaySettings:
    APP_PRIVATE_KEY = """
    """
    APP_PUBLIC_KEY = """
    """
    VIRTUAL_SERVICE_NOTIFY_URI = 'https://www.lhxq.top:8443/products/alipay/notify/'


class MinprogramSettings:
    APP_ID = 'wxf54e0eb3b0c3695d'
    APP_SECRET = 'f439732d65b949dba943f0eaf809ba50'
    LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session' \
                '?appid={}&secret={}&grant_type=authorization_code&js_code='.format(APP_ID, APP_SECRET)


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

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
