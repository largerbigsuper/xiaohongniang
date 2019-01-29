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
    content_type_choice = (
        (ContentType.objects.get_for_model(Moments).id, '动态相关'),
    )
    content_type_result_choice = (
        (ContentType.objects.get_for_model(Likes).id, '点赞'),
        (ContentType.objects.get_for_model(Comments).id, '评论和回复'),
    )
    action_type = models.PositiveIntegerField(verbose_name='类型', choices=ACTION_CHOICE, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False, related_name='actions',
                                     choices=content_type_choice, default=content_type_choice[0][0])
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type_result = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=False,
                                            related_name='results', choices=content_type_result_choice,
                                            default=content_type_result_choice[0][0])
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


mm_Notice = Notice.objects
