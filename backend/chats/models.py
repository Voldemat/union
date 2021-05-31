import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

class Message(models.Model):
    id = models.UUIDField(
        primary_key = True,
        db_index    = True,
        default     = uuid.uuid4,
        editable    = False
    )
    text = models.CharField(max_length = 500, null = True)
    writer = models.ForeignKey( settings.AUTH_USER_MODEL , on_delete = models.PROTECT )

    created_at = models.DateTimeField(auto_now_add = True, editable = False)

    chat = models.ForeignKey( 'Chat', on_delete = models.PROTECT, related_name = 'messages' )

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
        return "It`s not your chat impostor!"
