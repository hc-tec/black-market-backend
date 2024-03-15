from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from . import urls

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            urls.websocket_urlpatterns  # 指明路由文件是django_websocket/routing.py,类似于路由分发
        )
    ),
})
