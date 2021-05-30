from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField
)

from chats.models import Message, Chat
from users.serializers import UserSerializer

class MessageSerializer(ModelSerializer):
    writer = UserSerializer(many = False)
    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'created_at',
            'writer'
        ]

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = [
            'id',
            'name',
        ]