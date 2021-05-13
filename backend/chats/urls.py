from django.urls import path

from chats.views import index, chat
urlpatterns = [
    path('', index, name = 'index'),
    path('<uuid:id>/', chat, name='chat'),
]