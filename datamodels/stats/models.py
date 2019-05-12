import json
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from datamodels.moments.models import mm_Likes, mm_Comments
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

    def my_new_visitors_count(self, customer_id):
        return self.my_visitors(customer_id).filter(read_status=False).count()

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
    from_customer = models.ForeignKey('role.Customer', verbose_name='发起人', on_delete=models.CASCADE, db_index=False, related_name='records')
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


class CustomerPointManager(BaseManger):
    In = 1
    Out = 0
    In_Or_Out = (
        (Out, '减少'),
        (In, '增加'),
    )

    Action_Withdraw = 0
    Action_Login = 1
    Action_Add_Like = 2
    Action_Add_Comment = 3
    Action_Add_Moment = 4
    Action_Add_Bottle = 5
    Action_Pick_Bottle = 6
    Action_Invite_Enroll = 7
    Action_Talk = 8

    Action_Choice = (
        (Action_Withdraw, '兑换'),
        (Action_Login, '登录'),
        (Action_Add_Like, '点赞动态'),
        (Action_Add_Comment, '添加评论'),
        (Action_Add_Moment, '发动态'),
        (Action_Add_Bottle, '发漂流瓶'),
        (Action_Pick_Bottle, '捡漂流瓶'),
        (Action_Invite_Enroll, '邀请注册'),
        (Action_Talk, '聊天'),
    )

    Action_Point_Mapping = {
        Action_Login: 1,
        Action_Add_Like: 2,
        Action_Add_Comment: 2,
        Action_Add_Moment: 1,
        Action_Add_Bottle: 1,
        Action_Pick_Bottle: 0,
        Action_Invite_Enroll: 10,
        Action_Talk: 1
    }

    Action_Desc = {action: msg for action, msg in Action_Choice}

    # 每天积分行为限制
    Action_Per_Day_Limit_Setting = {
        Action_Login: 1,
        Action_Add_Like: 1,
        Action_Add_Comment: 1,
        Action_Add_Moment: 1,
        Action_Add_Bottle: 2,
        Action_Pick_Bottle: 0,
        Action_Invite_Enroll: 10000,
        Action_Talk: 2
    }
    # 积分最低行为次数标准
    Action_Per_Day_Base_Count = {
        Action_Add_Like: 5,
        Action_Add_Comment: 5
    }

    def get_total_point(self, customer_id):
        record = self.filter(customer_id=customer_id).first()
        if record:
            return record.total_left
        else:
            return 0

    def is_limited(self, customer_id, action):
        if action == self.Action_Add_Like:
            count_limited = mm_Likes.filter(customer_id=customer_id,
                                            create_at__date=datetime.now().date()
                                            ).count() < self.Action_Per_Day_Base_Count[action]
            if count_limited:
                return True
        if action == self.Action_Add_Comment:
            count_limited = mm_Comments.filter(from_customer=customer_id,
                                               create_at__date=datetime.now().date()
                                               ).count() < self.Action_Per_Day_Base_Count[action]
            if count_limited:
                return True

        if action == self.Action_Withdraw:
            return False
        else:
            action_count_today = self.filter(customer_id=customer_id,
                                             create_at__date=datetime.now().date(),
                                             action=action
                                             ).count()
            return action_count_today >= self.Action_Per_Day_Limit_Setting[action]

    def _add_action(self, customer_id, action, amount, total_left, operator_id=None):
        """
        积分记录
        :param customer_id: 用户id
        :param amount: 操作总量
        :param action: 行为
        :param operator_id: 操作人auth_user.id
        :return:
        """
        in_or_out = self.In
        if action == self.Action_Withdraw:
            in_or_out = self.Out
        if not self.is_limited(customer_id, action):
            self.create(customer_id=customer_id,
                        in_or_out=in_or_out,
                        amount=amount,
                        total_left=total_left,
                        action=action,
                        desc=self.Action_Desc[action],
                        operator_id=operator_id,
                        )

    def add_action(self, customer_id, action):
        """
        增加积分记录
        :param customer_id:
        :param action:
        :return:
        """
        amount = self.Action_Point_Mapping[action]
        total_left = self.get_total_point(customer_id) + amount
        self._add_action(customer_id=customer_id,
                         action=action,
                         amount=amount,
                         total_left=total_left,
                         )

    def withdraw(self, customer_id, operator_id, amount):
        """兑换积分"""
        total_left = self.get_total_point(customer_id) - amount
        if total_left < 0:
            data = {'detail': '积分数量不足'}
            return data
        self._add_action(customer_id=customer_id,
                         action=self.Action_Withdraw,
                         amount=amount,
                         total_left=total_left,
                         operator_id=operator_id
                         )
        return


class CustomerPoint(models.Model):

    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='用户')
    in_or_out = models.PositiveSmallIntegerField(verbose_name='增加/减少',
                                                 choices=CustomerPointManager.In_Or_Out,
                                                 default=CustomerPointManager.In)
    amount = models.PositiveSmallIntegerField(verbose_name='数量', default=0)
    total_left = models.PositiveIntegerField(verbose_name='剩余数量', default=0)
    action = models.PositiveSmallIntegerField(verbose_name='原因', default=0, choices=CustomerPointManager.Action_Choice)
    desc = models.CharField(verbose_name='描述', max_length=48)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='操作人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = CustomerPointManager()

    class Meta:
        db_table = 'lv_customer_points'
        ordering = ['-create_at']


