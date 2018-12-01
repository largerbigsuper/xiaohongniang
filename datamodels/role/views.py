from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from datamodels.role.models import mm_Customer
from datamodels.sms.models import mm_SMSCode
from lib.tools import Params


@csrf_exempt
@require_POST
def user_register(request):
    """用户注册"""
    required_params = ['code', 'login_tel', 'password']
    Params.required_params(request, required_params)
    code = request.POST.get('code')
    login_tel = request.POST.get('login_tel')
    password = request.POST.get('password')
    mm_SMSCode.is_effective(login_tel, code)
    mm_Customer.add(login_tel, password)
    return JsonResponse(dict(code=0))


@csrf_exempt
@require_POST
def customer_login(request):
    """登录"""
    required_params = ['login_tel', 'password']
    Params.required_params(request, required_params)
    login_tel = request.POST.get('login_tel')
    password = request.POST.get('password')
    try:
        user = authenticate(request, username=login_tel, password=password)
        if user:
            login(request, user)
            request.session['user_id'] = user.i
            request.session['customer_id'] = user.customer.id
            data = {
                'user_id': user.id,
                'name': user.customer.name,
            }
            return JsonResponse(data)
        else:
            return JsonResponse(dict(code=1, msg='账号或密码错误'))
    except User.DoesNotExist:
        return JsonResponse(dict(code=1, msg='账号不存在'))


def customer_logout(request):
    logout(request)
    return JsonResponse(dict(code=0))
