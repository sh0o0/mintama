from rest_framework import serializers

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

