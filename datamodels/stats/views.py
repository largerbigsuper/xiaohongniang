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


class UnreadTotalOpreationRecordView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {
            'total': mm_OperationRecord.my_visitors(self.request.session['customer_id']).count()
        }
        return Response(Tool.format_data(data))
