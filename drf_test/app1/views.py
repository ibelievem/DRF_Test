from django.shortcuts import render,HttpResponse
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils.decorators import method_decorator

# json.dumps():将一个Python数据结构转换为json
# json.loads():将一个JSON编码的字符串转换回一个Python数据结构

# csrf_exempt   未注释中间件情况下免除csrf认证
# csrf_protect  在注释中间件情况下csrf认证


# FBV  函数视图--function base view
@csrf_exempt
def users(request):
    user_list=['alex','oldboy']
    return HttpResponse(json.dumps(user_list))


# --------------------------------------------------------------------------------
# class MyBaseView(object):
#     # 类似于装饰器，可以在执行前后增加相关操作
#     # 类似于中间件
#     def dispatch(self, request, *args, **kwargs):
#         print("执行前")
#         ret=super(MyBaseView,self).dispatch(request,*args,**kwargs)
#         print("执行后")
#         return ret
#
# # CBV  类视图--class base view
# # 多继承中优先执行 MyBaseView，就近原则
# class StudentsView(MyBaseView,View):
#
#     def get(self,request,*args,**kwargs):
#         return HttpResponse('GET')
#
#     # 在cbv（类视图）中使用装饰器的解决csrf认证的方法
#     @method_decorator(csrf_exempt)
#     def post(self,request,*args,**kwargs):
#         return HttpResponse('POST')
#
#     def put(self,request,*args,**kwargs):
#         return HttpResponse('PUT')
#
#     def delete(self,request,*args,**kwargs):
#         return HttpResponse('DELETE')
# --------------------------------------------------------------------------------

@method_decorator(csrf_exempt,name="dispatch")
class StudentsView(View):

    # 在cbv（类视图）中使用装饰器的解决csrf认证的方法
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(StudentsView,self).dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        return HttpResponse('GET')

    def post(self,request,*args,**kwargs):
        return HttpResponse('POST')

    def put(self,request,*args,**kwargs):
        return HttpResponse('PUT')

    def delete(self,request,*args,**kwargs):
        return HttpResponse('DELETE')


# ======================================================================
# 非 restful 规范
# def get_order(request):
#     return HttpResponse('')
#
#
# def add_order(request):
#     return HttpResponse('')
#
#
# def del_order(request):
#     return HttpResponse('')
#
#
# def update_order(request):
#     return HttpResponse('')


# restful 规范

# ---------------------
# FBV
# def order(request):
#     if request.method=="GET":
#         return HttpResponse("获取订单")
#     elif request.method=="POST":
#         return HttpResponse("创建订单")
#     elif request.method=="PUT":
#         return HttpResponse("更新订单")
#     elif request.method=="DELETE":
#         return HttpResponse("删除订单")

# ---------------------
# CBV
class OrderView(View):
    def get(self,*args,**kwargs):

        ret={
            "code":1000,
            "msg":"xxx",
        }
        return HttpResponse(json.dumps(ret),status=201)

    def post(self,*args,**kwargs):
        return HttpResponse("创建订单")

    def put(self,*args,**kwargs):
        return HttpResponse("更新订单")

    def delete(self,*args,**kwargs):
        return HttpResponse("删除订单")


# ############### django rest framework ###########################
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions
from rest_framework.request import Request


class MyAuthentication(object):
    def authenticate(self,request):
        token=request._request.GET.get("token")
        # 获取用户名和密码，去数据库校验
        if not token:
            raise exceptions.AuthenticationFailed("用户认证失败！")
        return ("alex",None)

    def authenticate_header(self,val):
        pass


class DogView(APIView):

    authentication_classes = [MyAuthentication,]

    def get(self,request,*args,**kwargs):

        # 此时的request不再是原生的request，而是封装过后的request
        print(request)
        # 输出 alex
        print(request.user)

        ret={
            "code":1000,
            "msg":"xxx",
        }
        return HttpResponse(json.dumps(ret),status=201)

    def post(self,*args,**kwargs):
        return HttpResponse("创建Dog")

    def put(self,*args,**kwargs):
        return HttpResponse("更新Dog")

    def delete(self,*args,**kwargs):
        return HttpResponse("删除Dog")
