import json

from django.test import TestCase
from django.db.utils import IntegrityError
from django.shortcuts import resolve_url
from django.urls import reverse_lazy, resolve
from django.core.exceptions import ObjectDoesNotExist

from .models import Category, User, Reference, Portfolio
from .views import LoginOrSignupView, SignupView, LoginView, LogoutView, check_username, check_password

EMAIL = 'darekanoemail@mail.com'


#model
class TestUser(TestCase):

    def test_email_none(self):
        user = User(username='test', email=None)
        with self.assertRaises(IntegrityError):
            user.save()

    def test_same_username(self):
        name = 'a'
        user1 = User(username=name, email=EMAIL)
        user2 = User(username=name, email=EMAIL)
        with self.assertRaises(IntegrityError):
            user1.save()
            user2.save()

#view
class TestLoginOrSignupView(TestCase):
    url = '/login-or-signup/'

    def test_url_resolves_to_login_or_signup_view(self):
        resolved_view = resolve(self.url)
        resolved_func_name = resolved_view.func.__name__
        self.assertEqual(resolved_func_name, LoginOrSignupView.as_view().__name__)


class TestSignupView(TestCase):
    url = '/signup/'

    def test_url_resolves_to_signup_view(self):
        resolved_view = resolve(self.url)
        resolved_func_name = resolved_view.func.__name__
        self.assertEqual(resolved_func_name, SignupView.as_view().__name__)

    def test_can_register_user(self):
        username = 'test'
        password = 'test_password!'
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}
        self.client.post(self.url, data)
        self.assertEqual(len(User.objects.all()), 1)

    def test_cannot_register_username_exceed_max_length(self):
        username = 'a' * 151
        password = 'test_password!'
        err = {'username': ['この値は 150 文字以下でなければなりません( 151 文字になっています)。']}
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}

        response = self.client.post(self.url, data)
        response_content = json.loads(response.content)

        self.assertEqual(response_content, err)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=username)

    def test_cannot_register_username_nothing(self):
        username = ''
        password = 'test_password!'
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}
        self.client.post(self.url, data)
        user_num = len(User.objects.all())
        self.assertEqual(user_num, 0)

    def test_cannot_register_email_nothing(self):
        username = 'test'
        password = 'test_password!'
        data = {'username': username, 'email': '', 'password1': password, 'password2': password}
        self.client.post(self.url, data)
        user_num = len(User.objects.all())
        self.assertEqual(user_num, 0)

    def test_cannot_register_password_nothing(self):
        username = 'test'
        password = ''
        data = {'username': username, 'email': '', 'password1': password, 'password2': password}
        self.client.post(self.url, data)
        user_num = len(User.objects.all())
        self.assertEqual(user_num, 0)