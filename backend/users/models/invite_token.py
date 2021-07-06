import uuid
import datetime

from django.db import models

from .user import User

class InviteToken(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
    )

    user_inviting = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "my_invite")

    user_invited = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "not_my_invite", blank = True)


    updated_at = models.DateTimeField(auto_now_add = True)
    
    expired_at = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(days = 1))

    def __str__(self) -> str:
        # return string representation of instance...
        return str(self.id)


    def save(self, *args, **kwargs) -> None:
        super(InviteToken, self).save(*args, **kwargs)
        if self.user_invited and self.user_invited != self.user_inviting:
            User.bind_friends(self.user_invited, self.user_inviting)

        return None
        
    def expired(self) -> bool:
        """
            [HELP DOCS]
                Expired is InviteToken flag property.
                If invited user is defined expired flag will be True.
        """

        if self.user_invited:
            return True

        elif self.updated_at < self.expiry_at:
            return True

        return False

    def time_to_expire(self) -> datetime.datetime:
        return self.expired_at.replace(tzinfo = None) - datetime.datetime.now().replace(tzinfo = None)