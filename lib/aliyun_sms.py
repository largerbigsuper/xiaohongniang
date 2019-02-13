#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午2:21
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : aliyun_sms.py
# -*- coding: utf-8 -*-
import json
import random
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT

from LV.settings import AliYunSMS

"""
短信业务调用接口示例，版本号：v20170525

Created on 2017-06-12

"""

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"

acs_client = AcsClient(AliYunSMS.ACCESS_KEY_ID, AliYunSMS.ACCESS_KEY_SECRET, REGION)
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def gen_code():
    return ''.join(random.sample(list(map(str, range(10))), 4))


def send_simple_code(phone_number, code):
    """发送注册码"""
    return _send_sms(uuid.uuid1(), phone_number, AliYunSMS.SMS_TEMPLATE_NAME, AliYunSMS.SMS_TEMPLATE_ID, {'code': code})


def _send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    """
    :param template_param:
    :return: b'{"Message":"OK","RequestId":"EA2BC3D5-26F1-42E6-A928-413D1493256F","BizId":"836102743645158736^0","Code":"OK"}'

    """
    smsRequest = SendSmsRequest.SendSmsRequest()
    # 申请的短信模板编码,必填
    smsRequest.set_TemplateCode(template_code)
    # 短信模板变量参数
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    # 设置业务请求流水号，必填。
    smsRequest.set_OutId(business_id)
    # 短信签名
    smsRequest.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)

    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)

    # 短信发送的号码列表，必填。
    smsRequest.set_PhoneNumbers(phone_numbers)

    # 调用短信发送接口，返回json
    response = acs_client.do_action_with_exception(smsRequest)

    # TODO 业务处理
    return json.loads(response.decode('utf-8'))


if __name__ == '__main__':
    __business_id = uuid.uuid1()
    params = {'code': '12325'}
    print(_send_sms(__business_id, "18258185399", "正能科技", "SMS_152210626", params))
