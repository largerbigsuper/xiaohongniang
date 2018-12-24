from django.db import transaction, IntegrityError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.moments.models import mm_Moments, mm_Comments, mm_Likes
from datamodels.moments.serializers import MomentsSerializer, MomentsDetailSerializer, CommentSerializer, \
    CommentListSerializer, LikeListSerialzier, LikeCreateSerializer
from lib.exceptions import DBException
from lib.tools import Tool
from lib import messages


class MomentsListView(generics.ListCreateAPIView):
    """
    创建动态
    动态列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsSerializer

    def get_queryset(self):
        return self.request.user.customer.moments.prefetch_related('comment').all()

    def create(self, request, *args, **kwargs):
        Tool.param_is_json(request, 'images')
        data = request.data.dict()
        data['customer'] = request.user.customer
        moment = mm_Moments.model(**data)
        moment.save()
        serializer = self.serializer_class(moment)
        return Response(Tool.format_data(serializer.data))


class MomentModifyView(generics.RetrieveUpdateDestroyAPIView):
    """
    获取一条动态
    修改一条动态
    删除一条动态
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsSerializer

    def get_queryset(self):
        return self.request.user.customer.moments.all()


class CustomerMomentsListView(generics.ListAPIView):
    """
    获取其他人的动态列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsSerializer

    def get_queryset(self):
        return mm_Moments.filter(customer_id=self.kwargs['pk']).all()


class MomentsDetailView(generics.RetrieveAPIView):
    """
    获取其他人一条动态详情
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsDetailSerializer
    queryset = mm_Moments.all()


class FollowingMonmentsListView(generics.ListAPIView):
    """
    获取我的关注的人动态列表
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsDetailSerializer

    def get_queryset(self):
        return mm_Moments.get_customer_moments(self.request.user.customer.get_following_ids())


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
        return mm_Comments.filter(moment_id=self.kwargs['pk']).select_related('from_customer', 'to_customer').order_by('create_at')

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
            return Response(Tool.format_data(msg=messages.ADD_COMMENT_OK))


class ReplyOrDeleteCommentView(generics.DestroyAPIView, generics.CreateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'POST':
            return mm_Comments.valid()
        else:
            return mm_Comments.filter(from_customer_id=self.request.session['customer_id'])

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
            serializer = LikeCreateSerializer(like)
            return Response(Tool.format_data(serializer.data, msg=messages.ADD_LIKE_OK))

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            like = self.get_object()
            like.moment.modify_like_total(-1)
            like.delete()
            return Response(Tool.format_data(msg=messages.DELETE_LIKE_OK))
