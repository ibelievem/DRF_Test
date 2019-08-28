from django.shortcuts import render,HttpResponse

# Create your views here.

from rest_framework.views import APIView
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning

from rest_framework.parsers import JSONParser,FormParser
from rest_framework.request import Request

from api import models
import json


# --------------------------解析器---------------------------------------------
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
        print(type(request._request))
        return HttpResponse("POST和Body")


class ParserView(APIView):

    # 局部配置解析器
    # parser_classes = [JSONParser,FormParser]

    """
    JSONParser：表示只能解析 content-type:application/json 头
    FormParser：表示只能解析 content-type:application/x-www-form-urlencode 头
    """

    def post(self,request,*args,**kwargs):
        """
        允许用户发送json格式数据
            a. content-type:application/json
            b. {"name"："alex","age":18}
        """
        # 获取解析后的结果,用的时候才去解析
        """
        1、获取用户的请求头
        2、获取用户的请求体
        3、根据用户的请求头和 parser_classes=[JSONParser,FormParser]中支持的请求头进行比较
        4、JSONParser对象去处理请求体
        5、request.data
        """
        print(request.data)

        # 字典类型
        print(type(request.data))

        return HttpResponse("ParserView")


# --------------------------序列化-----------------------------------------------------
from rest_framework import serializers


class RolesSerializer(serializers.Serializer):

    id=serializers.IntegerField()
    title=serializers.CharField()


class RolesView(APIView):

    def get(self, request, *args, **kwargs):

        # 序列化方式一：自定义
        # roles=models.Role.objects.all().values("id","title")
        #
        # # 将 QuerySet 类型转换为 list 类型
        # roles=list(roles)
        #
        # print(roles)
        # print(type(roles))
        #
        # # json 只能序列化 python 的数据类型，不能够序列化django的数据类型
        # # 此时 json 可以序列化列表类型
        # # ensure_ascii=False 中文正常显示
        # ret=json.dumps(roles,ensure_ascii=False)
        #
        # # ret 字符串类型
        # # [{"id": 1, "title": "医生"}, {"id": 2, "title": "教师"}, {"id": 3, "title": "学生"}] <class 'str'>
        # print(ret,type(ret))

        # --------------------------------------------------------------------------------------------

        # 方式二：对于[obj,obj,obj...]
        roles=models.Role.objects.all()
        ser=RolesSerializer(instance=roles,many=True)
        # ser.data 已经是转换完成的结果

        ret = json.dumps(ser.data, ensure_ascii=False)
        print(ret,type(ret))
        return HttpResponse(ret)


# 方式二：继承 serializers.Serializer
# class UserinfoSerializer(serializers.Serializer):
#
#     # 参数source指明数据库的字段
#     user_type_num=serializers.CharField(source="user_type")
#     user_type=serializers.CharField(source="get_user_type_display")
#     username=serializers.CharField()
#     password=serializers.CharField()
#
#     # 多对一查询时：
#     gp=serializers.CharField(source="group.title")
#
#     # 多对多查询时：
#     # rls=serializers.CharField(source="roles.all") #不能用
#     # 自定义显示
#     rls=serializers.SerializerMethodField() # 使用此方式
#
#     # row 当前行的对象
#     def get_rls(self,row):
#         role_obj_list=row.roles.all()
#         ret=[]
#         for item in role_obj_list:
#             ret.append({"id":item.id,"title":item.title})
#         return ret


# 方式三：继承serializers.ModelSerializer
# class UserinfoSerializer(serializers.ModelSerializer):
#     ooo = serializers.CharField(source="get_user_type_display")
#     rls = serializers.SerializerMethodField()
#     group=serializers.CharField(source="group.title")
#
#     class Meta:
#         model=models.UserInfo
#         # fields="__all__"
#         fields=["id","username","password","ooo","rls","group"]
#
#     # row 当前行的对象
#     def get_rls(self,row):
#         role_obj_list=row.roles.all()
#         ret=[]
#         for item in role_obj_list:
#             ret.append({"id":item.id,"title":item.title})
#         return ret


