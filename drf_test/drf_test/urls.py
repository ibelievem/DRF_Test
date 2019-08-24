"""drf_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app1 import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', views.users),
    url(r'^students/', views.StudentsView.as_view()),


    # 非 restful 规范
    # url(r'^get_order/',views.get_order),
    # url(r'^add_order/',views.add_order),
    # url(r'^del_order/',views.del_order),
    # url(r'^update_order/',views.update_order),


    # restful 规范
    # FBV
    # url(r'^order/',views.order),

    # CBV
    url(r'^order/',views.OrderView.as_view()),


    url(r'^dog/',views.DogView.as_view()),




]
