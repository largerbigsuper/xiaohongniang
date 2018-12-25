from django.db import models
from django.db.models import F

from datamodels.role.models import Customer
from lib.common import BaseManger


class MomentsManager(BaseManger):

    def get_customer_moments(self, customer_list=None):
        if customer_list is None:
            return []
        else:
            return self.filter(customer_id__in=customer_list).select_related('customer').order_by('-create_at')


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


mm_Moments = Moments.objects
mm_Comments = Comments.objects
mm_Likes = Likes.objects
