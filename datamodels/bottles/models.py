from django.db import models

from lib.common import BaseManger


class BottleManager(BaseManger):

    def my_bottles(self, customer_id):
        return self.filter(customer_id=customer_id)

    def my_picked_bottles(self, customer_id):
        return self.filter(picker__id=customer_id).order_by('-pick_at')

    def optional_bottles(self, customer_id):
        return self.exclude(customer_id=customer_id).filter(picker__id__isnull=True).order_by('?')


class Bottle(models.Model):
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='发布人')
    text = models.CharField(verbose_name='正文', max_length=200)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    picker = models.ForeignKey('role.Customer', on_delete=models.CASCADE,
                               related_name='pickers', null=True, blank=True,
                               verbose_name='捡到的人')
    pick_at = models.DateTimeField(verbose_name='捡到时间', blank=True, null=True)

    objects = BottleManager()

    class Meta:
        db_table = 'lv_bottles'
        ordering = ['-create_at']
        verbose_name = '漂流瓶'
        verbose_name_plural = '漂流瓶管理'


mm_Bottles = Bottle.objects
