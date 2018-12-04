from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response

from datamodels.sms.models import mm_SMSCode
from lib.aliyun_sms import send_simple_code, gen_code
from lib.exceptions import LVError
from lib.tools import Tool


@csrf_exempt
@api_view(['POST'])
def get_poll_code(request):
    """获取验证码"""
    Tool.required_params(request, ['account'])
    account = request.data.get('account')
    code = gen_code()
    if not mm_SMSCode.can_get_new_code(tel=account):
        raise LVError('请过几分钟尝试')
    response = send_simple_code(account, code)
    if response['Code'] == 'OK':
        mm_SMSCode.add(account, code)
        return Response("OK")
    else:
        raise LVError(response['Message'])


