import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth    import AuthMiddlewareStack

from chats.routing import websocket_urlpatterns
from chats.middleware import QueryAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
    # Just HTTP for now. (We can add other protocols later.)
})