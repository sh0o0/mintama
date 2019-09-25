from rest_framework import serializers

from .models import Diary, Section
from accounts.serializers import Category, Reference


class SectionHeadingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = [
            'heading',
        ]


class DiarySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    sections_count = serializers.SerializerMethodField()
    sections_heading = serializers.SerializerMethodField()

    class Meta:
        model = Diary
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
        return instance.diary_sections.all().count()

    def get_sections_heading(self, instance):
        queryset = instance.diary_sections.all()
        section_serializer = SectionHeadingSerializer(queryset, many=True)
        return section_serializer.data


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = [
            'categories',
            'diary',
            'heading',
            'content',
            'references',
        ]