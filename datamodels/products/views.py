import json
import logging
import traceback

from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.products.models import mm_Order, mm_ServiceCertification, mm_CustomerOrder, mm_VirtualService
from lib.pay import alipay_serve, wechatpay_serve

logger = logging.getLogger('products')


class AliPayNotifyView(APIView):
    """
    支付宝回调接口
    1. 校验结果
    2. 更改订单状态
    3. 创建内部订单
    4. 先关权限逻辑
    """
    authentication_classes = []

    @transaction.atomic()
    def post(self, request, format=None):
        data = request.data.dict()
        # sign 不能参与签名验证
        signature = data.pop("sign")

        print(json.dumps(data))
        print(signature)
        logger.info('CallBack Data: %s' % json.dumps(data))
        logger.info('CallBack signature: %s' % signature)
        # verify
        success = alipay_serve.verify(data, signature)
        logger.info('CallBack verify result: %s' % success)

        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            try:
                out_trade_no = data['out_trade_no']
                total_amount = float(data['buyer_pay_amount'])
                order = mm_Order.filter(union_trade_no=out_trade_no,
                                        total_amount=total_amount
                                        ).select_related('virtual_service').first()
                if order:
                    order.status = mm_Order.ORDER_STATU_DONE
                    order.trade_no = data['trade_no']
                    order.save()
                    price_info = json.loads(order.virtual_service.pricelist)[order.price_index]
                    days = price_info['days']
                    service_name = order.virtual_service.name
                    price_index_name = price_info['name']
                    mm_CustomerOrder.add_order(order.customer, 1, order, out_trade_no, service_name,
                                               price_index_name, total_amount)
                    if order.virtual_service.service_type in mm_VirtualService.Service_Group_Vip:
                        mm_ServiceCertification.update_certification(order.customer_id, order.virtual_service, days)
                    elif order.virtual_service.service_type in mm_VirtualService.Service_Group_Card:
                        mm_VirtualService.modify_card(order.customer_id, order.virtual_service.service_type, 1)
                    else:
                        pass
            except:
                logger.error('Error: %s ' % traceback.format_exc())
            finally:
                return Response('success')
        else:
            return Response('failed')


class WechatPayNotifyView(APIView):
    """微信支付回调"""

    authentication_classes = []

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        微信异步通知
        """
        raw_data = request.body.decode("utf-8")
        logger.info('Wechatpay CallBack Data: %s' % json.dumps(raw_data))
        data = wechatpay_serve.to_dict(raw_data)
        if not wechatpay_serve.check(data):
            return wechatpay_serve.reply("签名验证失败", False)
        # 处理业务逻辑

        total_fee = int(data['total_fee'])
        out_trade_no = data['out_trade_no']
        order = mm_Order.filter(union_trade_no=out_trade_no,
                                total_amount=total_fee/100
                                ).select_related('virtual_service').first()
        if order:
            order.status = mm_Order.ORDER_STATU_DONE
            order.trade_no = data['transaction_id']
            order.save()
            price_info = json.loads(order.virtual_service.pricelist)[order.price_index]
            days = price_info['days']
            service_name = order.virtual_service.name
            price_index_name = price_info['name']
            mm_CustomerOrder.add_order(order.customer, 2, order, out_trade_no, service_name,
                                       price_index_name, total_fee/100)
            if order.virtual_service.service_type in mm_VirtualService.Service_Group_Vip:
                mm_ServiceCertification.update_certification(order.customer_id, order.virtual_service, days)
            elif order.virtual_service.service_type in mm_VirtualService.Service_Group_Card:
                mm_VirtualService.modify_card(order.customer_id, order.virtual_service.service_type, 1)
            else:
                pass
        return wechatpay_serve.reply("OK", True)

