from django.shortcuts import render,HttpResponse

# Create your views here.

from rest_framework.views import APIView
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning


class UsersView(APIView):

    # 局部使用
    # 1、URL中通过GET传参
    # versioning_class = QueryParameterVersioning

    # 2、在URL路径中传参，推荐使用此方式
    # versioning_class = URLPathVersioning

    def get(self,request,*args,**kwargs):

        # 获取版本
        print(request.version)

        # 获取处理版本类的对象
        print(request.versioning_scheme)

        # 反向生成URL
        url=request.versioning_scheme.reverse(viewname="users",request=request)
        print(url)

        return HttpResponse("用户列表")


class DjangoView(APIView):

    def post(self,request,*args,**kwargs):
        from django.core.handlers.wsgi import WSGIRequest
        print(type(request._request))
        return HttpResponse("POST和Body")
