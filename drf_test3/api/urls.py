from django.conf.urls import url
from api import views

urlpatterns = [

    url(r'^(?P<version>[v1|v2]+)/users/$',views.UsersView.as_view(),name="users"),
    url(r'^(?P<version>[v1|v2]+)/django/$',views.DjangoView.as_view(),name="users"),

]
