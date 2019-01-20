import json
import traceback

from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.products.models import mm_VirtualService, mm_AlipayOrder, mm_ServiceCertification
from datamodels.products.serializers import VirtualServiceSerializer
from lib import messages
from lib.pay import alipay_serve
from lib.tools import Tool


class VirtualServiceCreateView(generics.CreateAPIView):

    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = VirtualServiceSerializer


class VirtualServiceListView(generics.ListAPIView):

    serializer_class = VirtualServiceSerializer
    queryset = mm_VirtualService.all()


class VirtualServiceModifyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = VirtualServiceSerializer
    queryset = mm_VirtualService.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            self.permission_classes = (IsAuthenticated, IsAdminUser)
        return super().get_permissions()


class CustomerCitificationListView(generics.ListAPIView):
    pass


class CreateVirtualServiceOrder(APIView):
    """
    下单地址
    1. 购买服务
    """

    def post(self, request, format=None):
        pay_type = request.data.get('pay_type', 1)
        pay_from = request.data.get('pay_from', 'APP')
        service_id = int(request.data.get('service_id'))
        price_index = int(request.data.get('price_index', 0))
        customer_id = request.session['customer_id']
        order_string = None
        try:
            if pay_type == 1:  # 支付宝
                if pay_from == 'APP':
                    order_string = mm_AlipayOrder.create_order(customer_id, service_id, price_index)
            data = {
                'order_string': order_string
            }
            return Response(Tool.format_data(data))
        except:
            error_msg = traceback.format_exc()
            data = {
                'detail': error_msg
            }
            return Response(Tool.format_data(data, messages.FAILED), status=status.HTTP_400_BAD_REQUEST)


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
