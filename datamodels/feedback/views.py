from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.feedback.models import mm_Report
from datamodels.feedback.serializers import FeedBackSerializer, ReportSerializer, ReportListSerializer
from lib import messages
from lib.tools import Tool


class AddFeedBackView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FeedBackSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['customer_id'] = request.session['customer_id']
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(Tool.format_data(serializer.data, msg=messages.ADD_FEEDBACK_OK))


class AddReportView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReportSerializer
        else:
            return ReportListSerializer

    queryset = mm_Report.all()

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['customer_id'] = request.session['customer_id']
        serializer = self.get_serializer_class()(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(Tool.format_data(serializer.data, msg=messages.ADD_OK))
