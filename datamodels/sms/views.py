from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from datamodels.sms.models import mm_SMSCode
from lib.aliyun_sms import send_simple_code, gen_code
from lib.tools import Tool


@csrf_exempt
@require_POST
def get_poll_code(request):
    """获取验证码"""
    Tool.required_params(request, ['account'])
    account = request.POST.get('account')
    code = gen_code()
    if not mm_SMSCode.can_get_new_code(tel=account):
        error = {
            'code': 1,
            'msg': '请过几分钟尝试'
        }
        return JsonResponse(error)
    response = send_simple_code(account, code)
    if response['Code'] == 'OK':
        mm_SMSCode.add(account, code)
        return JsonResponse({'code': 0})
    else:
        error = {
            'code': 1,
            'msg': response['Message']
        }
        return JsonResponse(error)


