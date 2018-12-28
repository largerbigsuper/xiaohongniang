from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamodels.feedback.serializers import FeedBackSerializer
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
