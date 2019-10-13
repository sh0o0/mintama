from rest_framework import serializers

from api.base_serializers import DecideResponseDataModelSerializer
from todos.models import Board, List, Card


class CardSerializer(DecideResponseDataModelSerializer):

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
        extra_kwargs = {
            'moved_at': {'read_only': True}
        }


class ListSerializer(DecideResponseDataModelSerializer):
    cards = serializers.SerializerMethodField()
    next_list = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = [
            'id',
            'board',
            'name',
            'order',
            'next',
            'next_list',
            'auto_switch',
            'switch_time',
            'is_archive',
            'cards',
        ]

    def request_path_method(self):
        path = self._context['request'].path
        return path.split('/')[-2]

    def get_cards(self, instance):
        method = self.request_path_method()
        if method == 'all_cards':
            queryset = instance.cards.all().order_by('order')
        elif method == 'archive_cards':
            queryset = instance.cards.all().filter(is_archive=True).order_by('order')
        else:
            queryset = instance.cards.all().filter(is_archive=False).order_by('order')

        serializer = CardSerializer(queryset, many=True, context=self._context)
        return serializer.data

    def get_next_list(self, instance):
        if instance.next:
            return {'id': instance.next.id, 'name': instance.next.name}
        return None


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
            'lists',
        ]
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def request_path_method(self):
        path = self._context['request'].path
        return path.split('/')[-2]

    def get_lists(self, instance):
        method = self.request_path_method()
        if method == 'all_lists':
            queryset = instance.lists.all().order_by('order')
        elif method == 'archive_lists':
            queryset = instance.lists.all().filter(is_archive=True).order_by('order')
        else:
            queryset = instance.lists.all().filter(is_archive=False).order_by('order')

        serializer = ListSerializer(queryset, many=True, context=self._context)
        return serializer.data

    def get_username(self, instance):
        return instance.user.username