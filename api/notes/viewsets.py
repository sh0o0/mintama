import logging

from django.contrib.auth import get_user_model
from django.http import QueryDict
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.permissions import DetailIsAdminOrWriteOwnOnly, IsAdminOrWriteOwnOnly
from helper.viewsets import get_list_for_username, add_user_id_to_request_data
from notes.models import Note, Section
from .serializers import NoteSerializer, SectionSerializer, ReviewSerializer


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

    @get_list_for_username
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('username', None)
        pk = kwargs.get('pk', None)

        user = get_object_or_404(User, username=username)
        instance = get_object_or_404(Note, id=pk, user=user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def pop_sections_for_request(self, request):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            sections_data = request.data.pop('sections', None)
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
            sections_data = request.data.pop('sections', None)

        return sections_data

    def save_sections(self, parent_note, sections):
        Section.objects.filter(note=parent_note).delete()
        if sections:
            for section_data in sections:
                section_data['categories'] = [category['id'] for category in section_data['categories_dict']]
                section_data['references'] = [reference['id'] for reference in section_data['references_dict']]
                section_data['note'] = parent_note.id

            sections_serializer = SectionSerializer(data=sections, many=True)
            sections_serializer.is_valid(raise_exception=True)
            sections_serializer.save()

    @add_user_id_to_request_data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop('partial', False)
        sections_data = self.pop_sections_for_request(request)

        note_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        note_serializer.is_valid(raise_exception=True)
        note = note_serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        self.save_sections(note, sections_data)
        return Response(note_serializer.data)

    @add_user_id_to_request_data
    def create(self, request, *args, **kwargs):
        sections_data = self.pop_sections_for_request(request)

        note_serializer = self.get_serializer(data=request.data)
        note_serializer.is_valid(raise_exception=True)
        note = note_serializer.save()

        self.save_sections(note, sections_data)
        headers = self.get_success_headers(note_serializer.data)
        return Response(note_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrWriteOwnOnly]

    @get_list_for_username
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('pk', None)
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user.notes.all(), many=True)
        try:
            serializer_data = serializer.data[0]
        except IndexError:
            serializer_data = {}
        return Response(serializer_data)