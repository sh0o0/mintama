import logging

from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from api.permissions import DetailIsAdminOrWriteOwnOnly
from helper.viewsets import add_user_id_to_request_data
from todos.models import Board, List, Card
from .serializers import BoardSerializer, ListSerializer, CardSerializer

logger = logging.getLogger(__name__)


class ListFilter(filters.FilterSet):
    order_by = filters.OrderingFilter(
        fields=[
            ('order', 'order')
        ]
    )

    class Meta:
        model = List
        fields = [
            'order_by'
        ]


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]

    @action(methods=['post'], detail=True)
    def default(self, request, *args, **kwargs):
        board = Board.create_default_board(request.user)
        List.create_default_lists(board)
        serializer = self.get_serializer(board)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=False, url_path='auto_switch/true')
    def all_auto_switch_true(self, request, *args, **kwargs):
        instance = self.get_object()
        for list in instance.lists:
            list.auto_switch = True
            list.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=False, url_path='auto_switch/false')
    def all_auto_switch_false(self, request, *args, **kwargs):
        instance = self.get_object()
        for list in instance.lists:
            list.auto_switch = False
            list.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @add_user_id_to_request_data
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]
    filter_class = ListFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=True)
    def next(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.switch_next()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=True)
    def previous(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.switch_previous()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=False, url_path='auto_switch/true')
    def auto_switch_true(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.auto_switch = True
        instance.save()

        serializer = BoardSerializer(instance)
        return Response(serializer.data)

    @action(methods=['put', 'patch'], detail=False, url_path='auto_switch/false')
    def auto_switch_false(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.auto_switch = False
        instance.save()

        serializer = BoardSerializer(instance)
        return Response(serializer.data)


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]