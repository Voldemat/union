from django.urls import path

from rest_framework.routers import SimpleRouter

from api_v1.views import UserViewSet, TokenAuthentication

router = SimpleRouter()

router.register('users', UserViewSet, basename = 'users')

urlpatterns = [
    path('token-auth/', TokenAuthentication.as_view(), name = 'token-auth')
]

urlpatterns += router.urls