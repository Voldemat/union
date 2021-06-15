from django.test import TestCase
from django.contrib.auth import get_user_model

from chats.models import Chat
# Create your tests here

User = get_user_model()

user = User.objects.get(email="viocan2005@gmail.com")

friend = User.objects.get(email = "you@email.com")
class ChatTestCase(TestCase):
    def setUp(self) -> None:
        self.user = user
        self.user.save()

        self.friend = friend
        self.friend.save()

        return None

    def test_create_chat(self) -> None:
        chat:Chat = Chat.objects.create_chat()

        chat.save(users = [self.user, self.friend])

        return None
