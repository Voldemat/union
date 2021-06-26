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
		email:str 		= None,
		first_name:str 	= None,
		last_name:str 	= None,
		birth_date:str 	= None,
		avatar:object 	= None,
		about_me:str 	= None,
		password:str 	= None, 
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


class FriendManager(models.Manager):
	pass


class Friend(models.Model):
	id = models.UUIDField(
		primary_key = True,
		db_index = True,
		default = uuid.uuid4,
		editable = False
	)

	user = models.ForeignKey('User', on_delete = models.CASCADE)

	friend = models.ForeignKey('User', on_delete = models.CASCADE, related_name = "friend_model")

	objects = FriendManager()

	def __str__(self) -> str:
		return f'Friend - {self.friend}'


	def clean(self) -> None:
		if self.user == self.friend:
			raise ValidationError("User objects equal friend object")

		return None

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


	is_active   = models.BooleanField(default = True)
	is_staff    = models.BooleanField(default = False)
	is_admin    = models.BooleanField(default = False)


	objects = UserManager()

	USERNAME_FIELD = 'email'

	def __str__(self) -> str:
		return self.email


	def get_chats(self) -> QuerySet:
		chats:QuerySet = Chat.objects.filter(users__id = str(self.id))
		return chats


	def get_friends(self) -> QuerySet:
		queryset:QuerySet = Friend.objects.filter(user = self)
		return queryset

	def get_friends_chats(self) -> Optional[QuerySet]:
		friends_chats:list = list()
		for user in self.get_friends():
			chat:Optional[Chat] = self.get_friend_chat(user)
			if chat == None:
				chat = Chat.objects.create(users = [self, user])

			friends_chats.append(chat)


		return friends_chats if friends_chats else None

	def get_friend_chat(self, friend:object) -> Optional[Chat]:
		for chat in self.get_chats():
			chat_users:QuerySet = chat.users.all()
			if len(chat_users) == 2 and self in chat_users and friend in chat_users:
				return chat

		return None


	def get_full_name(self) -> str:
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
	def bind_friends(self, user_1:object, user_2:object) -> None:
		friend_instance:Friend = Friend.objects.get_or_create(user = user_1, friend = user_2)
		friend_instance:Friend = Friend.objects.get_or_create(friend = user_1, user = user_2)

		return None





