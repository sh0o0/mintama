from django.db import models
from rest_framework import serializers
from django_filters import rest_framework as filter

from .models import User, Category, Portfolio, Reference


class UserFilter(filter.FilterSet):
    icon = filter.CharFilter(field_name='icon', lookup_expr='contains')

    class Meta:
        model = User
        fields = ['icon']


class UserSerializer(serializers.ModelSerializer):
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