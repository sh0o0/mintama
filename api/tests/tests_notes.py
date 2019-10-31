import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from notes.models import Note


User = get_user_model()
EMAIL = 'darekano@email.jp'


class TestNoteViewSet(TestCase):
    public_url = '/api/notes/'
    private_url = '/api/accounts/{}/notes/'
    personal_url = '/api/accounts/{}/notes/{}/'
    post_url = '/api/accounts/{}/notes/'
    username = 'testreferenceuser'
    password = 'test_password!'

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

        notes_name = ['note1', 'note2', 'note3']
        notes = []
        for note_name in notes_name:
            note = Note(user=user, title=note_name)
            note.save()
            notes.append(note)

        self.user = user
        self.sub_user = sub_user
        self.rest_client = client
        self.sub_client = sub_client
        self.notes = notes

    def test_public_list(self):
        res = self.rest_client.get(self.public_url)
        content = json.loads(res.content)
        self.assertEqual(content['count'], 3)

    def test_private_list(self):
        res = self.rest_client.get(self.private_url.format(self.user.username))
        content = json.loads(res.content)
        self.assertEqual(content['count'], 3)

        res = self.rest_client.get(self.private_url.format(self.sub_user.username))
        content = json.loads(res.content)
        self.assertEqual(content['count'], 0)

    def test_retrieve(self):
        url = self.personal_url.format(self.user.username, self.notes[0].id)
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(content['title'], self.notes[0].title)

    def test_can_update_own(self):
        url = self.personal_url.format(self.user.username, self.notes[0].id)
        data = {'title': 'patch title'}
        res = self.rest_client.patch(url, data)
        content = json.loads(res.content)
        self.assertEqual(content['title'], data['title'])

    def test_cannot_update_others(self):
        url = self.personal_url.format(self.sub_user.username, self.notes[0].id)
        data = {'title': 'patch title'}
        res = self.rest_client.patch(url, data)
        self.assertEqual(res.status_code, 403)

    def test_can_create_note(self):
        url = self.post_url.format(self.user.username)
        title = 'create note'
        data = {'title': title}
        res = self.rest_client.post(url, data)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(content['username'], self.user.username)
        self.assertEqual(content['title'], title)


class TestReviewViewSet(TestCase):
    entries = 'reviews'
    public_url = '/api/{}/'.format(entries)
    private_url = '/api/accounts/{}/' + '{}/'.format(entries)
    personal_url = '/api/accounts/{}/' + entries + '/{}/'
    post_url = '/api/accounts/{}/' + '{}/'.format(entries)
    username = 'review'
    password = 'test_password!'

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

    def test_public_list(self):
        res = self.rest_client.get(self.public_url)
        content = json.loads(res.content)
        self.assertEqual(content['count'], 5)

    def test_list(self):
        days_ago_1 = datetime.datetime.now() - datetime.timedelta(days=1)
        days_ago_7 = datetime.datetime.now() - datetime.timedelta(days=7)
        days_ago_16 = datetime.datetime.now() - datetime.timedelta(days=16)
        title1 = 'note1'
        title2 = 'note2'
        title3 = 'note3'
        note1 = Note(user=self.user, title=title1, written_at=days_ago_1)
        note2 = Note(user=self.user, title=title2, written_at=days_ago_7)
        note3 = Note(user=self.user, title=title3, written_at=days_ago_16)
        note1.save()
        note2.save()
        note3.save()

        url = self.public_url + '{}/'.format(self.user.username)
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(content['days_1'][0]['title'], title1)
        self.assertEqual(content['days_7'][0]['title'], title2)
        self.assertEqual(content['days_16'][0]['title'], title3)
        self.assertEqual(content['days_35'], [])
        self.assertEqual(content['days_62'], [])
