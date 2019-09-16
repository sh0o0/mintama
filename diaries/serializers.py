from rest_framework import serializers

from .models import Diary, Section

class DiarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Diary
        fields = [
            'user',
            'title',
        ]


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