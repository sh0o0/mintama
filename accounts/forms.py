from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class CheckUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class CheckPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

    #一般的なパスワードバリデーション
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password', error)
