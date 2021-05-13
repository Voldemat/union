from django.urls import re_path, path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path(r'ws/chats/<uuid:chat_id>/', ChatConsumer.as_asgi()),
]