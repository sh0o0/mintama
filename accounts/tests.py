import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import resolve

from .models import User
from .views import LoginOrSignupView, SignupView, HomeView

EMAIL = 'darekanoemail@mail.com'


#model
class TestUser(TestCase):

    def test_email_none(self):
        user = User(username='test', email=None)
        with self.assertRaises(IntegrityError):
            user.save()

    def test_unique_username(self):
        name = 'unique'
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
        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(User.objects.all()), 1)

    def test_cannot_register_username_exceed_max_length(self):
        username = 'a' * 151
        password = 'test_password!'
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}
        err = {'username': ['この値は 150 文字以下でなければなりません( 151 文字になっています)。']}

        res = self.client.post(self.url, data)
        content = json.loads(res.content)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(content, err)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=username)

    def test_cannot_register_username_nothing(self):
        username = ''
        password = 'test_password!'
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}

        res = self.client.post(self.url, data)
        user_num = len(User.objects.all())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(user_num, 0)

    def test_cannot_register_email_nothing(self):
        username = 'test'
        password = 'test_password!'
        data = {'username': username, 'email': '', 'password1': password, 'password2': password}

        res = self.client.post(self.url, data)
        user_num = len(User.objects.all())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(user_num, 0)

    def test_cannot_register_password_nothing(self):
        username = 'test'
        password = ''
        data = {'username': username, 'email': '', 'password1': password, 'password2': password}

        res = self.client.post(self.url, data)
        user_num = len(User.objects.all())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(user_num, 0)


class TestLoginView(TestCase):
    url = '/login/'

    def test_get_home_yet_login(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)

    def test_can_login(self):
        username = 'test'
        password = 'test_password!'
        data = {'username': username, 'password': password}

        user = User(username=username, email=EMAIL)
        user.set_password(password)
        user.save()
        authenticate(username=username, password=password)

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, 200)

    def test_cannot_login_not_user(self):
        username = 'test_login'
        password = 'test_password!'

        res = self.client.post(self.url, username=username, password=password)
        self.assertEqual(res.status_code, 401)


class TestLogout(TestCase):
    url = '/logout/'

    def test_can_logout(self):
        username = 'test'
        password = 'test_password!'
        data = {'username': username, 'email': EMAIL, 'password1': password, 'password2': password}

        self.client.post('/signup/', data)

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        self.client.get(self.url)
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)


class TestHomeView(TestCase):
    url = '/'

    def test_url_resolves_to_home_view(self):
        resolved_view = resolve(self.url)
        resolved_func_name = resolved_view.func.__name__
        self.assertEqual(resolved_func_name, HomeView.as_view().__name__)
