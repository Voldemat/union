from django.urls import path

from rest_framework.routers import SimpleRouter

from api_v1.views import (
    UserViewSet,
    TokenAuthentication,
    ChatViewSet,
    FriendsAPIView,
    InviteTokenViewSet
)

from rest_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Union API V1')

router = SimpleRouter()

router.register('users', UserViewSet, basename = 'users')
router.register('chats', ChatViewSet, basename = 'chats')
router.register('invite-tokens', InviteTokenViewSet, basename = 'invite-tokens')

urlpatterns = [
    path('token-auth/', TokenAuthentication.as_view(), name = 'token-auth'),
    path('docs/', schema_view, name = 'docs'),
    path('friends/', FriendsAPIView.as_view(), name = 'friends')
]

urlpatterns += router.urls