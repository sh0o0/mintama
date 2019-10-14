import logging

from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as filters

from accounts.models import Category, Reference
from api.permissions import DetailIsAdminOrWriteOwnOnly
from notes.models import Note, Section
from .serializers import NoteSerializer, SectionSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class NoteFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    written_at = filters.DateFilter(field_name='written_at', lookup_expr='date')
    order_by = filters.OrderingFilter(
        fields=[
            ('written_at', 'written_at')
        ]
    )
    squeeze = filters.NumberFilter(field_name='squeeze', method='get_squeeze')

    def get_squeeze(self, queryset, name, value):
        return queryset.all()[:value]

    class Meta:
        model = Note
        fields = [
            'title',
            'written_at',
            'squeeze',
            'order_by',
        ]


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]
    filter_class = NoteFilter

    def handle_exception(self, exc):
        return super().handle_exception(exc)

    def list(self, request, *args, **kwargs):
        username = kwargs.get('username', None)

        if username:
            user = get_object_or_404(User, username=username)
            queryset = self.filter_queryset(self.queryset.filter(user=user))
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        pk = kwargs.get('pk', None)
        # if not pk:
        #     self.list(request, *args, **kwargs)

        user = get_object_or_404(User, username=username)
        instance = get_object_or_404(Note, id=pk, user=user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop('partial', False)
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            sections_data = request.data.pop('sections', None)
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            sections_data = request.data.pop('sections', None)

        note_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        note_serializer.is_valid(raise_exception=True)
        note = note_serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        Section.objects.filter(note=note).delete()
        if sections_data:
            for section_data in sections_data:
                print(section_data)
                section_data['categories'] = [category['id'] for category in section_data['categories_dict']]
                section_data['references'] = [reference['id'] for reference in section_data['references_dict']]
                section_data['note'] = note.id

            sections_serializer = SectionSerializer(data=sections_data, many=True)
            sections_serializer.is_valid(raise_exception=True)
            sections_serializer.save()

        return Response(note_serializer.data)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            sections_data = request.data.pop('sections', None)
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            sections_data = request.data.pop('sections', None)

        note_serializer = self.get_serializer(data=request.data)
        note_serializer.is_valid(raise_exception=True)
        note = note_serializer.save()

        if sections_data:
            for section_data in sections_data:
                section_data['categories'] = [category['id'] for category in section_data['categories_dict']]
                section_data['references'] = [reference['id'] for reference in section_data['references_dict']]
                section_data['note'] = note.id

            sections_serializer = SectionSerializer(data=sections_data, many=True)
            sections_serializer.is_valid(raise_exception=True)
            sections_serializer.save()

        headers = self.get_success_headers(note_serializer.data)
        return Response(note_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]