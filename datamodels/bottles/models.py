from django.db import models

from lib.common import BaseManger


class BottleManager(BaseManger):

    def my_bottles(self, customer_id):
        return self.filter(customer_id=customer_id)

    def my_picked_bottles(self, customer_id):
        return self.filter(pickers__id=customer_id)

    def optional_bottles(self, customer_id):
        return self.exclude(customer_id=customer_id).exclude(pickers__id=customer_id).order_by('?')


class Bottle(models.Model):
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE)
    text = models.CharField(verbose_name='正文', max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    pickers = models.ManyToManyField('role.Customer', through='BottlePickerRelation', related_name='bottle_pickers')

    objects = BottleManager()

    class Meta:
        db_table = 'lv_bottles'
        ordering = ['-create_at']
        verbose_name = '漂流瓶'
        verbose_name_plural = '漂流瓶管理'


class BottlePickerRelationManager(BaseManger):
    pass


class BottlePickerRelation(models.Model):
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE, db_index=False, unique=True)
    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, db_index=False)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = BottlePickerRelationManager()

    class Meta:
        db_table = 'lv_bottle_picker_relations'
        index_together = [
            ('bottle', 'customer')
        ]
        ordering = ['-create_at']
        verbose_name = '漂流瓶与用户关系管理'
        verbose_name_plural = '漂流瓶与用户关系管理'


mm_Bottles = Bottle.objects
mm_BottlePickerRelation = BottlePickerRelation.objects
