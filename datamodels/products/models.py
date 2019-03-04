import json
from datetime import datetime, timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F

from LV.settings import AlipaySettings
from datamodels.role.models import mm_Customer
from lib import pay
from lib.common import BaseManger
from lib.exceptions import ParamException
from lib.pay import alipay_serve


class VirtualServiceManager(BaseManger):
    Service_Vip = 1
    Service_Show_Index = 2
    Service_Online_Card = 3
    Service_Offline_Card = 4

    Service_Group_Vip = [Service_Vip, Service_Show_Index]
    Service_Group_Card = [Service_Online_Card, Service_Offline_Card]

    SERVICE_TYPE_CHOICE = (
        (Service_Vip, '会员'),
        (Service_Show_Index, '首页显示'),
        (Service_Online_Card, '红娘线上服务卡'),
        (Service_Offline_Card, '红娘线下服务卡'),

    )

    Demand_Type_2_Service_Type = {
        1: Service_Online_Card,  # 线下服务卡
        2: Service_Offline_Card,  # 线上服务卡
    }

    PRICELIST_FIELD_MAPPING = {
        "name": (str,),
        "days": (int,),
        "price": (int, float),
    }

    def check_pricelist_format(self, pricelist):
        try:
            pricelist_json = json.loads(pricelist)
            for price_dict in pricelist_json:
                for k, v in price_dict.items():
                    if k not in self.PRICELIST_FIELD_MAPPING:
                        msg = '不支持参数%s' % k
                        raise ParamException(msg)
                    if not isinstance(v, self.PRICELIST_FIELD_MAPPING[k]):
                        msg = '%s参数格式错误'
                        raise ParamException(msg)
        except:
            raise ParamException('pricelist 格式应为json')

    def modify_card(self, customer_id, service_type=Service_Online_Card, amount=1):
        if service_type == self.Service_Online_Card:
            mm_Customer.filter(pk=customer_id).update(online_card_count=F('online_card_count') + amount)
        elif service_type == self.Service_Offline_Card:
            mm_Customer.filter(pk=customer_id).update(offline_card_count=F('offline_card_count') + amount)


class VirtualService(models.Model):
    """
    平台虚拟服务
    :pricelist
    [
        {
            "name": "首页置顶3天",
            "days": 3,
            "price": 200.0,
         },

    ]
    """

    service_type = models.PositiveSmallIntegerField(verbose_name='服务类型',
                                                    choices=VirtualServiceManager.SERVICE_TYPE_CHOICE,
                                                    default=1,
                                                    db_index=True)
    name = models.CharField(verbose_name='产品名', max_length=20, db_index=True)
    pricelist = models.CharField(verbose_name='价格表', max_length=1000, default='[]')
    detail = models.CharField(verbose_name='详情', max_length=1000, null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = VirtualServiceManager()

    class Meta:
        db_table = 'lv_virtual_service'
        verbose_name = '付费服务'
        verbose_name_plural = '付费服务'

    def pricelist_admin(self):
        price_str = ''
        for p in json.loads(self.pricelist):
            price_str += '{}-{}天-{}元'.format(p['name'], p['days'], p['price'])
        return price_str

    pricelist_admin.short_description = '价格套餐'

    def __str__(self):
        return self.name


class ServiceCertificationManager(BaseManger):

    def update_certification(self, customer_id, virtual_service, days):
        certification, created = self.get_or_create(customer_id=customer_id, virtual_service_id=virtual_service.id)
        if certification.expired:
            expired_at = datetime.now() + timedelta(days=days)

        else:
            expired_at = certification.expired_at + timedelta(days=days)
        certification.expired_at = expired_at
        certification.save()
        if virtual_service.service_type == mm_VirtualService.Service_Vip:
            mm_Customer.filter(pk=customer_id).update(service_vip_expired_at=certification.expired_at)
        elif virtual_service.service_type == mm_VirtualService.Service_Show_Index:
            mm_Customer.filter(pk=customer_id).update(service_show_index_expired_at=certification.expired_at)
        else:
            pass

    def get_customer_certifications(self, customer_id):
        return self.select_related('virtual_service').filter(customer_id=customer_id)


class ServiceCertification(models.Model):
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='用户', db_index=False)
    virtual_service = models.ForeignKey('products.VirtualService', on_delete=models.CASCADE, verbose_name='服务名',
                                        db_index=False)
    expired_at = models.DateTimeField(verbose_name='有效期', null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = ServiceCertificationManager()

    class Meta:
        db_table = 'lv_service_certification'
        unique_together = [
            ('customer', 'virtual_service')
        ]
        index_together = [
            ('customer', 'virtual_service')
        ]
        verbose_name = '付费服务统计'
        verbose_name_plural = '付费服务统计'

    @property
    def expired(self):
        if self.expired_at:
            return self.expired_at < datetime.now()
        else:
            return True


class AlipayOrderManager(BaseManger):
    ORDER_STATU_UNPAY = 0
    ORDER_STATU_DONE = 1

    def add(self, customer_id, virtual_service_id,
            union_trade_no, service_name, price_index_name,
            price_index, total_amount, status=0):
        return self.create(customer_id=customer_id,
                           virtual_service_id=virtual_service_id,
                           union_trade_no=union_trade_no,
                           service_name=service_name,
                           price_index_name=price_index_name,
                           price_index=price_index,
                           total_amount=total_amount,
                           status=status
                           )

    def create_order(self, customer_id, service_id, price_index, pay_from='APP'):
        service = VirtualService.objects.get(pk=service_id)
        price_info = json.loads(service.pricelist)[price_index]
        subject = price_info['name']
        total_amount = price_info['price']
        out_trade_no = pay.gen_union_trade_no()
        order = self.add(customer_id=customer_id,
                         virtual_service_id=service.id,
                         union_trade_no=out_trade_no,
                         service_name=service.name,
                         price_index_name=subject,
                         price_index=price_index,
                         total_amount=total_amount,
                         )
        order_string = None
        if pay_from == 'APP':
            order_string = alipay_serve.api_alipay_trade_app_pay(
                out_trade_no=out_trade_no,
                total_amount=total_amount,
                subject=subject,
                notify_url=AlipaySettings.VIRTUAL_SERVICE_NOTIFY_URI,
                timeout_express='15m'
            )
        return order_string


class AlipayOrder(models.Model):
    STATUS_CHOICE = (
        (0, '未支付'),
        (1, '已支付'),
    )
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='购买人')
    status = models.PositiveSmallIntegerField(verbose_name='订单状态', choices=STATUS_CHOICE, default=0)
    virtual_service = models.ForeignKey('products.VirtualService', on_delete=models.CASCADE, verbose_name='服务')
    union_trade_no = models.CharField(verbose_name='内部订单号', max_length=100, unique=True, blank=True)
    trade_no = models.CharField(verbose_name='流水号', max_length=100, blank=True, null=True)
    service_name = models.CharField(verbose_name='服务名称', max_length=100)
    price_index_name = models.CharField(verbose_name='套餐名称', max_length=100)
    price_index = models.PositiveSmallIntegerField(verbose_name='套餐id', default=0)
    total_amount = models.FloatField(verbose_name='总额', default=0)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = AlipayOrderManager()

    class Meta:
        db_table = 'lv_alipay_orders'
        verbose_name = '支付宝订单管理'
        verbose_name_plural = '支付宝订单管理'

    def __str__(self):
        return '<AlipayOrder: {}>'. format(self.id)


