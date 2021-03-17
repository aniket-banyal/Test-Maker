from django.contrib.auth.forms import UserCreationForm
from .models import Maker


class UserRegisterForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Maker
        fields = ['email', 'password1', 'password2']
