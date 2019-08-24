from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse,HttpResponse
from api import models

import hashlib
import time

from rest_framework import exceptions


ORDER_DICT={
    1:{
        "name":"张三",
        "age":18,
        "gender":"男",
        "content":"这是张三的信息"
    },
    2: {
        "name": "李四",
        "age": 20,
        "gender": "男",
        "content": "这是李四的信息"
    },
}

# MD5加密
def md5(user):

    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):
    '''
    用于用户登录认证
    '''

    def post(self,requset,*args,**kwargs):

        ret={"code":1000,"msg":None}
        try:
            user=requset._request.POST.get("username")
            pwd=requset._request.POST.get("password")
            obj=models.UserInfo.objects.filter(username=user,password=pwd).first()
            # print(obj,type(obj))
            if not obj:
                ret["code"]=1001
                ret["msg"]="用户名或密码错误"

            # 登录用户创建 token
            token=md5(user)

            # 数据库中的token表中存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj,defaults={"token":token})

            ret["token"]=token

        except Exception as e:
            ret["code"]=1002
            ret["msg"]="请求异常"


        return JsonResponse(ret)


class Authtication(object):
    def authenticate(self,request):
        token=request._request.GET.get("token")
        # filter() 返回对象数据集， .first() 获取数据集中的第一个
        # filter 无数据返回空，但是 get 无数据会报错
        token_obj=models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")

        # 在rest framework 内部会将整个两个字段赋值给request，以供后续操作使用
        return (token_obj.user,token_obj)


    def authenticate_header(self,request):
        pass


class OrderView(APIView):
    """
    订单相关业务
    """

    authentication_classes = [Authtication,]

    def get(self,request,*args,**kwargs):

        # request.user 为 token_obj.user
        # request.auth 为 token_obj

        # print(request.user)
        # print(request.auth)

        ret={"code":1000,"msg":None}
        try:
            ret["data"]=ORDER_DICT

        except Exception as e:
            pass

        return JsonResponse(ret)

class UserInfoView(APIView):
    """
    用户中心
    """
    authentication_classes = [Authtication,]

    def get(self,request,*args,**kwargs):
        return HttpResponse("用户信息")
























