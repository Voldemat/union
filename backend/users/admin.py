from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, InviteToken
from users.forms import UserForm
# Register your models here.

class UserAdminModel(admin.ModelAdmin):
    def __init__(self, *args, **kwargs) -> None:
        """
            [HELP DOCS]
                UserAdminModel class that specified
                admin model panel(ex. ordering, list_dispay and et.)
                Also added inline model - Friend.

        """
        super(UserAdminModel, self).__init__(*args, **kwargs)
        return None
    
    form = UserForm
    list_filter = ('last_login','birth_date')
    ordering = ("birth_date", "email", "last_login")
    list_display = (
        "email",
        "first_name",
        "last_name",
        "birth_date",
    )
    search_fields = (
        "email",
        "birth_date",
        "last_login",
        "first_name",
        "last_name"
    )
    list_select_related = True

admin.site.register(User, UserAdminModel)
admin.site.register(InviteToken)