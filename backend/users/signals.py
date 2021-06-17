from typing import Optional

from django.contrib.auth import get_user_model

from django.db.models import Model
from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver


@receiver(pre_save, sender = get_user_model())
def delete_self_from_friends(
    sender:Model,
    instance:get_user_model(),
    raw:bool,
    using:str,
    update_fields:Optional[set], *args, **kwargs) -> None:

    instance.friends.remove(instance.id)
    print('pre_save')
    print(instance.friends.all())
    return None

@receiver(post_save, sender = get_user_model())
def check(sender, instance, *args, **kwargs) -> None:
    print('post_save')
    print(instance.friends.all())
    return None