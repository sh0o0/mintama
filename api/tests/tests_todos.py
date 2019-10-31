import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from todos.models import Board, List, Card


User = get_user_model()
EMAIL = 'darekano@email.jp'


class TodosTestCase(TestCase):
    entries = ''
    username = 'review'
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

        board_names = ['board1', 'board2', 'board3']
        boards = []
        sub_boards = []
        for name in board_names:
            board = Board(user=user, name=name)
            board.save()
            boards.append(board)

            sub_board = Board(user=sub_user, name='sub_{}'.format(name))
            sub_board.save()
            sub_boards.append(sub_board)

        list_names = ['list1', 'list2', 'list3']
        lists = []
        sub_lists = []
        for name in list_names:
            list = List(board=boards[0], name=name)
            list.save()
            lists.append(list)

            sub_list = List(board=sub_boards[0], name='sub_{}'.format(name))
            sub_list.save()
            sub_lists.append(sub_list)

        card_names = ['card1', 'card2', 'card3']
        cards = []
        sub_cards = []
        for name in card_names:
            card = Card(list=lists[0], name=name)
            card.save()
            cards.append(card)

            sub_card = Card(list=sub_lists[0], name='sub_{}'.format(name))
            sub_card.save()
            sub_cards.append(sub_card)

        self.user = user
        self.sub_user = sub_user
        self.rest_client = client
        self.sub_client = sub_client
        self.boards = boards
        self.sub_boards = sub_boards
        self.lists = lists
        self.sub_lists = sub_lists
        self.cards = cards
        self.sub_cards = sub_cards


class TestBoardViewSet(TodosTestCase):
    entries = 'boards'
    username = 'test_board_viewset'
    password = 'test_password!'

    def test_cannot_get_others(self):
        url = self.public_url
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 400)

        url = self.private_url.format(self.sub_user.username)
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 403)

        url = self.personal_url.format(self.sub_user.username, self.sub_boards[0].id)
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 403)

        url = self.personal_url.format(self.user.username, self.sub_boards[0].id)
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_can_get_own(self):
        url = self.private_url.format(self.user.username)
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 200)

        url = self.personal_url.format(self.user.username, self.boards[0].id)
        res = self.rest_client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_default(self):
        url = self.private_url.format(self.user.username) + 'default/'
        res = self.rest_client.post(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content['name'], 'デフォルト')
        self.assertEqual(len(content['lists']), 5)

        url = self.private_url.format(self.user.username) + '{}/'.format('default')
        res = self.rest_client.post(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(content['name'], 'デフォルト')
        self.assertEqual(len(content['lists']), 5)

    def test_all_auto_switch_false_and_true(self):
        board = Board.create_default_board(self.user)
        List.create_default_lists(board)

        url = self.personal_url.format(self.user.username, board.id) + 'auto_switch/false/'
        res = self.rest_client.put(url)
        self.assertEqual(res.status_code, 200)

        board = Board.objects.get(id=board.id)
        for list in board.lists.all():
            self.assertFalse(list.auto_switch)

        url = self.personal_url.format(self.user.username, board.id) + 'auto_switch/true/'
        res = self.rest_client.put(url)
        self.assertEqual(res.status_code, 200)

        board = Board.objects.get(id=board.id)
        for list in board.lists.all():
            self.assertTrue(list.auto_switch)

    def test_all_cards_next(self):
        self.lists[0].auto_switch = True
        self.lists[0].next = self.lists[1]
        self.lists[0].save()

        url = self.personal_url.format(self.user.username, self.boards[0].id) + 'all_cards_next/'
        res = self.rest_client.put(url)
        self.assertEqual(res.status_code, 200)

        list1 = List.objects.get(id=self.lists[0].id)
        list2 = List.objects.get(id=self.lists[1].id)
        self.assertEqual(len(list1.cards.all()), 0)
        self.assertEqual(len(list2.cards.all()), 3)

    def test_normal_lists(self):
        self.lists[0].is_archive = True
        self.lists[0].save()

        url = self.personal_url.format(self.user.username, self.boards[0].id)
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content['lists']), 2)

    def test_all_lists(self):
        self.lists[0].is_archive = True
        self.lists[0].save()

        url = self.personal_url.format(self.user.username, self.boards[0].id) + 'all_lists/'
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content['lists']), 3)


class TestListViewSet(TodosTestCase):
    entries = 'lists'
    username = 'test_list_viewset'

    def test_get_normal_cards(self):
        self.cards[0].is_archive = True
        self.cards[0].save()

        url = self.personal_url.format(self.user.username, self.lists[0].id)
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content['cards']), 2)

    def test_get_all_cards(self):
        self.cards[0].is_archive = True
        self.cards[0].save()

        url = self.personal_url.format(self.user.username, self.lists[0].id) + 'all_cards/'
        res = self.rest_client.get(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content['cards']), 3)

    def test_next_action(self):
        self.lists[0].auto_switch = True
        self.lists[0].next = self.lists[1]
        self.lists[0].save()

        url = self.personal_url.format(self.user.username, self.lists[0].id) + 'next/'
        res = self.rest_client.put(url)
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content['cards']), 0)
        self.assertEqual(len(content['cards']), 0)

        list1 = List.objects.get(id=self.lists[0].id)
        list2 = List.objects.get(id=self.lists[1].id)
        self.assertEqual(len(list1.cards.all()), 0)
        self.assertEqual(len(list2.cards.all()), 3)

    def test_list_save_order(self):
        data = [{'id': list.id} for list in reversed(self.lists)]

        url = self.private_url.format(self.user.username) + 'save_order/'
        res = self.rest_client.put(url, data, format='json')
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content), 3)
        order = 2
        for list in self.boards[0].lists.all():
            self.assertEqual(list.order, order)
            order -= 1


class TestCardViewSet(TodosTestCase):
    entries = 'cards'
    username = 'test_card_viewset'

    def test_list_save_order(self):
        list_id = self.lists[0].id
        cards_id = [{'id': card.id} for card in reversed(self.cards)]
        data = {'id': list_id, 'cards': cards_id}

        url = self.private_url.format(self.user.username) + 'save_order/'
        res = self.rest_client.put(url, data, format='json')
        content = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(content), 3)
        order = 2
        for card in self.lists[0].cards.all():
            self.assertEqual(card.order, order)
            order -= 1
