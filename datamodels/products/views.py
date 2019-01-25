import json
import traceback

from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.products.models import mm_AlipayOrder, mm_ServiceCertification
from lib.pay import alipay_serve


class AliPayNotifyView(APIView):
    """
    支付宝回调接口
    1. 校验结果
    2. 更改订单状态
    3. 创建内部订单
    4. 先关权限逻辑
    """
    @transaction.atomic()
    def post(self, request, format=None):
        data = request.data.dict()
        # sign 不能参与签名验证
        signature = data.pop("sign")
        print(json.dumps(data))
        print(signature)
        # verify
        success = alipay_serve.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            print("trade succeed")
            out_trade_no = data['out_trade_no']
            total_amount = float(data['buyer_pay_amount'])
            order = mm_AlipayOrder.filter(union_trade_no=out_trade_no,
                                          total_amount=total_amount
                                          ).select_related('virtual_service').first()
            if order:
                order.status = mm_AlipayOrder.ORDER_STATU_DONE
                order.save()
                days = json.loads(order.pricelist)[order.price_index]['days']
                mm_ServiceCertification.update_certification(order.customer_id, order.virtual_service, days)

            return Response('success')
        else:
            return Response('failed')
