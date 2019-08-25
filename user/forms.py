from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from .models import User


class AddStyleClass:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs['class'] = 'form-item'


class SignupForm(AddStyleClass, UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class EntryUserDetailForm(AddStyleClass, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'sex',
            'residence',
            'introduction',
            'learning_started_date',
            'icon',
        ]


class LoginForm(AddStyleClass, AuthenticationForm):
    pass


class CheckUsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class CheckPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

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
