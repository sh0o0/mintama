from rest_framework import serializers

from accounts.models import Category, Reference
from notes.models import Note, Section


class SectionHeadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = [
            'heading',
        ]


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    sections_count = serializers.SerializerMethodField()
    sections_heading = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'user',
            'title',
            'written_at',
            'sections_count',
            'sections_heading',
        ]

    def get_user(self, instance):
        return instance.user.username

    def get_sections_count(self, instance):
        return instance.note_sections.all().count()

    def get_sections_heading(self, instance):
        queryset = instance.note_sections.all()
        section_serializer = SectionHeadingSerializer(queryset, many=True)
        return section_serializer.data


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = [
            'categories',
            'note',
            'heading',
            'content',
            'references',
        ]