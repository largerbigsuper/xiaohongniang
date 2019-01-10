from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from datamodels.bottles.models import mm_Bottles, mm_BottlePickerRelation
from datamodels.bottles.serializers import CreateBottleSerializer, NormalBottleSerializer
from lib import messages
from lib.tools import Tool


class MyBottleView(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBottleSerializer

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Bottles.my_bottles(customer_id)

    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        data['customer_id'] = request.session['customer_id']
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(Tool.format_data(serializer.data, msg=messages.ADD_OK))


class BottleDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Bottles.my_bottles(customer_id)


class PickOneBottleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        bottle = mm_Bottles.optional_bottles(request.session['customer_id']).first()
        if bottle:
            mm_BottlePickerRelation.create(bottle=bottle, customer=request.user.customer)
            serializer = NormalBottleSerializer(bottle, context={'request': request})
            return Response(Tool.format_data(serializer.data))
        else:
            return Response(data={'detail': messages.NO_DATA}, status=status.HTTP_400_BAD_REQUEST)


class PickedBottlesView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NormalBottleSerializer

    def get_queryset(self):
        customer_id = self.request.session['customer_id']
        return mm_Bottles.my_picked_bottles(customer_id)


class DeletePickedBolltleView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return mm_Bottles.my_picked_bottles(self.request.session['customer_id'])

    def destroy(self, request, *args, **kwargs):
        bottle = self.get_object()
        mm_BottlePickerRelation.filter(bottle_id=bottle.id, customer_id=request.session['customer_id']).delete()
        return Response(Tool.format_data())

