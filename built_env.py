#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午4:04
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : built_env.py
import os
from subprocess import call
BASE_DIR = os.getcwd()
call(['pip', 'install', '--upgrade', 'pip',
      '-i', 'http://mirrors.aliyun.com/pypi/simple/', '--trusted-host', 'mirrors.aliyun.com'])

# step1
call(['pip', 'install', '-r', 'requirements.txt',
      '-i', 'http://mirrors.aliyun.com/pypi/simple/', '--trusted-host', 'mirrors.aliyun.com'])
# step2
# call(['pip', 'install', 'git+https://github.com/htwenning/aliyun-python-sdk-core'])
# call(['pip', 'install', 'git+https://github.com/htwenning/aliyun-python-sdk-dysmsapi'])
# call(['pip', 'install', 'git+https://github.com/rongcloud/server-sdk-python.git'])
# aliyun_python_sdk_core = BASE_DIR + '/python-lib/aliyun-python-sdk-core'
aliyun_python_sdk_dysmsapi = BASE_DIR + '/python-lib/aliyun-python-sdk-dysmsapi'
server_sdk_python = BASE_DIR + '/python-lib/server-sdk-python'
# call(['pip', 'install', aliyun_python_sdk_core])
call(['pip', 'install', aliyun_python_sdk_dysmsapi])
call(['pip', 'install', server_sdk_python])



