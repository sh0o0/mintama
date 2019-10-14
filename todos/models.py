import datetime
import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

logger = logging.getLogger(__name__)


class Board(models.Model):
    user = models.ForeignKey(
        User,
        related_name='bords',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=50,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_switch(auto=True)

    @classmethod
    def create_default_board(cls, user):
        logger.debug('create default board')
        board = cls(user=user, name='デフォルト')
        board.save()
        return board

    def all_switch(self, auto=True):
        logger.debug('all switch')
        intend_save_cards = []
        for list in self.lists.all():
            if auto:
                is_switch = list.is_auto_switch and list.next is not None
            else:
                is_switch = list.auto_switch and list.next is not None

            if is_switch is False:
                continue

            for card in list.cards.all():
                card.list = list.next
                intend_save_cards.append(card)

        for card in intend_save_cards:
            card.save()

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
    order = models.IntegerField(
        default=9999,
    )

    next = models.ForeignKey(
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

    @classmethod
    def create_default_lists(cls, board):
        logger.debug('create default lists')

        todo_list = cls(board=board, name='することすべて', order=1)
        today_list = cls(board=board, name='今日すること', order=2)
        complete_list = cls(board=board, name='今日完了したこと', order=3)
        exceed_list = cls(board=board, name='前からの持ち越し', order=4)
        completed_list = cls(board=board, name='完了したことすべて', order=5)

        todo_list.save()
        today_list.save()
        complete_list.save()
        exceed_list.save()
        completed_list.save()

        todo_list.next = today_list
        today_list.next, today_list.auto_switch = exceed_list, True
        complete_list.next = completed_list
        exceed_list.next = todo_list

        todo_list.save()
        today_list.save()
        complete_list.save()
        exceed_list.save()

    def switch_next(self):
        if self.next is None:
            return

        for card in self.cards.all():
            card.list = self.next
            card.save()

    @property
    def is_auto_switch(self):
        if self.auto_switch == False:
            logger.debug('is auto switch false')
            return False

        if len(self.cards.all()) == 0:
            return False

        now = datetime.datetime.now()
        for card in self.cards.all():
            year = card.moved_at.year
            month = card.moved_at.month
            day = card.moved_at.day
            if self.switch_time == datetime.time():
                # 0:00なら一日増し
                day += 1
                point = datetime.datetime(year=year, month=month, day=day)
            else:
                hour = self.switch_time.hour
                minute = self.switch_time.minute
                point = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
                if card.moved_at.time() < self.switch_time:
                    point += datetime.timedelta(days=1)

            if point > now:
                logger.debug('is auto switch false')
                return False

            logger.debug('is auto switch true')
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
        max_length=300,
    )
    detail = models.CharField(
        max_length=5000,
        blank=True,
    )
    order = models.IntegerField()

    moved_at = models.DateTimeField(
        auto_now=timezone.datetime.now,
    )
    is_archive = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name

# class LittleCard(models.Model):
#     pass