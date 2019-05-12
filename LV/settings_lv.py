#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/30 下午2:09
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : settings_lv.py


class Platform:

    WEB = 0
    ANDROID = 1
    IOS = 2

    Hans_Mapping = {
        WEB: '网页',
        ANDROID: '安卓',
        IOS: '苹果',
    }


NORNAML_CUSTOMER_CHAT_TIMES_LIMIT_PER_DAY = 3  # 每天免费聊天次数
NORNAML_CUSTOMER_BOTTLE_PICK_TIMES_LIMIT_PER_DAY = 5  # 每天捡漂流瓶次数
NORNAML_CUSTOMER_BOTTLE_REPLY_TIMES_LIMIT_PER_DAY = 5  # 每天扔漂流瓶次数
