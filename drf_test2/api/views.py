from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from django.http import JsonResponse
from api import models

import hashlib
import time


# MD5加密
def md5(user):

    ctime=str(time.time())
    m=hashlib.md5(bytes(user,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):

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