class UserinfoSerializer(serializers.ModelSerializer):
    # 反向生成某字段的url
    group = serializers.HyperlinkedIdentityField(view_name='gp',lookup_field="group_id",lookup_url_kwarg="pk")

    class Meta:
        model=models.UserInfo
        # fields="__all__"
        fields=["id","username","password","group","roles"]

        # 深度 最好 0~4 之间
        depth=0



class UserinfoView(APIView):
    def get(self,request,*args,**kwargs):
        users = models.UserInfo.objects.all()
        # 对象，Serializer类处理 ： self.to_representation
        # QuerySet，ListSerializer类处理：self.to_representation
        # 1、实例化，一般是将数据封装到对象：先执行__new__ , 后执行 __init__
        """
        many=Ture,接下来执行 ListSerializer 对象的构造方法
        many=False,接下来执行 UserinfoSerializer 对象的构造方法
        """
        ser=UserinfoSerializer(instance=users,many=True,context={"request":request})
        print(ser.data)

        # 2、调用对象的 data 属性
        ret = json.dumps(ser.data, ensure_ascii=False)
        print(ret,type(ret))

        return HttpResponse(ret)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserGroup
        fields="__all__"


class GroupView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        obj=models.UserGroup.objects.filter(pk=pk).first()
        ser=GroupSerializer(instance=obj,many=False)
        ret=json.dumps(ser.data,ensure_ascii=False)

        return HttpResponse(ret)


##################### 验证 #############################


class PasswordValidator(object):
    def __init__(self, base):
        self.base = str(base)

    def __call__(self, value):
        if value != self.base:
            message = '标题必须以 %s 为开头。' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class UsergroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={"required":"标题不能为空"},validators=[PasswordValidator("老男人")])


class UsergroupView(APIView):

    def post(self, request, *args, **kwargs):
        # print(request.data)
        ser=UsergroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data["title"])
        else:
            print(ser.errors)

        return HttpResponse("提交数据")


# ---------------------------------------------------------  分页  -----------------------------------------------------


# =============================方式一、分页，看第几页，每页显示n条数据===========================

# from api.utils.serializers.pager import PagerSerializer
# from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination


# # 根据自己写的类可以定制通过参数修改每页的数据量
# 方式一、分页，看第几页，每页显示n条数据
# class MyPageNumberPagination(PageNumberPagination):
#     # 每页的显示个数
#     page_size = 2
#     # 通过参数 size 修改每页显示的个数
#     page_size_query_param = "size"
#     # 每页最多显示 5 个
#     max_page_size = 5
#
#     # 通过参数 page 设置页码
#     page_query_param = 'page'
#
#
# class Pager1View(APIView):
#
#     def get(self, request, *args, **kwargs):
#         # 获取所有数据
#         roles=models.Role.objects.all()
#
#         # 创建分页对象，根据自己写的类可以定制通过参数修改每页的数据量
#         # pg=MyPageNumberPagination()
#         # 创建分页对象，按部就班的显示每页的数据量
#         pg=PageNumberPagination()
#
#         # 在数据库中获取分页的数据
#         pager_roles=pg.paginate_queryset(queryset=roles,request=request,view=self)
#         print(pager_roles)
#
#         # 对数据进行序列化
#         ser=PagerSerializer(instance=pager_roles,many=True)
#
#         # 返回的不仅有数据，还有上下页的 url
#         # return pg.get_paginated_response(ser.data)
#
#         return Response(ser.data)


# =============================方式二、分页，在某个位置，向后查看n条数据 ===========================

