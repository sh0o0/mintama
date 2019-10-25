from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

User = get_user_model()


#decorator
def add_user_id_to_request_data(func):
    def wrapper(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = False
        else:
            request.data['user'] = request.user.id
        return func(self, request, *args, **kwargs)
    return wrapper


def list_from_username(func):
    def wrapper(self, request, *args, **kwargs):
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
    return wrapper
