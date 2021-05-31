"""
    User global model
"""
import uuid
from itertools import chain

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from chats.models import Chat

class UserManager(BaseUserManager):
    def create_user(self, email:str = None, first_name:str = None, last_name:str = None, birth_date:str = None, avatar:object = None, about_me:str = None, password:str = None):
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            birth_date = birth_date,
            avatar = avatar,
            about_me = about_me
        )
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password = None):
        user = self.create_user(email = email, password = password)


        user.is_admin = True
        
        user.is_staff = True


        user.save(using = self._db)

        return user





class User(AbstractBaseUser, models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
    )

    email       = models.EmailField(
        verbose_name    = 'Email Address',
        max_length      = 255,
        unique          = True
    )
    first_name  = models.CharField('First name', max_length = 255)

    last_name   = models.CharField('Last name', max_length = 255)

    birth_date  = models.DateField('Birth date', blank = True, null = True)

    avatar      = models.ImageField(
        verbose_name    = 'Avatar',
        upload_to       = 'users/avatars/',
        blank           = True,
        null            = True
    )

    about_me    = models.CharField('About me', max_length = 1000, blank = True, null = True)

    is_active   = models.BooleanField(default = True)
    is_staff    = models.BooleanField(default = False)
    is_admin    = models.BooleanField(default = False)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_chats(self):
        chats:list = Chat.objects.filter(users__id = str(self.id))
        return chats


    def get_full_name(self):
        return self.first_name + self.last_name

        
    def has_perm(self, perm, obj = None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

