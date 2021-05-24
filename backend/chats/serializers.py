from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField
)

from chats.models import Message, Chat

class MessageSerializer(ModelSerializer):
    writer = StringRelatedField()
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
            'id'
        ]