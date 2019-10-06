import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Board(models.Model):
    user = models.ForeignKey(
        User,
        related_name='bords',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=50,
    )
    is_archive = models.BooleanField(
        default=False,
    )

    @classmethod
    def create_default_board(cls, user):
        board = cls(user=user, name='デフォルト')
        board.save()
        return board

    def all_switch(self):
        for list in self.lists:
            list.switch_next()

    def all_previous(self):
        for list in self.lists:
            list.switch_previous()

    def __str__(self):
        return self.name


class List(models.Model):
    board = models.ForeignKey(
        Board,
        related_name='lists',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=50,
    )
    order = models.IntegerField()

    next = models.OneToOneField(
        'self',
        related_name='previous',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    auto_switch = models.BooleanField(
        default=False,
    )
    switch_time = models.TimeField(
        default=datetime.time
    )
    is_archive = models.BooleanField(
        default=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_auto_switch:
            self.switch_next()


    @classmethod
    def create_default_lists(cls, board):
        names = ['TODO', 'TODAY', 'COMPLETE', 'EXCEED', 'COMPLETED']
        lists = {}
        for order, name in enumerate(names):
            list = cls(board=board, name=name, order=order)
            list.save()
            lists[name.lower()] = list

        lists['todo'].next = lists['today']
        lists['todo'].save()

        lists['today'].next, lists['today'].auto_switch = lists['exceed'], True
        lists['today'].save()

        lists['complete'].next = lists['completed']
        lists['complete'].save()

        lists['exceed'].next = lists['todo']
        lists['exceed'].save()

        return lists

    def switch_next(self):
        if self.next is None:
            return False

        for card in self.cards.all():
            card.list = self.next
            card.save()

        return True

    def switch_previous(self):
        if self.previous is None:
            return False

        for card in self.cards.all():
            card.list = self.previous
            card.save()

        return True

    @property
    def is_auto_switch(self):
        if self.auto_switch == False:
            return False

        now = datetime.datetime.now()
        for card in self.cards.all():
            if self.self.switch_time == datetime.time():
                point = card.moved_at(hour=0, minute=0, second=0) + datetime.timedelta(days=1)
            else:
                hour = self.switch_time.hour
                minute = self.switch_time.minute
                second = self.switch_time.second
                if card.moved_at.time() < self.switch_time:
                    point = card.moved_at(hour=hour, minute=minute, second=second) + datetime.timedelta(days=1)
                else:
                    point = card.moved_at(hour=hour, minute=minute, second=second)

            if point > now:
                return False

        return True

    def __str__(self):
        return self.name


class Card(models.Model):
    list = models.ForeignKey(
        List,
        related_name='cards',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=50,
    )
    detail = models.CharField(
        max_length=2000,
    )
    order = models.IntegerField()

    moved_at = models.DateTimeField(
        auto_now=True,
    )
    is_archive = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

# class LittleCard(models.Model):
#     pass