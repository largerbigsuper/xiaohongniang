from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.notices.models import mm_Notice, NoticeStatus
from datamodels.notices.serializers import NoticeSerializer
from lib.tools import Tool


class NoticeListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NoticeSerializer

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Notice.all_notices(customer_id).order_by('status', '-create_at')

    def paginate_queryset(self, queryset):
        # 拉去消息列表后，将未读状态设置为已读状态
        q = super().paginate_queryset(queryset)
        notice_ids = [notice.id for notice in q]
        mm_Notice.filter(pk__in=notice_ids).update(status=NoticeStatus.STATUS_READ)
        return q


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


class UnreadNoticeAmountView(APIView):

    def _get_unread_count(self):
        return mm_Notice.unread_notices(self.request.session['customer_id']).count()

    def get(self, request):
        data = {
            'unread_count': self._get_unread_count()
        }
        return Response(Tool.format_data(data))
