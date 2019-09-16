from rest_framework.permissions import IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return request.methods in SAFE_METHODS or super().has_permission()

