# @author: xws    time: 2019/8/26 15:16
from rest_framework.permissions import BasePermission


# 权限1
class SVIPPermission(BasePermission):

    message="必须是 SVIP 才能访问"

    def has_permission(self,request,view):
        if request.user.user_type!=3:
            # 无权访问
            return False
        # 有权访问
        return True


# 权限2
class MyPermission1(BasePermission):

    def has_permission(self,request,view):
        if request.user.user_type==3:
            # 无权访问
            return False
        # 有权访问
        return True
