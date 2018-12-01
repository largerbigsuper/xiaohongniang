from datetime import datetime, timedelta

from django.db import models

from lib.common import BaseManger
from lib.exceptions import LVException


class SMSCodeManager(BaseManger):

    def add(self, tel, code):
        expire_at = datetime.now() + timedelta(minutes=5)
        return self.create(tel=tel, code=code, expire_at=expire_at)

    def can_get_new_code(self, tel):
        return not self.filter(tel=tel, expire_at__gt=datetime.now()).exists()

    def is_effective(self, tel, code):
        try:
            record = self.get(tel=tel, code=code)
            if record.expire_at < datetime.now():
                raise LVException(code=1, msg='验证码已失效')
        except self.model.DoesNotExist:
            raise LVException(code=1, msg='验证码不存在')


class SMSCode(models.Model):
    tel = models.CharField(max_length=11)
    code = models.CharField(max_length=4)
    expire_at = models.DateTimeField()

    objects = SMSCodeManager()

    class Meta:
        db_table = 'lv_sms_code'
        index_together = [
            ('tel', 'code', 'expire_at')
        ]


mm_SMSCode = SMSCode.objects
