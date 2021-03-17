from django.forms import ModelForm
from django import forms
from .models import Taker


class UserRegisterForm(ModelForm):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = Taker
        fields = ['name', 'email']
