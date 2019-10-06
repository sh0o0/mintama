from rest_framework import serializers

from api.base_serializers import DecideResponseDataModelSerializer
from todos.models import Board, List, Card


class CardSerializer(DecideResponseDataModelSerializer):
    list = serializers.StringRelatedField()

    class Meta:
        model = Card
        fields = [
            'id',
            'list',
            'name',
            'order',
            'detail',
            'moved_at',
            'is_archive',
        ]


class ListSerializer(DecideResponseDataModelSerializer):
    board = serializers.StringRelatedField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = [
            'id',
            'board',
            'name',
            'order',
            'next',
            'auto_switch',
            'switch_time',
            'is_archive',
            'cards',
        ]

    def get_cards(self, instance):
        serializer = CardSerializer(instance.cards.all(), many=True, context=self._context)
        return serializer.data


class BoardSerializer(DecideResponseDataModelSerializer):
    username = serializers.SerializerMethodField()
    lists = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'user',
            'username',
            'name',
            'is_archive',
            'lists',
        ]
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def get_lists(self, instance):
        serializer = ListSerializer(instance.lists.all(), many=True, context=self._context)
        return serializer.data

    def get_username(self, instance):
        return instance.user.username