"""Django URL Configuration

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
from django.urls import path

from app import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # path('admin/', admin.site.urls),

    # 默认页面
    path('', views.video),

    # 子页面
    path('user/regist', views.user_regist),
    path('index/', views.index),
    path('admin/login', views.login),
    path('video/', views.video),

    # 局部刷新
    path('send/msg/', views.send_msg),
    path('get/msg/', views.get_msg),

    # 视频流响应
    path('video_feed/', views.video_feed),

]
