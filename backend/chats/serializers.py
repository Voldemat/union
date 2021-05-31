from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    SerializerMethodField
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
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs['user']
            print(self.user)
            del kwargs['user']
        super().__init__(*args, **kwargs)

    name = SerializerMethodField('get_name')
    def get_name(self, chat):
        if getattr(self, "user", False):
            return chat.get_name(user = self.user)
        else:
            return chat.get_name()
    class Meta:
        model = Chat
        fields = [
            'id',
            'name'
        ]

