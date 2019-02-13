#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/19 下午3:59
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : pay.py
import string
from datetime import datetime
from random import choice

from alipay import AliPay

from LV.settings import AlipaySettings


def gen_union_trade_no(pay_type=1):
    """
    生成内部订单号
    格式：
    {pay_type}{20190119161237}{0001}
    :param pay_type:
    :return:
    """
    create_time = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join([choice(string.digits) for _ in range(4)])
    return '{pay_type}{create_time}{random_str}'.format(pay_type=pay_type,
                                                        create_time=create_time,
                                                        random_str=random_str
                                                        )


alipay_serve = AliPay(
    appid=AlipaySettings.APP_ID,
    app_notify_url=None,  # 默认回调url
    app_private_key_path=AlipaySettings.APP_PRIVATE_KEY,
    alipay_public_key_path=AlipaySettings.APP_PUBLIC_KEY,
    sign_type="RSA",
    debug=True
)

# alipay_serve = None