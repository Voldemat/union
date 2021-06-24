from django.forms import ModelForm
from django.contrib.auth import get_user_model

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        """
            [HELP DOCS]
                UserForm class.

        """
        super(UserForm, self).__init__(*args, **kwargs)
    class Meta:
        model = get_user_model()
        fields = '__all__'

    def save(self, commit=True):
        """
            [HELP DOCS]
                Save form method.
                This modified save method hash user password
                before saving to db.
                Modify commit to override that method(commit = False). 

        """
        # super save with commit = False
        user = super(UserForm, self).save(commit=False)

        # check that new password isn`t equal to db password 
        if not user.check_password(self.cleaned_data.get("password", None)):
            # set user password...
            user.set_password(self.cleaned_data.get("password", None)) 


        # if that save method is final we save user to db
        if commit:
            user.save()

        return user