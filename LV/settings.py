"""
Django settings for LV project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

ENV = os.getenv('DJANGO_RUN_ENV', 'DEV')
if ENV == 'TEST':
    from .settings_docker import *
    DEBUG = False
    ALLOWED_HOSTS = ['*']

else:
    from .common_settings import *
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^ww=aak_o4#=nue97+8@=7g)m+t_b33qqv%o)_^r5ypc%a^)g0'

# SECURITY WARNING: don't run with debug turned on in production!



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTS_APPS = [
    'rest_framework',
    'django_filters',
    'crispy_forms',
    # 'rest_framework.authtoken'
]

CUSTOM_APPS = [
    'datamodels.sms',
    'datamodels.role',
    'datamodels.moments',
    'datamodels.notices',
    'datamodels.feedback',
    'datamodels.stats',
    'datamodels.bottles',
]

INSTALLED_APPS += THIRD_PARTS_APPS
INSTALLED_APPS += CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lib.middleware.ResponseFormateMiddleware',
]

ROOT_URLCONF = 'LV.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LV.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

# TIME_ZONE = 'zh-hans'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

# Thtird parts settings

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'lib.pagination.CustomPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    # 'EXCEPTION_HANDLER': 'lib.handlers.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'lib.render.FormatedJSONRenderer',
        # 'lib.render.FormatedBrowsableAPIRenderer',
        # 'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)

}

# APPEND_SLASH = False

ADMINS = [
    ('admin', 'zaihuazhao@163.com'),
]


SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_CACHE_ALIAS = "default"
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
CSRF_COOKIE_AGE = 60 * 60 * 24 * 7 * 2

# X-XSRF-TOKEN
# CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'
# CSRF_COOKIE_SECURE = False

# DATE_FORMAT = ''
# DATETIME_FORMAT = ''

EMAIL_FILE_PATH = ''

# 周一为第一天
FIRST_DAY_OF_WEEK = 1

# 错误邮件名
SERVER_EMAIL = 'lv@localhost'

# LOGIN_REDIRECT_URL = '/accounts/profile/'
# LOGIN_URL = '/accounts/login/'
# LOGOUT_REDIRECT_URL = ''

# logging settings
# logger name datamodels.appname.views
# logger = logging.getLogger(__name__)

LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_WARNING = 'WARNING'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_CRITICAL = 'CRITICAL'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        },
        "django_file": {
            "level": LOG_LEVEL_INFO,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./log/access.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
        "request_file": {
            "level": LOG_LEVEL_ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./log/requests.log",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file', 'mail_admins'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


for app_name in CUSTOM_APPS:
    handler_name = app_name
    handler_config = {
        "level": LOG_LEVEL_INFO,
        "class": "logging.handlers.RotatingFileHandler",
        "filename": "./log/" + app_name + ".log",
        "maxBytes": 1024 * 1024 * 10,  # 10MB
        "backupCount": 10,
        "formatter": "verbose"
    }
    LOGGING['handlers'][handler_name] = handler_config
    logger_name = app_name + '.views'
    logger_config = {
        'handlers': ['console', handler_name],
        'level': 'INFO',
    }
    LOGGING['loggers'][logger_name] = handler_config

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#         },
#     },
# }

CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
