from django.conf.urls import url,include
from api import views

# 自动生成路由
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'xxx', views.View1View)
router.register(r'rt', views.View1View)

urlpatterns = [

    url(r'^(?P<version>[v1|v2]+)/users/$',views.UsersView.as_view(),name="users"),
    url(r'^(?P<version>[v1|v2]+)/django/$',views.DjangoView.as_view(),name="django"),
    url(r'^(?P<version>[v1|v2]+)/parser/$',views.ParserView.as_view(),name="parser"),


    url(r'^(?P<version>[v1|v2]+)/roles/$',views.RolesView.as_view(),name="roles"),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$',views.UserinfoView.as_view(),name="userinfo"),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)$',views.GroupView.as_view(),name="gp"),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$',views.UsergroupView.as_view(),name="usergroup"),


    url(r'^(?P<version>[v1|v2]+)/pager1/$',views.Pager1View.as_view()),


    # 查询所有、增加
    url(r'^(?P<version>[v1|v2]+)/view1/$',views.View1View.as_view({"get":"list","post":"create"})),
    # 查询单个、更新所有、删除、更新单个
    url(r'^(?P<version>[v1|v2]+)/view1/(?P<pk>\d+)$',views.View1View.as_view({"get":"retrieve",
                                                                              "delete":"destroy",
                                                                              "put":"update",
                                                                              "patch":"partial_update"
                                                                              })),




    url(r'^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view()),


    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]
