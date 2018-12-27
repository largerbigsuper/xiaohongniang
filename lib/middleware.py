#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午9:33
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : middleware.py
import datetime
import json
import time


class ResponseFormateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # 最近访问更新
        if request.user.is_authenticated:
            _now = time.mktime(datetime.datetime.now().timetuple())
            _last = request.session.get('last_requst_at')
            if isinstance(_last, datetime.datetime):# 数据库中读取的session是datetime格式，需进行转化；redis中不能存储datetime格式数据
                _last = time.mktime(_last.timetuple())
                request.session['last_requst_at'] = _last
            if _last:
                if _last + 5 * 60 < _now:
                    request.session['last_requst_at'] = _now
                    request.user.customer.last_request_at = datetime.datetime.fromtimestamp(_now)
                    request.user.customer.save()
            else:
                request.session['last_requst_at'] = _now
                request.user.customer.last_request_at = datetime.datetime.fromtimestamp(_now)
                request.user.customer.save()

        if response.status_code in [200, 201, 204]:
            if response.status_code in [201, 204]:
                response.status_code = 200
            if hasattr(response, 'data'):
                if not response.data:
                    response.data = {
                        'msg': 'OK',
                        'data': None
                    }
                    response.content = bytes(json.dumps(response.data).encode('utf-8'))
                else:
                    if 'msg' not in response.data:
                        response.data = {
                            'msg': 'OK',
                            'data': response.data
                        }
                        response.content = bytes(json.dumps(response.data).encode('utf-8'))

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_exception(self, request, exception):
        # if isinstance(exception, LVError):
        #     return JsonResponse(dict(code=exception.code, msg=exception.msg))
        # else:
        #     return None
