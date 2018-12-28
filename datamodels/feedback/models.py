from django.db import models

from datamodels.role.models import Customer
from lib.common import BaseManger


class DealStatus:
    DEAL_STATUS_UNREAD = 0
    DEAL_STATUS_ACCEPTED = 1


DEAL_STATUS_CHOICE = (
    (DealStatus.DEAL_STATUS_UNREAD, '未处理'),
    (DealStatus.DEAL_STATUS_ACCEPTED, '已处理')
)


class FeedBackManager(BaseManger):
    pass


class FeedBack(models.Model):
    customer = models.ForeignKey(Customer, related_name='feedbacks', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='反馈内容', max_length=500)
    create_at = models.DateTimeField(auto_now_add=True)
    deal_status = models.PositiveIntegerField(verbose_name='状态', choices=DEAL_STATUS_CHOICE, default=0)

    objects = FeedBackManager()

    class Meta:
        db_table = 'lv_feedback'


mm_FeedBack = FeedBack.objects
