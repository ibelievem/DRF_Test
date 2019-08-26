from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse,HttpResponse
from api import models

import hashlib
import time


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


# 权限
class MyPermission(object):

    def has_permission(self,request):
        pass


class AuthView(APIView):
    '''
    用于用户登录认证
    '''

    # 在settings中配置全部视图都需认证，但是当authentication_classes = []时，可免除认证，即使用匿名用户
    # 此时 requset.user=None , requset.auth=None
    authentication_classes = []

    def post(self,requset,*args,**kwargs):

        ret={"code":1000,"msg":None}
        try:
            user=requset._request.POST.get("username")
            pwd=requset._request.POST.get("password")
            obj=models.UserInfo.objects.filter(username=user,password=pwd).first()
            # print(obj,type(obj))
            # print(user,pwd)

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


class OrderView(APIView):
    """
    订单相关业务(只有 SVIP 用户有权限)
    """
    def get(self,request,*args,**kwargs):

        # request.user 为 token_obj.user
        # request.auth 为 token_obj

        if request.user.user_type != 3:
            return HttpResponse("无权访问！")

        ret={"code":1000,"msg":None}
        try:
            ret["data"]=ORDER_DICT

        except Exception as e:
            pass

        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    用户中心（普通用户、VIP）
    """

    def get(self,request,*args,**kwargs):
        print(request.user)
        print(request.auth)

        if request.user.user_type==3:
            return HttpResponse("无权访问")

        return HttpResponse("用户信息")
























