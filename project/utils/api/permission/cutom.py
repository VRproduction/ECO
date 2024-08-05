# permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows access only to admin users for certain endpoints.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True  # Admin users have full access
        return False