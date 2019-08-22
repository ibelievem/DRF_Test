from django.shortcuts import render,HttpResponse
import json
from django.views import View

# json.dumps():将一个Python数据结构转换为json
# json.loads():将一个JSON编码的字符串转换回一个Python数据结构


# FBV  函数视图--function base view
def users(request):
    user_list=['alex','oldboy']
    return HttpResponse(json.dumps(user_list))


# CBV  类视图--class base view
class StudentsView(View):

    def get(self,request,*args,**kwargs):
        return HttpResponse('GET')

    def post(self,request,*args,**kwargs):
        return HttpResponse('POST')

    def put(self,request,*args,**kwargs):
        return HttpResponse('PUT')

    def delete(self,request,*args,**kwargs):
        return HttpResponse('DELETE')
