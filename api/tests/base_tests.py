import datetime
import json
import os
from inspect import currentframe

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import settings
from django.contrib.auth import authenticate, login
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url
from django.test import TestCase, LiveServerTestCase
from django.test.client import encode_multipart
from django.urls import reverse_lazy, resolve
from PIL import Image
from rest_framework.test import APIClient
from selenium.webdriver import Chrome


User = get_user_model()
EMAIL = 'darekano@email.jp'


class BaseTestCase(TestCase):
    entries = ''
    username = 'test_user'
    password = 'test_password!'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.public_url = '/api/{}/'.format(cls.entries)
        cls.private_url = '/api/accounts/{}/' + '{}/'.format(cls.entries)
        cls.personal_url = '/api/accounts/{}/' + cls.entries + '/{}/'
        cls.post_url = '/api/accounts/{}/' + '{}/'.format(cls.entries)

    def create_new_user(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def setUp(self):
        user = self.create_new_user(self.username, EMAIL, self.password)
        sub_user = self.create_new_user('sub_user', EMAIL, self.password)

        client = APIClient()
        client.login(username=user.username, password=self.password)

        sub_client = APIClient()
        sub_client.login(username=sub_user.username, password=self.password)

        self.user = user
        self.sub_user = sub_user
        self.rest_client = client
        self.sub_client = sub_client


class BaseTestWeb(TestCase):
    username = 'test_web_user'
    password = 'test_password!'
    email = EMAIL

    scheme = 'http'
    host = settings.ALLOWED_HOSTS[0]
    port = 8000

    @property
    def base_url(self):
        return '{}://{}:{}/'.format(self.scheme, self.host, self.port)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = Chrome(executable_path=os.path.join(settings.BASE_DIR, 'chromedriver.exe'))

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()