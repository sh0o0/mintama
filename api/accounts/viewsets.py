import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from accounts.models import Category, Reference, Portfolio
from api.permissions import IsAdminOrReadOnly, DetailIsAdminOrWriteOwnOnly
from helper.viewsets import add_user_id_to_request_data
from .serializers import UserSerializer, CategorySerializer, ReferenceSerializer, PortfolioSerializer


logger = logging.getLogger(__name__)
User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    max_page_size = 10000


class OwnUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(methods=['get'], detail=False)
    def user(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = User.objects.get(id=kwargs['pk'])
        except (ObjectDoesNotExist, ValidationError):
            instance = get_object_or_404(User, username=kwargs['pk'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.request.user

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination


class ReferenceFilter(filters.FilterSet):
    q = filters.CharFilter(field_name='q', method='get_q')

    def create_conditions(self, keywords):
        conditions = None
        for key in keywords:
            if conditions is None:
                conditions = Q(title__icontains=key)
            conditions |= Q(title__icontains=key)
            conditions |= Q(content__icontains=key)
            conditions |= Q(link__icontains=key)
            conditions |= Q(user__username__icontains=key)
        return conditions
    
    def get_q(self, queryset, name, value):
        keywords = value.strip().split()
        conditions = self.create_conditions(keywords)
        queryset = queryset.select_related().filter(conditions)
        return queryset
        
    class Meta:
        model = Reference
        fields = [
            'q'
        ]


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]
    filter_class = ReferenceFilter

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

    @add_user_id_to_request_data
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [DetailIsAdminOrWriteOwnOnly]
