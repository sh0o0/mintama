from django.db import models
from rest_framework import serializers
from django_filters import rest_framework as filter

from .models import User, Category, Portfolio, Reference


class UserFilter(filter.FilterSet):
    icon = filter.CharFilter(field_name='icon', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['icon']


class UserSerializer(serializers.ModelSerializer):
    residence = serializers.SerializerMethodField()
    learning_started_date = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    # icon = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'gender',
            'residence',
            'learning_started_date',
            'crack_level',
            'icon',
            'introduction',
        ]

    def get_introduction(self, instance):
        return instance.introduction if instance.introduction else ''

    def get_residence(self, instance):
        return instance.residence if instance.residence else ''

    def get_learning_started_date(self, instance):
        return instance.learning_started_date if instance.learning_started_date else ''

    # def get_icon(self, instance):
    #     return instance.icon if instance.icon else ''


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = [
            'user',
            'title',
            'evaluation',
            'content',
            'link',
        ]


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = [
            'user',
            'title',
            'content',
            'link',
        ]