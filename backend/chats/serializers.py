from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField
)

from chats.models import Message

class MessageSerializer(ModelSerializer):
    writer = StringRelatedField()
    class Meta:
        model = Message
        fields = [
            'text',
            'created_at',
            'writer'
        ]