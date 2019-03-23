from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from datamodels.moments.models import Comments, Likes, Moments
from datamodels.role.models import Customer
from lib.common import BaseManger


class Action:
    ACTION_TYPE_ADD_LIKE = 1
    ACTION_TYPE_ADD_COMMENT = 2
    ACTION_TYPE_ADD_REPLY = 3


ACTION_CHOICE = (
    (Action.ACTION_TYPE_ADD_LIKE, '点赞'),
    (Action.ACTION_TYPE_ADD_COMMENT, '评论'),
    (Action.ACTION_TYPE_ADD_REPLY, '回复'),
)

ACTION_TYPE_TO_RESULT = {
    Action.ACTION_TYPE_ADD_LIKE: '动态',
    Action.ACTION_TYPE_ADD_COMMENT: '动态',
    Action.ACTION_TYPE_ADD_REPLY: '评论',
}


class NoticeStatus:
    STATUS_UNREAD = 0
    STATUS_READ = 1


STATUS_CHOICE = (
    (NoticeStatus.STATUS_UNREAD, '未读'),
    (NoticeStatus.STATUS_READ, '已读'),
)


class NoticeManager(BaseManger):

    def all_notices(self, custmoer_id, status=None):
        f = {
            'to_customer_id': custmoer_id
        }
        if status is not None:
            f['status'] = status
        return self.filter(**f).select_related('from_customer')

    def unread_notices(self, custmoer_id, status=NoticeStatus.STATUS_UNREAD):
        return self.all_notices(custmoer_id, status=status)

    def add_notice(self, content_object, content_result, action_type=1):
        """
        点赞，评论消息
        :param content_object: 点赞，评论对象
        :param content_result: 结果对象
        :param action_type: 1：点赞， 2：评论 3：回复评论
        :return:
        """
        notice_list = []
        if action_type == 1:  # 1.点赞
            notice = Notice(action_type=action_type,
                            content_object=content_object,
                            content_result=content_result,
                            from_customer_id=content_result.customer_id,
                            to_customer_id=content_object.customer_id,
                            )
            notice_list.append(notice)

        elif action_type == 2:  # 2.评论
            # 1.普通评论
            notice = Notice(action_type=action_type,
                            content_object=content_object,
                            content_result=content_result,
                            from_customer_id=content_result.from_customer_id,
                            to_customer_id=content_object.customer_id,
                            )
            notice_list.append(notice)

        elif action_type == 3:  # 3.回复评论，通知被回复人
            reply_notice = Notice(action_type=action_type,
                                  content_object=content_object,
                                  content_result=content_result,
                                  from_customer_id=content_result.from_customer_id,
                                  to_customer_id=content_result.to_customer_id,
                                  )
            notice_list.append(reply_notice)
        mm_Notice.bulk_create(notice_list)


class Notice(models.Model):
    # content_type_choice = (
    #     (ContentType.objects.get_for_model(Moments).id, '动态相关'),
    # )
    content_type_choice = []
    # content_type_result_choice = (
    #     (ContentType.objects.get_for_model(Likes).id, '点赞'),
    #     (ContentType.objects.get_for_model(Comments).id, '评论和回复'),
    # )
    content_type_result_choice = []
    action_type = models.PositiveIntegerField(verbose_name='类型', choices=ACTION_CHOICE, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False, related_name='actions',
                                     choices=content_type_choice, default=0)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type_result = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False,
                                            related_name='results', choices=content_type_result_choice,
                                            default=0)
    result_id = models.PositiveIntegerField()
    content_result = GenericForeignKey('content_type_result', 'result_id')
    from_customer = models.ForeignKey(Customer, verbose_name='发起人', on_delete=models.CASCADE, db_index=False, related_name='sender')
    to_customer = models.ForeignKey(Customer, verbose_name='接收人', on_delete=models.CASCADE, db_index=False, related_name='reciver')
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_CHOICE, default=0)

    objects = NoticeManager()

    class Meta:
        db_table = 'lv_notices'
        index_together = [
            ('action_type', 'status', 'content_type', 'to_customer')
        ]
        ordering = ['-create_at']
        verbose_name = '消息管理'
        verbose_name_plural = '消息管理'


class DemandManager(BaseManger):

    Status_Need_Reply = 0
    Status_Accepted = 1
    Status_Refused = 2

    Status_Choice = (
        (Status_Need_Reply, '未回复'),
        (Status_Accepted, '接受'),
        (Status_Refused, '拒绝'),
    )

    Type_Ask_Wechat = 0
    Type_Make_Date_Online = 1
    Type_Make_Date_Offline = 2
    Type_Choice = (
        (Type_Ask_Wechat, '请求微信'),
        (Type_Make_Date_Online, '线上约她'),
        (Type_Make_Date_Offline, '线下约她'),
    )

    def received(self, customer_id, status=None, demand_type=None):
        f = {
            'to_customer_id': customer_id
        }
        if status is not None:
            f['status'] = status
        if demand_type is not None:
            f['demand_type'] = demand_type
        return self.filter(**f).order_by('-id')


class Demand(models.Model):

    demand_type = models.PositiveSmallIntegerField(verbose_name='请求类型',
                                                   choices=DemandManager.Type_Choice,
                                                   default=DemandManager.Type_Ask_Wechat)
    customer = models.ForeignKey('role.Customer', verbose_name='申请人', on_delete=models.CASCADE)
    to_customer = models.ForeignKey('role.Customer', verbose_name='请求对象', on_delete=models.CASCADE,
                                    related_name='exchange_user')
    status = models.PositiveSmallIntegerField(verbose_name='申请状态', choices=DemandManager.Status_Choice,
                                              default=DemandManager.Status_Need_Reply)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = DemandManager()

    class Meta:
        db_table = 'lv_demand'
        verbose_name = verbose_name_plural = '帮我约/微信交换申请'


class WechatCardManager(BaseManger):

    def mycards(self, customer_id):
        return self.filter(customer_id=customer_id).order_by('-id')

    def add_wechat(self, customer_id, accepted_customer_id, accepted_customer_wechat):

        return self.get_or_create(customer_id=customer_id,
                                  accepted_customer_id=accepted_customer_id,
                                  wechat=accepted_customer_wechat)


class WechatCard(models.Model):

    customer = models.ForeignKey('role.Customer', verbose_name='申请人', on_delete=models.CASCADE)
    accepted_customer = models.ForeignKey('role.Customer', related_name='accepted_customers',
                                          on_delete=models.CASCADE, verbose_name='被申请人')
    wechat = models.CharField(max_length=100, verbose_name='微信号')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = WechatCardManager()

    class Meta:
        db_table = 'lv_wechat_card'


mm_Notice = Notice.objects
mm_Demand = Demand.objects
mm_WechatCard = WechatCard.objects
