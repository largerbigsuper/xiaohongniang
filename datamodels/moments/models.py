from django.db import models

from datamodels.role.models import Customer
from lib.common import BaseManger


class MomentsManager(BaseManger):
    pass


class Moments(models.Model):
    customer = models.ForeignKey(Customer, related_name='moments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='正文', max_length=1500, null=True, blank=True)
    images = models.CharField(verbose_name='图片', max_length=1000, default='[]', blank=True)
    latitude = models.FloatField(verbose_name='精度', null=True, blank=True)
    longitude = models.FloatField(verbose_name='维度', null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    objects = MomentsManager()

    class Meta:
        db_table = 'lv_moments'
        index_together = [
            ('latitude', 'longitude')
        ]


mm_Moments = Moments.objects
