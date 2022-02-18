from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Permission for owner
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
