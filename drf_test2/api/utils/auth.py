# @author: xws    time: 2019/8/24 19:47

from rest_framework import exceptions

from api import models
from rest_framework.authentication import BaseAuthentication


class FirstAuthtication(BaseAuthentication):

    def authenticate(self, request):
        pass

    def authenticate_header(self,request):
        pass


class Authtication(BaseAuthentication):
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
