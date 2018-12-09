import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from datamodels.role.models import mm_Customer
from datamodels.role.serializers import CustomerSerializer
from datamodels.sms.models import mm_SMSCode
from lib.exceptions import LoginException
from lib.tools import Tool


logger = logging.getLogger(__name__)


class RegisterView(APIView):

    def post(self, request):
        required_params = ['code', 'account', 'password']
        Tool.required_params(request, required_params)
        code = request.data.get('code')
        account = request.data.get('account')
        password = request.data.get('password')
        mm_SMSCode.is_effective(account, code)
        customer = mm_Customer.add(account, password)
        login(request, customer.user)
        data = dict(account=account)
        return Response(Tool.format_data(data), status=status.HTTP_200_OK)


class LoginView(APIView):

    @csrf_exempt
    def post(self, request):
        """登录"""
        required_params = ['account', 'password']
        Tool.required_params(request, required_params)
        username = request.data.get('account')
        password = request.data.get('password')
        try:
            user = authenticate(self.request, username=username, password=password)
            if user:
                login(request, user)
                request.session['user_id'] = user.id
                request.session['customer_id'] = user.customer.id
                data = {
                    'user_id': user.id,
                    'name': user.customer.name,
                }
                return Response(Tool.format_data(data))
            else:
                raise LoginException('账号或密码错误')
        except User.DoesNotExist:
            raise LoginException('账号不存在')


class LogoutView(APIView):

    def get(self, request):
        logout(request)
        return Response(Tool.format_data(), status=status.HTTP_200_OK)


class PasswordResetView(APIView):

    def post(self, request):
        """密码重置"""
        if request.user.is_authenticated:
            Tool.required_params(request, ['raw_password', 'new_password'])
            raw_password = request.data['raw_password']
            new_password = request.data['new_password']
            user = mm_Customer.reset_password_by_login(request.user.id, raw_password, new_password)
        else:
            account = request.data.get('account')
            password = request.data.get('password')
            code = request.data.get('code')
            user = mm_Customer.reset_password_by_sms(account, password, code)
        return Response(Tool.format_data(), status=status.HTTP_200_OK)


class CustomerProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        serializer = CustomerSerializer(request.user.customer)
        return Response(Tool.format_data(serializer.data))

    def post(self, request, format=None):
        serializer = CustomerSerializer(request.user.customer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(Tool.format_data(serializer.data))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return mm_Customer.get(pk=pk)
        except mm_Customer.model.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_200_OK)
