import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

class ChatManager(models.Manager):
    def create_chat(self, *args, **kwargs) -> object:
        if 'users' in kwargs:

            self.users = kwargs['users']

            print(self.users)
            if len(self.users) < 2:
                raise ValueError("Chat should have minimum 2 users")

            del kwargs['users']

        chat = self.create(*args, **kwargs)


        if getattr(self, 'users', None):
            chat.users.add(*self.users)
            chat.save()

        return chat



class Message(models.Model):
    id = models.UUIDField(
        primary_key = True,
        db_index    = True,
        default     = uuid.uuid4,
        editable    = False
    )
    text = models.CharField(max_length = 500, null = True)
    writer = models.ForeignKey( settings.AUTH_USER_MODEL , on_delete = models.CASCADE )

    created_at = models.DateTimeField(auto_now_add = True, editable = False)

    chat = models.ForeignKey( 'Chat', on_delete = models.CASCADE, related_name = 'messages' )

    def __str__(self):
        return f'Message - {self.writer}'

class Chat(models.Model):
    id = models.UUIDField(
        primary_key = True,
        db_index    = True,
        default     = uuid.uuid4,
        editable    = False
    )

    name = models.CharField(max_length = 50, default = 'GroupChat')
    users = models.ManyToManyField(  settings.AUTH_USER_MODEL )

    objects = ChatManager()

    def __str__(self):
        return str(self.id)

    def is_personal(self):
        if len(self.users.all()) > 2:
            return False
        return True

    def get_name(self, *args, **kwargs):
        if self.is_personal() and 'user' in kwargs:
            return self.get_personal_chat_name(kwargs['user'])
        else:
            return self.name

    def get_personal_chat_name(self, user):
        for instance in self.users.all():
            if instance != user:
                return instance.get_full_name()
        return "Only you in chat"
