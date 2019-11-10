import datetime
import json
import os
from inspect import currentframe

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import encode_multipart
from django.urls import resolve
from rest_framework.test import APIClient
from PIL import Image

from accounts.models import Reference
from api.accounts.viewsets import OwnUserViewSet
from todos.models import Board


User = get_user_model()
EMAIL = 'darekano@email.jp'


class TestOwnUserViewSet(TestCase):
    origin_url = '/api/own/'
    username = 'test own user viewset'
    password = 'test_password!'

    @classmethod
    def setUpClass(cls):
        user = User(username=cls.username, email=EMAIL)
        user.set_password(cls.password)
        user.save()

        client = APIClient()
        client.login(username=cls.username, password=cls.password)

        cls.user = user
        cls.rest_client = client

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.user

    def test_resolve_origin_url(self):
        resolved_view = resolve(self.origin_url)
        resolved_func_name = resolved_view.func.__name__
        self.assertEqual(resolved_func_name, OwnUserViewSet.as_view('list').__name__)

    def test_get_user_action(self):
        url = self.origin_url + 'user/'
        res = self.rest_client.get(url)
        res_data = json.loads(res.content)
        self.assertEqual(res_data['username'], self.username)


class TestUserViewSet(TestCase):
    origin_url = '/api/users/'
    username = 'test_user_viewset'
    password = 'test_password!'

    @classmethod
    def setUpClass(cls):
        user = User(username=cls.username, password=cls.password, email=EMAIL)
        user.set_password(cls.password)
        user.save()

        client = APIClient()
        client.login(username=cls.username, password=cls.password)

        test_users = ['user1', 'user2', 'user3']
        for username in test_users:
            test_user = User(username=username, email=EMAIL)
            test_user.save()

        cls.user = user
        cls.rest_client = client

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.user

    def test_list(self):
        res = self.rest_client.get(self.origin_url)
        content = json.loads(res.content)
        self.assertEqual(content['count'], 4)

    def test_retrieve(self):
        url = self.origin_url + self.username + '/'
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(content['username'], self.username)

    def disassemble_var_to_key_value(self, arg):
        names = {id(v): k for k, v in currentframe().f_back.f_locals.items()}
        ret = [names.get(id(arg), None), arg]
        return ret

    def patch_variable_and_return_content(self, url, key, value):
        content = encode_multipart('BoUnDaRyStRiNg', {key: value})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        res = self.rest_client.patch(url, content, content_type=content_type)
        res_content = json.loads(res.content)
        return res_content.get(key, None)

    def test_patch_all_field(self):
        board = Board.objects.create(user=self.user, name='test')
        url = self.origin_url + self.username + '/'

        username = 'test-patch-all-field'
        email = 'siranai@email.com'
        gender = 'male'
        residence = '東京都'
        introduction = 'this is a introduction.'
        crack_level = 2
        learning_started_date = datetime.date(year=2019, month=10, day=20)
        default_board = board.id
        icon = Image.open(os.path.join(settings.BASE_DIR, 'static/mintama/img/mintama-top.png'))
        clear_icon = True

        content_username = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(username))
        content_email = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(email))
        content_gender = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(gender))
        content_residence = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(residence))
        content_crack_level = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(crack_level))
        content_introduction = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(introduction))
        content_learning_started_date = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(learning_started_date))
        content_default_board = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(default_board))
        content_icon = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(icon))

        self.assertEqual(username, content_username)
        self.assertEqual(email, content_email)
        self.assertEqual(gender, content_gender)
        self.assertEqual(residence, content_residence)
        self.assertEqual(crack_level, content_crack_level)
        self.assertEqual(introduction, content_introduction)
        self.assertEqual(learning_started_date.strftime('%Y-%m-%d'), content_learning_started_date)
        self.assertEqual(default_board, content_default_board)
        self.assertIsNotNone(content_icon)
        self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(clear_icon))
        user = User.objects.get(username=username)
        self.assertIsNot(content_icon, user.icon)


class TestOwnUserViewSet(TestCase):
    origin_url = '/api/own/'
    username = 'testuser'
    password = 'test_password!'

    @classmethod
    def setUpClass(cls):
        user = User(username=cls.username, email=EMAIL)
        user.set_password(cls.password)
        user.save()

        client = APIClient()
        client.login(username=cls.username, password=cls.password)

        cls.user = user
        cls.rest_client = client

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.user

    def test_resolve_origin_url(self):
        resolved_view = resolve(self.origin_url)
        resolved_func_name = resolved_view.func.__name__
        self.assertEqual(resolved_func_name, OwnUserViewSet.as_view('list').__name__)

    def test_get_user_action(self):
        url = self.origin_url + 'user/'
        res = self.rest_client.get(url)
        res_data = json.loads(res.content)
        self.assertEqual(res_data['username'], self.username)


class TestReferenceViewSet(TestCase):
    public_url = '/api/references/'
    private_url = '/api/accounts/{}/references/'
    username = 'testreferenceuser'
    password = 'test_password!'

    def create_new_user(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def disassemble_var_to_key_value(self, arg):
        names = {id(v): k for k, v in currentframe().f_back.f_locals.items()}
        ret = [names.get(id(arg), None), arg]
        return ret

    def patch_variable_and_return_content(self, url, key, value):
        content = {key: value}
        res = self.sub_client.patch(url, content)
        res_content = json.loads(res.content)
        return res_content.get(key, None)

    def setUp(self):
        user = self.create_new_user(self.username, EMAIL, self.password)
        sub_user = self.create_new_user('sub_user', EMAIL, self.password)

        references_name = ['reference1', 'reference2', 'reference3']
        references = []
        for reference_name in references_name:
            reference = Reference(user=user, title=reference_name)
            reference.save()
            references.append(reference)

        sub_reference = Reference(user=sub_user, title='sub_reference')
        sub_reference.save()

        client = APIClient()
        client.login(username=user.username, password=self.password)

        sub_client = APIClient()
        sub_client.login(username=sub_user.username, password=self.password)

        self.user = user
        self.rest_client = client
        self.references = references
        self.sub_user = sub_user
        self.sub_client = sub_client
        self.sub_reference = sub_reference

    def test_list(self):
        public_res = self.rest_client.get(self.public_url)
        private_res = self.rest_client.get(self.private_url.format(self.username))
        public_content = json.loads(public_res.content)
        private_content = json.loads(private_res.content)
        self.assertEqual(public_content['count'], 4)
        self.assertEqual(private_content['count'], 3)

    def test_patch_all_field(self):
        url = self.private_url.format(self.sub_user.username) + '{}/'.format(self.sub_reference.id)

        title = 'patch title'
        content = 'contentcontentcontentcontentcontentcontent'
        link = 'http://darekano.link/'

        content_title = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(title))
        content_content = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(content))
        content_link = self.patch_variable_and_return_content(url, *self.disassemble_var_to_key_value(link))

        self.assertEqual(title, content_title)
        self.assertEqual(content, content_content)
        self.assertEqual(link, content_link)

    def test_create(self):
        url = self.private_url.format(self.sub_user.username)
        data = {
            'title': 'new title',
            'content': 'contentcontentcontentcontentcontentcontent',
            'link': 'http://darekano.link/',
        }
        res = self.sub_client.post(url, data)
        content = json.loads(res.content)
        self.assertEqual(data['title'], content['title'])
        self.assertEqual(data['content'], content['content'])
        self.assertEqual(data['link'], content['link'])

    def test_all_column_search(self):
        url = self.public_url + '?q={}'.format('1')
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        print(content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content['count'], 1)