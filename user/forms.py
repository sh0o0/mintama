from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class AddFormClass:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs['class'] = 'form-item'


class RegistrationForm(AddFormClass, UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'icon',
            'password1',
            'password2',
        ]


class LoginForm(AddFormClass, AuthenticationForm):
    pass
