# @author: xws    time: 2019/8/26 18:31
from rest_framework.throttling import BaseThrottle,SimpleRateThrottle

# 自定义的类实现访问控制频率
'''
import time

VISIT_RECODE={}


class VisitThrottle(BaseThrottle):
    """10秒内只能访问3次"""

    def __init__(self):
        self.history=None

    def allow_request(self,request,view):

        # 1、获取用户的IP
        # remote_addr=request.META.get("REMOTE_ADDR")
        remote_addr=self.get_ident(request)

        # print(remote_addr)
        ctime=time.time()

        if remote_addr not in VISIT_RECODE:
            VISIT_RECODE[remote_addr]=[ctime,]
            return True
        # 使用get获取字典键对应的值时，不存在不会报错
        history=VISIT_RECODE.get(remote_addr)
        self.history=history

        while history and history[-1] < ctime - 10:
            # 删除此值
            history.pop()

        if len(history)<3:
            history.insert(0,ctime)
            return True

        # 表示没有被限制,可以继续访问
        # return True

        # 表示访问频率过高，被限制
        return False

    def wait(self):
        """还需要等多少秒才可以访问"""
        ctime=time.time()
        return 10-(ctime-self.history[-1])
'''


# 使用内置类实现访问控制频率
# 对于匿名用户实现访问控制频率
class VisitThrottle(SimpleRateThrottle):
    # 当key使用
    scope = "Xws"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# 对于登录用户实现访问控制频率
class UserThrottle(SimpleRateThrottle):
    # 当key使用
    scope = "XwsUser"

    def get_cache_key(self, request, view):
        return request.user.username
