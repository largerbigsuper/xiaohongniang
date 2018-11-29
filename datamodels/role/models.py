from django.contrib.auth.models import User
from django.db import models

from lib.common import BaseManger


class BaseRole(models.Model):
    GENDER_CHOICE = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=20)
    age = models.PositiveSmallIntegerField('年龄', null=True, blank=True)
    gender = models.IntegerField('性别', choices=GENDER_CHOICE, default=0)
    avatar = models.CharField('头像', max_length=120, blank=True)
    login_tel = models.CharField('电话', max_length=11, unique=True)
    wechat_id = models.CharField('微信号', max_length=24, blank=True)
    # intro = models.CharField('自我简介', max_length=24, blank=True)

    class Meta:
        abstract = True


class CustomerManager(BaseManger):
    pass


class Customer(BaseRole):
    objects = CustomerManager()

    class Meta:
        db_table = 'lv_customers'


mm_Customer = Customer.objects
