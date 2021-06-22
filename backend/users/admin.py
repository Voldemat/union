from django.contrib import admin

from users.models import User, Friend
# Register your models here.

class FriendAdminInlineModel(admin.TabularInline):
    model = Friend
    fk_name = "user"

class UserAdminModel(admin.ModelAdmin):
    inlines = [
        FriendAdminInlineModel,
    ]

admin.site.register(User, UserAdminModel)
admin.site.register(Friend)