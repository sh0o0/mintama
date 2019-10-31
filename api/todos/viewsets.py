import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters

from api.permissions import IsAdminOrOwnOnly
from helper.viewsets import add_user_id_to_request_data, get_list_for_username
from todos.models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer

logger = logging.getLogger(__name__)


class ListFilter(filters.FilterSet):
    is_archive = filters.BooleanFilter(field_name='is_archive')
    order_by = filters.OrderingFilter(
        fields=[
            ('order', 'order')
        ]
    )

    class Meta:
        model = List
        fields = [
            'is_archive',
            'order_by',
        ]


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAdminOrOwnOnly]

    @get_list_for_username
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @add_user_id_to_request_data
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def default(self, request, *args, **kwargs):
        board = Board.create_default_board(request.user)
        List.create_default_lists(board)
        serializer = self.get_serializer(board)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=True, url_path='auto_switch/true')
    def all_auto_switch_true(self, request, *args, **kwargs):
        instance = self.get_object()
        for list in instance.lists.all():
            list.auto_switch = True
            list.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=True, url_path='auto_switch/false')
    def all_auto_switch_false(self, request, *args, **kwargs):
        instance = self.get_object()
        for list in instance.lists.all():
            list.auto_switch = False
            list.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(methods=['put'], detail=True)
    def all_cards_next(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.all_switch(auto=False)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def all_lists(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def archive_lists(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAdminOrOwnOnly]
    filter_class = ListFilter

    @action(methods=['put', 'patch'], detail=True)
    def next(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.switch_next()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put'], detail=False)
    def save_order(self, request, *args, **kwargs):
        res_lists = []
        for order, list_data in enumerate(request.data):
            list = List.objects.get(id=list_data['id'])
            list.order = order
            list.save()
            res_lists.append(list)

        serializer = self.get_serializer(res_lists, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def all_cards(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def archive_cards(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminOrOwnOnly]

    @action(methods=['put'], detail=False)
    def save_order(self, request, *args, **kwargs):
        res_cards = []
        list = List.objects.get(id=request.data['id'])
        for order, card_data in enumerate(request.data['cards']):
            card = Card.objects.get(id=card_data['id'])
            card.order, card.list = order, list
            card.save()
            res_cards.append(card)

        serializer = self.get_serializer(res_cards, many=True)
        return Response(serializer.data)