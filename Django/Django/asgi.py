import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.core.wsgi import get_wsgi_application

from Django import routings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django.settings")

# 默认仅支持http协议，修改以支持WebSocket
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 自动找urls.py, 找视图函数-->http
    "websocket": URLRouter(routings.websocket_urlpatterns),  # routings(urls) , consumers(views)
})
