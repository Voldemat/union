from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('api/v1/', include('api_v1.urls')),
    path('chats/', include('chats.urls'))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
