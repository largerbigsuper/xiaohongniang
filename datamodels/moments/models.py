from django.db import models
from django.db.models import F

from datamodels.role.models import Customer
from lib.common import BaseManger
from lib.im import IMServe


class MomentsManager(BaseManger):

    def get_customer_moments(self, customer_list=None):
        if customer_list is None:
            return []
        else:
            return self.filter(customer_id__in=customer_list).select_related('customer').prefetch_related('topic').order_by('-create_at')

    def latest_moments(self):
        return self.all().select_related('customer').prefetch_related('topic').order_by('-create_at')


class FunctionType:
    FUNCTION_TYPE_NORMAL = 1
    FUNCTION_TYPE_ADS = 2
    FUNCTION_TYPE_NOTICES = 2


FUNCTION_TYPE_CHOICE = (
    (1, '动态'),
    (2, '广告'),
    (3, '通知'),
)


class Moments(models.Model):
    customer = models.ForeignKey(Customer, related_name='moments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='正文', max_length=1500, null=True, blank=True)
    images = models.CharField(verbose_name='图片', max_length=1000, default='[]', blank=True)
    latitude = models.FloatField(verbose_name='精度', null=True, blank=True)
    longitude = models.FloatField(verbose_name='维度', null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_at = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    comment = models.ManyToManyField('moments.Comments', db_table='lv_moment_comment')
    comment_total = models.PositiveIntegerField(verbose_name='评论总数', default=0)
    like = models.ManyToManyField('moments.Likes', db_table='lv_comment_like')
    like_total = models.PositiveIntegerField(verbose_name='点赞总数', default=0)
    is_hidden_name = models.BooleanField(verbose_name='匿名', default=False)
    address = models.CharField(verbose_name='地址', blank=True, max_length=200)
    function_type = models.PositiveIntegerField(verbose_name='功能', choices=FUNCTION_TYPE_CHOICE, default=1)
    topic = models.ManyToManyField('moments.Topic', db_table='lv_moments_topics', related_name='moments')

    objects = MomentsManager()

    class Meta:
        db_table = 'lv_moments'
        index_together = [
            ('latitude', 'longitude')
        ]
        ordering = ['-create_at']

    def limited_comment(self):
        return self.comment.all()[:3]

    def modify_comment_total(self, step=1):
        self.comment_total = F('comment_total') + step
        self.save()

    def modify_like_total(self, step=1):
        self.like_total = F('like_total') + step
        self.save()


class CommentsManager(BaseManger):

    def valid(self):
        return self.filter(is_del=False)


class Comments(models.Model):
    from_customer = models.ForeignKey(Customer, related_name='comments', on_delete=models.CASCADE, db_index=False)
    to_customer = models.ForeignKey(Customer, related_name='reply', null=True, blank=True, on_delete=models.CASCADE, db_index=False)
    moment = models.ForeignKey(Moments, related_name='comments', on_delete=models.CASCADE, db_index=False)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, db_index=False)
    text = models.CharField(verbose_name='评论正文', max_length=200, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    is_del = models.BooleanField(verbose_name='删除', default=False)

    objects = CommentsManager()

    class Meta:
        db_table = 'lv_comments'
        index_together = [
            ('from_customer', 'moment', 'reply_to', 'to_customer')
        ]
        ordering = ['-create_at']


class LikesManager(BaseManger):
    pass


class Likes(models.Model):
    customer = models.ForeignKey(Customer, related_name='likes', on_delete=models.CASCADE, db_index=False)
    moment = models.ForeignKey(Moments, related_name='likes', on_delete=models.CASCADE, db_index=False)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = LikesManager()

    class Meta:
        db_table = 'lv_likes'
        unique_together = [
            ('customer', 'moment')
        ]
        index_together = [
            ('customer', 'moment')
        ]
        ordering = ['-create_at']


class TopicManager(BaseManger):

    def get_toptics(self, name, customer_id, user_id, logo_url=None):
        topic, created = self.get_or_create(name=name, defaults={'customer_id': customer_id, 'logo_url': logo_url})
        if created:
            group_id = topic.id
            IMServe.create_group(user_id, group_id=group_id, group_name=name)
        return topic


class Topic(models.Model):
    name = models.CharField(verbose_name='话题', max_length=20, db_index=True, unique=True)
    customer = models.ForeignKey(Customer, verbose_name='发起人', null=True, blank=True, on_delete=models.DO_NOTHING)
    logo_url = models.CharField('背景图', max_length=120, blank=True, null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    objects = TopicManager()

    class Meta:
        db_table = 'lv_topics'


mm_Moments = Moments.objects
mm_Comments = Comments.objects
mm_Likes = Likes.objects
mm_Topic = Topic.objects
