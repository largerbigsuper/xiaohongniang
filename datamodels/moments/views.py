import re

from django.db import transaction, IntegrityError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.moments.models import mm_Moments, mm_Comments, mm_Likes, mm_Topic
from datamodels.moments.serializers import CommentSerializer, \
    CommentListSerializer, LikeListSerialzier, LikeCreateSerializer, NormalMomentsDetailSerializer, \
    MomentsCreateSerializer, TopicSerializer
from datamodels.notices.models import mm_Notice, Action
from datamodels.stats.models import mm_CustomerPoint
from lib.exceptions import DBException
from lib.im import IMServe
from lib.tools import Tool
from lib import messages


class MomentsListView(generics.ListCreateAPIView):
    """
    创建动态
    动态列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsCreateSerializer

    def get_queryset(self):
        return self.request.user.customer.moments.prefetch_related('topic').all()

    def paginate_queryset(self, queryset):
        customer_id = self.request.session['customer_id']
        q = super().paginate_queryset(queryset)
        moment_ids = [moment.id for moment in q]
        likes = mm_Likes.filter(moment_id__in=moment_ids, customer_id=customer_id).values_list('moment_id', flat=True)
        for moment in q:
            moment.is_like = moment.id in likes
        return q

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        topics_str = data.pop('topics', '')
        topic_list = []
        if topics_str:
            topic_tags = re.findall(r'#.*?#', topics_str)
            for tag in topic_tags:
                name = tag.replace('#', '')
                topic = mm_Topic.get_toptics(name, request.user.customer.id, request.user.id)
                topic_list.append(topic)
            data['topic'] = topic_list
        data['customer_id'] = request.user.customer.id
        serializer = MomentsCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        moment = serializer.save()
        mm_CustomerPoint.add_action(request.session['customer_id'], mm_CustomerPoint.Action_Add_Moment)
        for t in topic_list:
            moment.topic.add(t)
        return Response(Tool.format_data(serializer.data))


class MomentModifyView(generics.RetrieveUpdateDestroyAPIView):
    """
    获取一条动态
    修改一条动态
    删除一条动态
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsCreateSerializer

    def get_queryset(self):
        return self.request.user.customer.moments.all()


class CustomerMomentsListView(generics.ListAPIView):
    """
    获取其他人的动态列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NormalMomentsDetailSerializer

    def get_queryset(self):
        return mm_Moments.filter(customer_id=self.kwargs['pk']).all().prefetch_related('topic')

    def paginate_queryset(self, queryset):
        customer_id = self.request.session['customer_id']
        q = super().paginate_queryset(queryset)
        moment_ids = [moment.id for moment in q]
        likes = mm_Likes.filter(moment_id__in=moment_ids, customer_id=customer_id).values_list('moment_id', flat=True)
        for moment in q:
            moment.is_like = moment.id in likes
        return q



class MomentsDetailView(generics.RetrieveAPIView):
    """
    获取其他人一条动态详情
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NormalMomentsDetailSerializer
    queryset = mm_Moments.all().prefetch_related('topic')

    def get_object(self):
        obj = super().get_object()
        customer_id = self.request.session['customer_id']
        obj.is_like = mm_Likes.filter(moment_id=obj.id, customer_id=customer_id).exists()
        return obj


class FollowingMomentsListView(generics.ListAPIView):
    """
    获取我的关注的人动态列表
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = NormalMomentsDetailSerializer

    def get_queryset(self):
        return mm_Moments.get_customer_moments(self.request.user.customer.get_following_ids())

    def paginate_queryset(self, queryset):
        customer_id = self.request.session['customer_id']
        q = super().paginate_queryset(queryset)
        moment_ids = [moment.id for moment in q]
        likes = mm_Likes.filter(moment_id__in=moment_ids, customer_id=customer_id).values_list('moment_id', flat=True)
        for moment in q:
            moment.is_like = moment.id in likes
        return q


class LatestMomentsListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NormalMomentsDetailSerializer

    def get_queryset(self):
        return mm_Moments.latest_moments()

    def paginate_queryset(self, queryset):
        customer_id = self.request.session['customer_id']
        q = super().paginate_queryset(queryset)
        moment_ids = [moment.id for moment in q]
        likes = mm_Likes.filter(moment_id__in=moment_ids, customer_id=customer_id).values_list('moment_id', flat=True)
        for moment in q:
            moment.is_like = moment.id in likes
        return q


class MomentSearchView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NormalMomentsDetailSerializer

    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id', 0)
        return mm_Moments.filter(topic__id=topic_id).order_by('-create_at')

    def paginate_queryset(self, queryset):
        customer_id = self.request.session['customer_id']
        q = super().paginate_queryset(queryset)
        moment_ids = [moment.id for moment in q]
        likes = mm_Likes.filter(moment_id__in=moment_ids, customer_id=customer_id).values_list('moment_id', flat=True)
        for moment in q:
            moment.is_like = moment.id in likes
        return q


"""
评论相关
"""


class CommentView(generics.ListCreateAPIView):
    """
    评论
    某条动态评论列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentListSerializer

    def get_queryset(self):
        return mm_Comments.valid().filter(moment_id=self.kwargs['pk']).select_related('from_customer',
                                                                                      'to_customer').order_by(
            '-create_at')

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['moment_id'] = kwargs['pk']
        data['from_customer_id'] = request.session['customer_id']
        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                comment = serializer.save()
                comment.moment.comment.add(comment)
                comment.moment.modify_comment_total()
                mm_Notice.add_notice(comment.moment, comment, Action.ACTION_TYPE_ADD_COMMENT)
                mm_CustomerPoint.add_action(request.session['customer_id'], mm_CustomerPoint.Action_Add_Comment)
            return Response(Tool.format_data(msg=messages.ADD_COMMENT_OK))


