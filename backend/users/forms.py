from typing import Optional


from django.forms import ModelForm
from django.contrib.auth import get_user_model

from modules.utils import save_list_get


User = get_user_model()
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
            [HELP DOCS]
                UserForm class.

        """
        super(UserForm, self).__init__(*args, **kwargs)
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        """
            [HELP DOCS]
                Save form method.
                This modified save method hash user password
                before saving to db.
                Modify commit to override that method(commit = False). 

        """

        # get password from cleaned_data
        clean_password:Optional[str] = self.cleaned_data.get("password", None)

        # super save with commit = False
        user = super(UserForm, self).save(commit=False)


        # get user from db
        try:
            user_db = User.objects.get(pk = user.pk)

        except User.DoesNotExist:
            user_db = None
        
        print(f'db password - {user_db.password}')
        print(f'clean password - {clean_password}')
        print(f'not user_db.check_password(clean_password) - {not user_db.check_password(clean_password)}')
        print(f'not user_db.password == clean_password - {not user_db.password == clean_password}')
        # if user don`t created yet hash password
        if not user_db:
            # hash user password...
            user.set_password(clean_password)
        elif not user_db.check_password(clean_password) and not user_db.password == clean_password:
            # hash user password...
            user.set_password(clean_password)


        # if that save method is final we save user to db
        if commit:
            user.save()

        return user