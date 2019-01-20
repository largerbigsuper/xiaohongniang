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


class ReportManager(BaseManger):
    Report_Type_1 = 1
    Report_Type_2 = 2
    Report_Type_3 = 3
    Report_Type_4 = 4
    Report_Type_5 = 5
    Report_Type_6 = 6
    Report_Type_7 = 7

    Report_Type_Choice = (
        (Report_Type_1, '虚假信息'),
        (Report_Type_2, '骚扰、广告'),
        (Report_Type_3, '辱骂不文明行为'),
        (Report_Type_4, '色情、暴力'),
        (Report_Type_5, '酒托、婚托、饭托'),
        (Report_Type_6, '欺骗行为'),
        (Report_Type_7, '其他'),
    )


class Report(models.Model):
    """
    举报
    """
    customer = models.ForeignKey(Customer, related_name='reports', on_delete=models.CASCADE, verbose_name='举报人')
    to_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='被举报人')
    report_type = models.PositiveSmallIntegerField(verbose_name='举报类型', choices=ReportManager.Report_Type_Choice,
                                                   default=1)
    detail = models.CharField(verbose_name='正文', max_length=1000)
    images = models.CharField(verbose_name='图片证据', max_length=1000, blank=True, default='[]')
    deal_status = models.PositiveIntegerField(verbose_name='状态', choices=DEAL_STATUS_CHOICE, default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = ReportManager()

    class Meta:
        db_table = 'lv_reports'
        ordering = ['-create_at']


mm_FeedBack = FeedBack.objects
mm_Report = Report.objects
