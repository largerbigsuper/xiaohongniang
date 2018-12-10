import traceback

from django.contrib.auth.models import User
from django.db import models, transaction, IntegrityError

from datamodels.sms.models import mm_SMSCode
from lib.common import BaseManger
from lib.exceptions import DBException
from lib.im import IMServe


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
    avatar_url = models.CharField('头像', max_length=120, blank=True)
    account = models.CharField('电话', max_length=11, unique=True)
    wechat_id = models.CharField('微信号', max_length=24, blank=True)
    intro = models.CharField('自我简介', max_length=120, blank=True)
    address_home = models.CharField('家庭住址', max_length=100, blank=True)
    address_company = models.CharField('公司地址', max_length=100, blank=True)
    im_token = models.CharField('融云token', max_length=100, blank=True)

    class Meta:
        abstract = True


class CustomerManager(BaseManger):

    def add(self, account, password):
        try:
            with transaction.atomic():
                user = self._add_user(account, password)
                im_token = IMServe.gen_token(user.id, account)['token']
                customer = self.create(user=user, account=account, im_token=im_token)
                return customer
        except IntegrityError:
            raise DBException('账号已注册')
        except:
            msg = traceback.format_exc()
            raise DBException(msg)

    def reset_password_by_login(self, user_id, raw_password, new_password):
            user = User.objects.get(id=user_id)
            if user.check_password(raw_password):
                return self._reset_password(user, new_password)
            else:
                raise DBException('原始密码错误')

    def reset_password_by_sms(self, account, password, code):
        try:
            mm_SMSCode.is_effective(account, code)
            user = User.objects.get(username=account)
            return self._reset_password(user, password)
        except User.DoesNotExist:
            raise DBException('%s账号不存在' % account)

    @staticmethod
    def _reset_password(user: User, password: str) -> User:
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def _add_user(account, password):
        user = User.objects.create_user(username=account, password=password)
        return user


class Customer(BaseRole):
    objects = CustomerManager()

    class Meta:
        db_table = 'lv_customers'


mm_Customer = Customer.objects