# from api.utils.serializers.pager import PagerSerializer
# from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination
#
#
# # # 根据自己写的类可以定制通过参数修改每页的数据量
# # # 方式二、分页，在某个位置，向后查看n条数据
# class MyPageNumberPagination(LimitOffsetPagination):
#
#     # 每页默认从索引向后取 2 条数据
#     default_limit = 2
#     # 通过参数 size 修改从索引向后取数据的个数
#     limit_query_param = 'limit'
#     # 从索引向后取数据的个数最多5条
#     max_limit = 5
#
#     # 索引位置
#     offset_query_param = 'offset'
#
#
# class Pager1View(APIView):
#
#     def get(self, request, *args, **kwargs):
#         # 获取所有数据
#         roles=models.Role.objects.all()
#
#         # 创建分页对象，根据自己写的类可以定制通过参数修改每页的数据量
#         # pg=MyPageNumberPagination()
#         # 创建分页对象，按部就班的显示每页的数据量
#         pg=LimitOffsetPagination()
#
#         # 在数据库中获取分页的数据
#         pager_roles=pg.paginate_queryset(queryset=roles,request=request,view=self)
#         print(pager_roles)
#
#         # 对数据进行序列化
#         ser=PagerSerializer(instance=pager_roles,many=True)
#
#         # 返回的不仅有数据，还有上下页的 url
#         # return pg.get_paginated_response(ser.data)
#
#         return Response(ser.data)


# =============================方式三、加密分页，上一页和下一页 ===========================

from api.utils.serializers.pager import PagerSerializer
from rest_framework.pagination import CursorPagination


# 根据自己写的类可以定制通过参数修改每页的数据量
# 方式三、分页，在某个位置，向后查看n条数据
class MyPageNumberPagination(CursorPagination):

    # 页码参数，加密过后的页码
    cursor_query_param = 'cursor'
    # 每页显示的数据量
    page_size = 2
    # 按照 id 正序排列每页的数据
    ordering = 'id'
    # 修改每页显示的数据量
    page_size_query_param = None

    # 修改每页显示的最大数据量
    max_page_size = None


class Pager1View(APIView):

    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles=models.Role.objects.all()

        # 创建分页对象，根据自己写的类可以定制通过参数修改每页的数据量
        pg=MyPageNumberPagination()
        # 创建分页对象，按部就班的显示每页的数据量
        # pg=CursorPagination()

        # 在数据库中获取分页的数据
        pager_roles=pg.paginate_queryset(queryset=roles,request=request,view=self)
        print(pager_roles)

        # 对数据进行序列化
        ser=PagerSerializer(instance=pager_roles,many=True)

        # 返回的不仅有数据，还有上下页的 url
        # 因为页码加密，因此必须用此方式返回数据
        return pg.get_paginated_response(ser.data)


# ---------------------------------------------------------  视图  -----------------------------------------------------

# 1、继承 GenericAPIView ，无意义
"""
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class View1View(GenericAPIView):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = MyPageNumberPagination

    def get(self,request,*args,**kwargs):

        # 获取数据
        roles=self.get_queryset()  # models.Role.objects.all()

        # 从[1,1000]中取 [1,10]
        pager_roles=self.paginate_queryset(roles)

        # 序列化数据
        ser=self.get_serializer(instance=pager_roles,many=True)

        return Response(ser.data)
"""


# 2、继承 GenericViewSet ，稍微有意义，视图的不同引发路由的改变
"""
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

class View1View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = MyPageNumberPagination

    def list(self,request,*args,**kwargs):

        # 获取数据
        roles=self.get_queryset()  # models.Role.objects.all()

        # 从[1,1000]中取 [1,10]
        pager_roles=self.paginate_queryset(roles)

        # 序列化数据
        ser=self.get_serializer(instance=pager_roles,many=True)

        return Response(ser.data)
"""


# 3、继承 ModelViewSet，推荐使用

# ModelViewSet(mixins.CreateModelMixin,
#              mixins.RetrieveModelMixin,
#              mixins.UpdateModelMixin,
#              mixins.DestroyModelMixin,
#              mixins.ListModelMixin,
#              GenericViewSet)
# mixins.CreateModelMixin,  增加数据，
# mixins.RetrieveModelMixin,查询单条数据，需要传 id
# mixins.UpdateModelMixin,  更新数据，需要传 id
# mixins.DestroyModelMixin, 删除数据，需要传 id
# mixins.ListModelMixin,    查询所有数据
# GenericViewSet):   实现方法的映射

from rest_framework.viewsets import ModelViewSet


class View1View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = MyPageNumberPagination
















