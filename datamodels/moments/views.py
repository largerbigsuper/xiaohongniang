import json

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.moments.models import mm_Moments
from datamodels.moments.serializers import MomentsSerializer, MomentsDetailSerializer
from lib.tools import Tool


class MomentsListView(generics.ListCreateAPIView):
    """
    创建动态
    动态列表
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MomentsSerializer

    def get_queryset(self):
        return self.request.user.customer.moments.all()

    def create(self, request, *args, **kwargs):
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

