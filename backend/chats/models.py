import uuid

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Message(models.Model):
    id = models.UUIDField(
        primary_key = True,
        db_index    = True,
        default     = uuid.uuid4,
        editable    = False
    )
    text = models.CharField(max_length = 500, null = True, blank = True)
    writer = models.ForeignKey( get_user_model(), on_delete = models.PROTECT )

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

    users = models.ManyToManyField(  get_user_model() )


    def __str__(self):
        return str(self.id)