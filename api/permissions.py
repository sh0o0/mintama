from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from api.exceptions import UsernameNoneException


User = get_user_model()


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(request, view)


class DetailIsAdminOrWriteOwnOnly(IsAdminUser):

    def has_permission(self, request, view):
        pk = view.kwargs.get('pk', None)
        username = view.kwargs.get('username', None)

        is_safe_method = request.method in SAFE_METHODS
        is_post_method = request.method == 'POST'

        if not username:
            if is_post_method:
                return True
            if is_safe_method:
                if not pk:
                    return True
            raise UsernameNoneException
        else:
            is_admin = super().has_permission(request, view)
            is_own_user = request.user == get_object_or_404(User, username=username)

            if is_safe_method:
                return True
            else:
                return is_admin or is_own_user


class IsAdminOrWriteOwnOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        is_safe_method = request.method in SAFE_METHODS
        try:
            user = User.Objects.get(id=view.kwargs['pk'])
        except:
            user = get_object_or_404(username=view.kwargs['pk'])

        is_own_user = request.user == user
        return is_own_user or is_safe_method or is_admin