class MessageTemplateManager(BaseManger):

    def my_templates(self, customer_id):
        return self.filter(customer_id=customer_id).order_by('-id')


class MessageTemplate(models.Model):

    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='用户')
    text = models.CharField(verbose_name='内容', max_length=200)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = MessageTemplateManager()

    class Meta:
        db_table = 'lv_message_template'
        verbose_name = verbose_name_plural = '打招呼模板'


class CustomerBonusRecordManager(BaseManger):

    In = 1
    Out = 0
    In_Or_Out = (
        (Out, '减少'),
        (In, '增加'),
    )

    Action_Enroll = 0
    Action_Buy = 1
    Action_Withdraw = 2

    Action_Choice = (
        (Action_Enroll, '邀请注册'),
        (Action_Buy, '被邀请人购买服务'),
        (Action_Withdraw, '提现'),
    )

    template_enroll = '邀请好友{}注册'
    template_buy = '被邀请人{}购买{}'
    template_withdraw = '发起提现请求'

    Award_Mapping = {
        Action_Enroll: 5,
        Action_Buy: 5,
    }

    def add_record(self, customer_id, from_customer_id, action, amount, desc, operator_id=None):
        if action == self.Action_Withdraw:
            in_or_out = self.Out
        else:
            in_or_out = self.In

        total_left = self.get_total_point(customer_id)

        if in_or_out == self.In:
            total_left += amount
        else:
            total_left -= amount

        return self.create(customer_id=customer_id,
                           from_customer_id=from_customer_id,
                           in_or_out=in_or_out,
                           amount=amount,
                           total_left=total_left,
                           action=action,
                           desc=desc,
                           operator_id=operator_id
                           )

    def get_buy_customer_count(self, customer_id):
        return self.filter(customer_id=customer_id,
                           action=self.Action_Buy).values_list('from_customer_id', flat=True).distinct().count()

    def get_total_point(self, customer_id):
        record = self.filter(customer_id=customer_id).first()
        if record:
            return record.total_left
        else:
            return 0


class CustomerBonusRecord(models.Model):

    customer = models.ForeignKey('role.Customer', on_delete=models.CASCADE, verbose_name='用户')
    from_customer = models.ForeignKey('role.Customer',
                                      on_delete=models.CASCADE,
                                      related_name='invited_customers',
                                      verbose_name='被邀请人')
    in_or_out = models.PositiveSmallIntegerField(verbose_name='增加/减少',
                                                 choices=CustomerBonusRecordManager.In_Or_Out,
                                                 default=CustomerBonusRecordManager.In)
    amount = models.PositiveSmallIntegerField(verbose_name='数量', default=0)
    total_left = models.PositiveIntegerField(verbose_name='剩余数量', default=0)
    action = models.PositiveSmallIntegerField(verbose_name='原因', default=CustomerBonusRecordManager.Action_Enroll,
                                              choices=CustomerBonusRecordManager.Action_Choice)
    desc = models.CharField(verbose_name='描述', max_length=48)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='操作人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')

    objects = CustomerBonusRecordManager()

    class Meta:
        db_table = 'lv_customer_bonus_records'
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '奖励记录管理'


class WithDrawRecordManager(BaseManger):
    Status_Submited = 0
    Status_Done = 1
    Status_Refused = 2

    Status_Choice = (
        (Status_Submited, '已提交'),
        (Status_Done, '已提现'),
        (Status_Refused, '拒绝提现'),
    )


class WithDrawRecord(models.Model):

    customer = models.ForeignKey('role.Customer', verbose_name='申请人', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(verbose_name='申请状态',
                                              choices=WithDrawRecordManager.Status_Choice,
                                              default=WithDrawRecordManager.Status_Submited)
    amount = models.PositiveIntegerField(verbose_name='数量', default=0)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name='处理人')
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    alipay_account = models.CharField(verbose_name='支付宝账号', max_length=20)

    objects = WithDrawRecordManager()

    class Meta:
        db_table = 'lv_withdraw_records'
        ordering = ['-create_at']
        verbose_name = verbose_name_plural = '提现申请管理'


class CustomerChatRecordManager(BaseManger):

    def add_record(self, customer_id, user_id):
        record, _ = self.get_or_create(customer_id=customer_id)
        record_list = json.loads(record.record_list)
        if customer_id not in record_list:
            record_list.append(user_id)
        record.record_list = json.dumps(record_list)
        record.save()

    def get_record_list(self, customer_id):
        record = self.filter(customer_id=customer_id).first()
        if record:
            return json.loads(record.record_list)
        else:
            return []


class CustomerChatRecord(models.Model):
    
    customer = models.OneToOneField('role.Customer', on_delete=models.CASCADE, verbose_name='用户')
    record_list = models.TextField(default='[]', verbose_name='记录')
    
    objects = CustomerChatRecordManager()
    
    class Meta:
        db_table = 'lv_customer_chat_record'
        verbose_name = verbose_name_plural = '聊天记录表'


mm_OperationRecord = OperationRecord.objects
mm_CustomerPoint = CustomerPoint.objects
mm_MessageTemplate = MessageTemplate.objects
mm_CustomerBonusRecord = CustomerBonusRecord.objects
mm_WithDrawRecord = WithDrawRecord.objects
mm_CustomerChatRecord = CustomerChatRecord.objects
