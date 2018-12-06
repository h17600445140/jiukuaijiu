#coding=utf-8
from  django.http.response import HttpResponseRedirect
from jiukuaijiu import  settings

class UserAuth(object):
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request,*args, **kwargs):
        # 请求前
        if request.path in settings.AUTH:
            user = request.session.get('user', '')
            if not user:
                # 不满足条件重定向
                return  HttpResponseRedirect('/user/login')
        # 下面是原生访问
        return self.get_response(request)
        # 请求后
