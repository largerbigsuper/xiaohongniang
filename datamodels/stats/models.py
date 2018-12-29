from datetime import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from datamodels.role.models import Customer
from lib.common import BaseManger


class OperationType:
    LOOK_UP_PROFILE = 1


Operation_Type_Choice = (
    (OperationType.LOOK_UP_PROFILE, '访问主页'),
)


class OperationRecordManager(BaseManger):

    def my_visitors(self, customer_id):
        return self.filter(object_id=customer_id).order_by('-create_at')

    def add_opreation_record(self, from_customer_id, content_object, operation_type=1):
        content_type = ContentType.objects.get_for_model(content_object)
        record, created = self.update_or_create(operation_type=operation_type,
                                                from_customer_id=from_customer_id,
                                                content_type=content_type,
                                                object_id=content_object.id,
                                                create_at__date=datetime.now().date(),
                                                defaults={'create_at': datetime.now()})
        return record


class OperationRecord(models.Model):
    operation_type = models.PositiveIntegerField(verbose_name='类型', choices=Operation_Type_Choice, default=1)
    from_customer = models.ForeignKey(Customer, verbose_name='发起人', on_delete=models.CASCADE, db_index=False, related_name='records')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    create_at = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(verbose_name='读取状态', default=False)

    objects = OperationRecordManager()

    class Meta:
        db_table = 'lv_opreation_records'
        index_together = [
            ('operation_type', 'from_customer', 'content_type', 'object_id')
        ]


mm_OperationRecord = OperationRecord.objects
