from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.stats.models import mm_OperationRecord
from datamodels.stats.serializers import OpreationRecordListSerilizer
from lib.tools import Tool


class OpreationRecordListView(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = OpreationRecordListSerilizer

    def get_queryset(self):
        return mm_OperationRecord.my_visitors(self.request.session['customer_id'])

    def paginate_queryset(self, queryset):
        # 拉去消息列表后，将未读状态设置为已读状态
        q = super().paginate_queryset(queryset)
        record_ids = [record.id for record in q]
        mm_OperationRecord.filter(pk__in=record_ids).update(read_status=True)
        return q


class UnreadTotalOpreationRecordView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            'total': mm_OperationRecord.my_visitors(self.request.session['customer_id']).filter(read_status=False).count()
        }
        return Response(Tool.format_data(data))
