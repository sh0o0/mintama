from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Board, List, Card


User = get_user_model()


class TestBoardModel(TestCase):
    @classmethod
    def setUpClass(cls):
        username = 'test'
        email = 'darekano@email.jp'
        cls.user = User(username=username, email=email)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.user

    def test_can_create_board(self):
        board = Board(user=self.user, name='test')
        board.save()
        board_count = len(Board.objects.all())
        self.assertEqual(board_count, 1)

    def test_create_default_board_method(self):
        board = Board.create_default_board(self.user)
        board_count = len(Board.objects.all())
        self.assertEqual(board_count, 1)
        self.assertEqual(board.user, self.user)
        self.assertEqual(board.name, 'デフォルト')

    def test_all_switch_method(self):
        board = Board(user=self.user, name='test')
        board.save()
        list1 = List(board=board, name='test1', auto_switch=True)
        list2 = List(board=board, name='test2', auto_switch=False)
        list1.save()
        list2.save()
        card = Card.objects.create(list=list1, name='test', order=99)
        card.save()

        list1.next = list2
        list1.save()

        board.all_switch(auto=False)
        card = Card.objects.get(id=card.id)
        self.assertEqual(card.list, list2)


class TestListModel(TestCase):

    @classmethod
    def setUpClass(cls):
        username = 'test'
        email = 'darekano@email.jp'
        cls.user = User(username=username, email=email)
        cls.user.save()

    def setUp(self):
        board = Board(user=self.user, name='test')
        board.save()

        list1 = List(board=board, name='test1', auto_switch=True)
        list2 = List(board=board, name='test2', auto_switch=True)
        list1.save()
        list2.save()

        card = Card(list=list1, name='test', order=99)
        card.save()

        list1.next = list2
        list1.save()

        self.board = board
        self.list1 = list1
        self.list2 = list2
        self.card = card

    def tearDown(self):
        del self.board
        del self.list1
        del self.list2
        del self.card

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        del cls.user

    def test_create_default_lists(self):
        board = Board.create_default_board(self.user)
        List.create_default_lists(board)
        list_count = len(List.objects.all().filter(board=board))
        self.assertEqual(list_count, 5)

    def test_switch_next(self):
        self.assertEqual(self.card.list, self.list1)
        self.list1.switch_next()
        card = Card.objects.get(id=self.card.id)
        self.assertEqual(card.list, self.list2)

    def test_is_auto_swtich_false(self):
        self.list1.auto_switch = False
        self.list1.save()
        self.assertFalse(self.list1.is_auto_switch())