class ReplyOrDeleteCommentView(generics.DestroyAPIView, generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'POST':
            return mm_Comments.valid()
        else:
            return mm_Comments.valid().filter(from_customer_id=self.request.session['customer_id'])

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            comment = self.get_object()
            comment.is_del = True
            comment.save()
            comment.moment.modify_comment_total(-1)
        return Response(Tool.format_data(msg=messages.DELETE_COMMENT_OK))

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        comment = self.get_object()
        data['moment_id'] = comment.moment_id
        data['from_customer_id'] = request.session['customer_id']
        data['to_customer_id'] = comment.from_customer_id
        if comment.from_customer_id == data['from_customer_id']:# 自己回复自己当做新评论
            data['reply_to_id'] = None
        else:
            data['reply_to_id'] = kwargs['pk']

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                comment = serializer.save()
                comment.moment.comment.add(comment)
                comment.moment.modify_comment_total()
                mm_Notice.add_notice(comment.moment, comment, Action.ACTION_TYPE_ADD_REPLY)
            return Response(Tool.format_data(msg=messages.REPLY_COMMENT_OK))

"""
点赞相关
"""


class LikesView(generics.CreateAPIView, generics.DestroyAPIView, generics.ListAPIView):
    """
    点赞, 取消点赞， 点赞列表
    """
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikeListSerialzier
        else:
            return LikeCreateSerializer

    def get_queryset(self):
        return mm_Likes.filter(moment_id=self.kwargs['pk']).select_related('customer').order_by('-create_at')

    def get_object(self):
        try:
            like = mm_Likes.get(moment_id=self.kwargs['pk'], customer_id=self.request.session['customer_id'])
            return like
        except mm_Likes.model.DoesNotExist:
            raise DBException('记录不存在')
        except:
            raise

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            like, created = mm_Likes.get_or_create(customer_id=request.session['customer_id'], moment_id=kwargs['pk'])
            if created:
                like.moment.modify_like_total()
                mm_Notice.add_notice(like.moment, like, Action.ACTION_TYPE_ADD_LIKE)
                mm_CustomerPoint.add_action(request.session['customer_id'], mm_CustomerPoint.Action_Add_Like)
            serializer = LikeCreateSerializer(like)
            return Response(Tool.format_data(serializer.data, msg=messages.ADD_LIKE_OK))

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            like = self.get_object()
            like.moment.modify_like_total(-1)
            like.delete()
            return Response(Tool.format_data(msg=messages.DELETE_LIKE_OK))


"""
话题相关
"""


class TopicListView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer
    queryset = mm_Topic.all()

    def post(self, request, *args, **kwargs):
        topic = mm_Topic.get_toptics(request.data.get('name'), request.session['customer_id'], request.user.id, request.data.get('logo_url'))
        serializer = self.serializer_class(topic)
        return Response(Tool.format_data(serializer.data))


class TopicView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer
    queryset = mm_Topic.all()

    def delete(self, request, *args, **kwargs):
        topic = self.get_object()
        IMServe.destory_group(topic.customer.user.id, topic.id)
        return super().delete(request, *args, **kwargs)


class TopicChatGroupView(generics.RetrieveDestroyAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer
    queryset = mm_Topic.all()

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        IMServe.join_group(request.user.id, obj.id, obj.name)
        return Response(Tool.format_data(msg=messages.JOIN_GROUP_OK))

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        IMServe.leave_group(request.user.id, obj.id)
        return Response(Tool.format_data(msg=messages.LEAVE_GROUP_OK))
