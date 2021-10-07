from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AuthorOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.author == user:
            return True
        return request.method in SAFE_METHODS
