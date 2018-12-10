#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午4:04
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : built_env.py
from subprocess import call

# step1
call(['pip', 'install', '-r', 'requirements.txt'])
# step2
# call(['pip', 'install', 'git+https://github.com/htwenning/aliyun-python-sdk-core'])
call(['pip', 'install', 'git+https://github.com/htwenning/aliyun-python-sdk-dysmsapi'])
call(['pip', 'install', 'git+https://github.com/rongcloud/server-sdk-python.git'])


