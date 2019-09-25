import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import QueryDict
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Diary, Section
from .serializers import DiarySerializer, SectionSerializer
from accounts.models import Category, Reference

logger = logging.getLogger(__name__)

User = get_user_model()


class DiaryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='exact')
    written_at = filters.DateFilter(field_name='written_at', lookup_expr='date')
    order_by = filters.OrderingFilter(
        fields=[
            ('title', 'タイトル'),
            ('written_at', 'written_at')
        ]
    )
    squeeze = filters.NumberFilter(field_name='squeeze', method='get_squeeze')

    def get_squeeze(self, queryset, name, value):
        print(queryset)
        print(name)
        print(value)
        return queryset.all()[:value]

    class Meta:
        model = Diary
        fields = [
            'title',
            'written_at',
            'squeeze',
            'order_by',
        ]


class DiaryViewSet(viewsets.ModelViewSet):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [IsAuthenticated]
    filter_class = DiaryFilter

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk == settings.REST_MYSELF_URL:
            logger.debug('api {} retrieve my own info'.format(self.__class__.__name__))
            filtered_user = self.get_queryset().filter(user=request.user.id)
            queryset = self.filter_queryset(filtered_user)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if kwargs['pk'] == settings.REST_MYSELF_URL:
            return self.list(request, *args, **kwargs)

        logger.debug('user api %s', kwargs['pk'])
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug('api {} update my own info'.format(self.__class__))
        if kwargs['pk'] == settings.REST_MYSELF_URL:
            instance = self.request.user
        else:
            instance = self.get_object()

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]