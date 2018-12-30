import logging

from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from datamodels.role.models import mm_Customer, RELATIONSHIP_FOLLOWING
from datamodels.role.serializers import CustomerSerializer, FollowingRelationShipSerializer, \
    FollowersRelationShipSerializer, CustomerListSerializer, BaseRelationShipSerializer, \
    CustomerHasSkillsListSerializer, CustomerSingleListSerializer, NormalCoustomerSerializer
from datamodels.sms.models import mm_SMSCode
from datamodels.stats.models import mm_OperationRecord
from lib import customer_login
from lib.exceptions import LoginException, DBException
from lib.im import IMServe
from lib.pagination import ReturnTwentyPagination
from lib.qiniucloud import QiniuServe
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
        customer_login.login(request, customer.user)
        data = dict(account=account, id=customer.id, user_id=customer.user.id)
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
                customer_login.login(request, user)
                data = {
                    'id': user.customer.id,
                    'user_id': user.id,
                    'name': user.customer.name,
                    'im_token': user.customer.im_token,
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
        _name = request.user.customer.name
        _avatar_url = request.user.customer.avatar_url
        serializer = CustomerSerializer(request.user.customer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if 'avatar_url' in serializer.validated_data:
                serializer.validated_data['avatar_url'] = QiniuServe.bucket_domain_dict['image'] + \
                                                          serializer.validated_data['avatar_url']
            serializer.save()
            if any([not _name == serializer.data['name'], not _avatar_url == serializer.data['avatar_url']]):
                IMServe.refresh_token(request.user.id, request.user.customer.name, request.user.customer.avatar_url)
                #TODO 删除替换的图片
            return Response(Tool.format_data(serializer.data))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerListSerializer

    def get_queryset(self):
        return mm_Customer.all()


class ActiveCustomerList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerListSerializer

    def get_queryset(self):
        return mm_Customer.active_customers()


class CustomerWithSkillsList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerHasSkillsListSerializer

    def get_queryset(self):
        return mm_Customer.customers_with_skills()


class CustomerSingleList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSingleListSerializer
    pagination_class = ReturnTwentyPagination

    def get_queryset(self):
        return mm_Customer.customers_need_paired()


class CustomerDetail(generics.RetrieveAPIView):
    """
    Retrieve, update or delete a snippet instance.

    """
    queryset = mm_Customer.all()
    serializer_class = CustomerListSerializer

    def get(self, request, *args, **kwargs):
        to_customer = self.get_object()
        if not to_customer.id == request.session['customer_id']:
            mm_OperationRecord.add_opreation_record(request.session['customer_id'], to_customer)
        return super().get(request, *args, **kwargs)


class MyFollowerView(APIView):
    """
    我的关注
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        customer_id = request.data['coustomer_id']
        relationship_status = request.data.get('status', RELATIONSHIP_FOLLOWING)
        relationship = request.user.customer.add_relationship(customer_id, relationship_status)
        serializer = BaseRelationShipSerializer(relationship)
        return Response(Tool.format_data(serializer.data))

    def delete(self, request, format=None):
        customer_id = request.query_params.get('customer_id', 0)
        request.user.customer.remove_relationship(customer_id)
        return Response(Tool.format_data())


class MyFollowersList(generics.ListAPIView):
    """
    关注我的
    """
    def get_queryset(self):
        return self.request.user.customer.get_follower_recoreds()

    serializer_class = FollowersRelationShipSerializer
    permission_classes = (IsAuthenticated,)


class MyFollowingList(generics.ListAPIView):
    """
    我的关注
    """
    def get_queryset(self):
        return self.request.user.customer.get_following_recoreds()

    serializer_class = FollowingRelationShipSerializer
    permission_classes = (IsAuthenticated,)


class UnfollowingList(generics.ListAPIView):
    """
    未关注列表
    """
    def get_queryset(self):
        return self.request.user.customer.get_unfollowing_customers()

    serializer_class = NormalCoustomerSerializer
    permission_classes = (IsAuthenticated,)


class CustomerSearchView(generics.ListAPIView):
    """
    用户搜索
    """

    def get_queryset(self):
        allowed_search_keys = ['gender', 'name', 'age', 'is_shop_keeper', 'is_show_skill', 'is_rut']
        params = dict()
        gender = self.request.query_params.get('gender')
        name = self.request.query_params.get('name')
        age = self.request.query_params.get('age')
        is_shop_keeper = self.request.query_params.get('is_shop_keeper')
        is_show_skill = self.request.query_params.get('is_show_skill')
        is_rut = self.request.query_params.get('is_rut')
        if gender:
            params['gender'] = int(gender)
        if name:
            params['name__icontains'] = name
        if age:
            params['age'] = int(age)
        if is_shop_keeper:
            params['is_shop_keeper'] = int(is_shop_keeper)
        if is_show_skill:
            params['is_show_skill'] = int(is_show_skill)
        if is_rut:
            params['is_rut'] = int(is_rut)
        if gender:
            params['gender'] = int(gender)
        return mm_Customer.filter(**params)

    serializer_class = NormalCoustomerSerializer
    permission_classes = (IsAuthenticated,)

