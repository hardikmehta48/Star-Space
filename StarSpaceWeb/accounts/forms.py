from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ['username','email','password1','password2', 'first_name', 'last_name']
        #                              to confirm password
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'account_handle'
