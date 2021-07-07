import uuid
from typing import Optional

from django.db import models
from django.db.models.query          import QuerySet
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from chats.models import Chat

class UserManager(BaseUserManager):
    def create_user(
        self:object,
        email:str       = None,
        first_name:str  = None,
        last_name:str   = None,
        birth_date:str  = None,
        avatar:object   = None,
        about_me:str    = None,
        password:str    = None, 
        *args, **kwargs) -> object: # -> User


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

    def create_superuser(self, email, password = None) -> object: # -> User
        user = self.create_user(email = email, password = password)


        user.is_admin = True
        
        user.is_staff = True


        user.save(using = self._db)

        return user


    # assign create_user func to create  
    create = create_user




class User(AbstractBaseUser, PermissionsMixin):
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
    first_name  = models.CharField('First name', max_length = 255, null = True)

    last_name   = models.CharField('Last name', max_length = 255, null = True)

    birth_date  = models.DateField('Birth date', blank = True, null = True)

    avatar      = models.ImageField(
        verbose_name    = 'Avatar',
        upload_to       = 'users/avatars/',
        blank           = True,
        null            = True
    )

    about_me    = models.CharField('About me', max_length = 1000, blank = True, null = True)

    friends     = models.ManyToManyField("User", blank = True) 
    is_active   = models.BooleanField(default = True)
    is_staff    = models.BooleanField(default = False)
    is_admin    = models.BooleanField(default = False)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        # String representation of user is email
        return self.email


    def get_chats(self) -> QuerySet:
        # return all chats with self user
        chats:QuerySet = Chat.objects.filter(users__id = str(self.id))
        return chats


    def get_friends(self) -> QuerySet:
        # return all self user friends
        queryset:QuerySet = self.friends.all()
        return queryset

    def get_friends_chats(self) -> Optional[list]:
        # init friends_chats list
        friends_chats:list = list()

        # go over all self user friends
        for friend in self.get_friends():
            # check that self user have friend chat with friend user instance
            chat:Optional[Chat] = self.get_friend_chat(friend)

            # if chat DoesNotExist create new
            if chat == None:
                chat = Chat.objects.create(users = [self, friend])

            # append chat to friends_list
            friends_chats.append(chat)

        # return list of friends_chats if (it has at least one element) else return None
        return friends_chats if friends_chats else None

    def get_friend_chat(self, friend:object) -> Optional[Chat]:

        # iterate over all self user chats
        for chat in self.get_chats():
            # get chat users list
            chat_users:QuerySet = chat.users.all()

            # return chat if it has 2 users and one of them is self user
            # and other is friend, passed in function
            if len(chat_users) == 2 and self in chat_users and friend in chat_users:
                return chat

        # if self user doesn`t have chat with defined friend return None
        return None


    def get_full_name(self) -> str:
        # return full user name or email
        if not self.first_name and not self.last_name:
            return self.email

        return self.first_name + " " + self.last_name

        
    def has_perm(self, perm, obj = None) -> bool:
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label) -> bool:
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



    @classmethod
    def bind_friends(cls, user_1:object, user_2:object, *args, **kwargs) -> None:
        user_1.friends.add(user_2)
        user_2.friends.add(user_1)

        user_1.save()
        user_2.save()
        return None


    @classmethod
    def bind_friends_and_add_chat(cls, user_1:object, user_2:object, create_chat:bool = True, *args:tuple, **kwargs:dict) -> Chat:
        """
            [HELP DOCS]
                User class method that make friend instances
                and add personal chat to given pair users.

                You can disable personal creation by setting 
                create_chat flag to False (create_chat = False).

                Users have be passed throw user_1 and user_2 args.

                Method return bool variable - created flag.

                if users weren`t be friends it return True, 
                in other case it return False.

        """

        #bind friends
        cls.bind_friends(user_1, user_2)
        
        # add personal chat for given users
        chat:Chat = Chat.objects.create_chat(users = (user_1, user_2))

        # return created flag
        return chat