class CustomerOrderManager(BaseManger):

    def add_order(self, customer, pay_type, order, union_trade_no, service_name, price_index_name, total_amount):
        self.create(customer=customer,
                    pay_type=pay_type,
                    content_object=order,
                    union_trade_no=union_trade_no,
                    service_name=service_name,
                    price_index_name=price_index_name,
                    total_amount=total_amount
                    )


class CustomerOrder(models.Model):
    PAY_TYPE_CHOICE = (
        (1, '支付宝'),
    )
    Content_Type_Choice = (
        (ContentType.objects.get_for_model(AlipayOrder).id, '支付宝'),
    )
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='购买人')
    pay_type = models.PositiveSmallIntegerField(verbose_name='支付方式', choices=PAY_TYPE_CHOICE, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False,
                                     choices=Content_Type_Choice, default=Content_Type_Choice[0][0])
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    union_trade_no = models.CharField(verbose_name='内部订单号', max_length=100, unique=True, blank=True)
    service_name = models.CharField(verbose_name='服务名称', max_length=100)
    price_index_name = models.CharField(verbose_name='套餐名称', max_length=100)
    total_amount = models.FloatField(verbose_name='总额', default=0)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = CustomerOrderManager()

    class Meta:
        db_table = 'lv_customer_orders'
        verbose_name = '订单管理'
        verbose_name_plural = '订单管理'


class SkuManager(BaseManger):
    pass


class Sku(models.Model):

    name = models.CharField(verbose_name='商品名', max_length=100, db_index=True)
    cover_image = models.ImageField(verbose_name='封面图')
    description = models.CharField(verbose_name='产品简介', max_length=200)
    total = models.PositiveIntegerField(verbose_name='总量', default=0)
    point = models.PositiveIntegerField(verbose_name='所需积分', default=0)
    in_sale = models.BooleanField(verbose_name='在售', default=False)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = SkuManager()

    class Meta:
        db_table = 'lv_sku'
        verbose_name = verbose_name_plural = '兑换商品管理'

    def __str__(self):
        return self.name


class SkuExchageManager(BaseManger):

    Status_Submited = 0
    Status_Done = 1
    Status_Refused = 2

    Status_Choice = (
        (Status_Submited, '已提交'),
        (Status_Done, '已兑换'),
        (Status_Refused, '拒绝兑换'),
    )

    def exchage(self, customer_id, sku_id):
        return self.create(customer_id=customer_id, sku_id=sku_id)


class SkuExchage(models.Model):

    customer = models.ForeignKey('role.Customer', verbose_name='申请人', on_delete=models.CASCADE)
    sku = models.ForeignKey(Sku, verbose_name='申请的商品', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(verbose_name='申请状态',
                                              choices=SkuExchageManager.Status_Choice,
                                              default=SkuExchageManager.Status_Submited)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = SkuExchageManager()

    class Meta:
        db_table = 'lv_sku_exchage'
        verbose_name = verbose_name_plural = '兑换申请管理'


mm_VirtualService = VirtualService.objects
mm_ServiceCertification = ServiceCertification.objects
mm_CustomerOrder = CustomerOrder.objects
mm_AlipayOrder = AlipayOrder.objects
mm_Sku = Sku.objects
mm_SkuExchage = SkuExchage.objects
