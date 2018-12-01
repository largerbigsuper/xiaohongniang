from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from datamodels.sms.models import mm_SMSCode
from lib.aliyun_sms import send_simple_code, gen_code


@csrf_exempt
@require_POST
def get_poll_code(request):
    """获取验证码"""
    if 'login_tel' not in request.POST:
        error = {
            'code': 1,
            'msg': '缺少参数login_tel'
        }
        return JsonResponse(error)
    login_tel = request.POST.get('login_tel')
    code = gen_code()
    if not mm_SMSCode.can_get_new_code(tel=login_tel):
        error = {
            'code': 1,
            'msg': '请过几分钟尝试'
        }
        return JsonResponse(error)
    response = send_simple_code(login_tel, code)
    if response['Code'] == 'OK':
        mm_SMSCode.add(login_tel, code)
        return JsonResponse({'status_code': 0})
    else:
        error = {
            'code': 1,
            'msg': response['Message']
        }
        return JsonResponse(error)


