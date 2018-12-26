from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.notices.models import mm_Notice, NoticeStatus
from datamodels.notices.serializers import NoticeSerializer
from lib.tools import Tool


class NoticeListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NoticeSerializer

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Notice.unread_notices(customer_id)


class SetNoticeStatusView(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Notice.unread_notices(customer_id)

    def update(self, request, *args, **kwargs):
        notice = self.get_object()
        notice.status = NoticeStatus.STATUS_READ
        notice.save()
        return Response(Tool.format_data())
