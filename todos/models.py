import datetime
import logging

from django.core.management import settings
from django.db import models
from django.utils import timezone


logger = logging.getLogger(__name__)


class Board(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        intend_save_cards = []
        for list in self.lists.all():
            if auto:
                is_switch = list.is_auto_switch() and list.next is not None
            else:
                is_switch = list.auto_switch and list.next is not None

            if is_switch is False:
                continue

            for card in list.cards.all():
                card.list = list.next
                intend_save_cards.append(card)
        if len(intend_save_cards):
            logger.debug('is next')
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

        todo_list = cls(board=board, name='することすべて', order=1, auto_switch=False)
        today_list = cls(board=board, name='今日すること', order=2, auto_switch=True)
        complete_list = cls(board=board, name='今日完了したこと', order=3, auto_switch=True)
        exceed_list = cls(board=board, name='前からの持ち越し', order=4, auto_switch=True)
        completed_list = cls(board=board, name='完了したことすべて', order=5, auto_switch=False)

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

    def is_auto_switch(self, now=datetime.datetime.now()):
        if self.auto_switch == False:
            logger.debug('false')
            return False

        if len(self.cards.all()) == 0:
            logger.debug('false')
            return False
        
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
                if card.moved_at.time() > self.switch_time:
                    point += datetime.timedelta(days=1)

            if point <= now:
                logger.debug('true point: %s', point)
                return True

        logger.debug('false')
        return False

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
    order = models.IntegerField(
        default=9999
    )

    moved_at = models.DateTimeField(
        auto_now=timezone.datetime.now,
    )
    is_archive = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.name