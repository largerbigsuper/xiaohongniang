from django.db import models

from lib.common import BaseManger


class SMSCodeManager(BaseManger):
    pass


class SMSCode(models.Model):
    tel = models.CharField(max_length=11)
    expire_at = models.DateTimeField()

    objects = SMSCodeManager()

    class Meta:
        db_table = 'lv_sms_code'
        index_together = [
            ('tel', 'expire_at')
        ]


mm_SMSCode = SMSCode.objects
