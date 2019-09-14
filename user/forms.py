import datetime

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
        lebels = {
            'username': '名前',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（確認）',
        }


class EntryUserDetailForm(AddStyleClass, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'gender',
            'residence',
            'introduction',
            'learning_started_date',
            'icon',
        ]
        labels = {
            'gender': '性別',
            'residence': '居住地',
            'introduction': '自己紹介',
            'learning_started_date': '勉強を始めた日付',
            'icon': 'アイコン',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year = datetime.date.today().year
        years = [y for y in range(year - 50, year + 1)]
        years.sort(reverse=True)
        self.fields['learning_started_date'].widget = forms.SelectDateWidget(years=years)

    def clean_learning_started_date(self):
        today = datetime.date.today()
        entered_date = self.cleaned_data['learning_started_date']
        if entered_date and entered_date > today:
            raise forms.ValidationError('Cannot enter dates after today.')
        return entered_date


# MainlyLearningFormset = forms.inlineformset_factory(
#     User, MainlyLearning, fields=['category'], extra=5
# )



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

    #Perform general password validation
    #訳：一般的なパスワードバリデーションを行う
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
