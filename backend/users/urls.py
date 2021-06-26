from django.urls import path

from users.views import friend_invite

urlpatterns = [
    path("<uuid:id>", friend_invite, name = 'friends-invite')

]