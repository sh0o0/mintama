import datetime

from rest_framework import serializers
from rest_framework.fields import empty
from notes.models import Note, Section


class SectionSerializer(serializers.ModelSerializer):
    categories_dict = serializers.SerializerMethodField()
    references_dict = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'note',
            'heading',
            'content',
            'categories',
            'categories_dict',
            'references',
            'references_dict',
        ]
        extra_kwargs = {
            'note': {'write_only': True},
            'categories': {'write_only': True},
            'references': {'write_only': True},
        }

    def get_categories_dict(self, instance):
        return [{'id': obj.id, 'name': obj.name} for obj in instance.categories.all()]

    def get_references_dict(self, instance):
        return [{'id': obj.id, 'title': obj.title} for obj in instance.references.all()]


class NoteSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id',
            'user',
            'username',
            'title',
            'written_at',
            'sections',
        ]
        read_only_filed = ['username']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def get_username(self, instance):
        return instance.user.username

    def get_sections(self, instance):
        queryset = instance.note_sections.all()
        section_serializer = SectionSerializer(queryset, many=True)
        return section_serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    days_1 = serializers.SerializerMethodField()
    days_7 = serializers.SerializerMethodField()
    days_16 = serializers.SerializerMethodField()
    days_35 = serializers.SerializerMethodField()
    days_62 = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'days_1',
            'days_7',
            'days_16',
            'days_35',
            'days_62',
        ]

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=None, data=empty, **kwargs)
        self.set_serializer_method_field()

    def extract_fields_days(self):
        fields = self._readable_fields
        fields_days = {}
        for field in fields:
            days = int(field.field_name.split('_')[-1])
            fields_days[field.field_name] = days
        return fields_days

    def extract_diary_notes(self):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time())
        fields_days = self.extract_fields_days()
        diary_notes = {}
        for field_name, days in fields_days.items():
            end_days = days - 1
            start = today - datetime.timedelta(days=days)
            end = today - datetime.timedelta(days=end_days)
            notes = Note.objects.filter(written_at__range=(start, end))
            diary_notes[field_name] = notes

        return diary_notes

    def set_serializer_method_field(self):
        diary_notes = self.extract_diary_notes()
        for name, notes in diary_notes.items():
            method_name = 'get_' + name

            def get_method(self, notes=notes):
                return NoteSerializer(notes, many=True).data

            setattr(self, method_name, get_method)
