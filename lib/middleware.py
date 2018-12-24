#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/12/1 下午9:33
# @Author  : Frankie
# @Email   : zaihuazhao@163.com
# @File    : middleware.py
import json


class ResponseFormateMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

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
