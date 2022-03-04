"""Custom permissions for the RDRHC Calendar API."""
from rest_framework.permissions import BasePermission


class HasAPIAccess(BasePermission):
    """Only permits users with explicit API access."""
    def has_permission(self, request, view):
        return all([
            request.user,
            request.user.has_perm('rdrhc_calendar.access_api')
        ])
