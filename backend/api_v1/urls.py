from django.urls import path

from rest_framework.routers import SimpleRouter

from api_v1.views import (
    UserViewSet,
    TokenAuthentication,
    ChatViewSet,
    check
)

from rest_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Union API V1')

router = SimpleRouter()

router.register('users', UserViewSet, basename = 'users')
router.register('chats', ChatViewSet, basename = 'chats')

urlpatterns = [
    path('token-auth/', TokenAuthentication.as_view(), name = 'token-auth'),
    path('docs/', schema_view, name = 'docs'),
    path('check/', check)
]

urlpatterns += router.urls