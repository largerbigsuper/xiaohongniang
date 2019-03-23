#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/23 下午6:08
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : settiongs_production.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/4 下午2:54
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : settings_docker.py
import os
DOMAIN = 'https://www.handanxiaohongniang.com'


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
        'image': 'http://lhxq.top/'
    }


QINIU_ACCESS_KEY = QiNiuSettings.ACCESS_KEY
QINIU_SECRET_KEY = QiNiuSettings.SECRET_KEY
QINIU_BUCKET_NAME = QiNiuSettings.BUCKET_NAME_DICT['image']
QINIU_BUCKET_DOMAIN = QiNiuSettings.BUCKET_DOMAIN_DICT['image']
QINIU_SECURE_URL = False


class RongYunSettings:
    APP_KEY = 'mgb7ka1nmdwtg'
    APP_SECRET = 'yKLJ0i0bmLZP'


class AlipaySettings:
    _root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_ID = '2019013063154821'
    APP_PRIVATE_KEY = os.path.join(_root_dir, 'lib/alipay/test_app_private.txt')
    ALIPAY_PUBLIC_KEY = os.path.join(_root_dir, 'lib/alipay/test_alipay_public_key_sha256.txt')
    VIRTUAL_SERVICE_NOTIFY_URI = DOMAIN + '/products/alipay/notify/'


class MinprogramSettings:
    APP_ID = 'wxdcbd25406b60939d'
    APP_SECRET = 'cda1c1d81e62f458256fc142e75d0249'
    LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session' \
                '?appid={}&secret={}&grant_type=authorization_code&js_code='.format(APP_ID, APP_SECRET)


class WeChatPaySettings:
    WEIXIN_APP_ID = 'wx502707dff6e8ce6c'
    WEIXIN_APP_SECRET = '7968e86926fc96525807d0256edaadff'
    WEIXIN_MCH_ID = '1527643731'
    WEIXIN_MCH_KEY = 'handanxiaohongniang1234567890000'
    WEIXIN_NOTIFY_URL = DOMAIN + '/products/wechatpay/notify/'



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

CSRF_TRUSTED_ORIGINS = ['servicewechat.com', 'handanxiaohongniang.com']
