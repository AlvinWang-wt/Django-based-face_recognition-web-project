from django.urls import re_path

from app import consumers

websocket_urlpatterns = [
    # xxxxx/room/x1 (和路由匹配上), 则走websocket协议的类
    re_path(r'/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
]