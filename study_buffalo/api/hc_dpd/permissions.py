"""Custom permissions for the Health Canada Drug Product Database API."""
from rest_framework.permissions import BasePermission


class HasDPDViewAccess(BasePermission):
    """Only permits view by users with explicit API access."""
    def has_permission(self, request, view):
        return all([
            request.user,
            request.user.has_perm('hc_dpd.api_view')
        ])

class HasDPDEditAccess(BasePermission):
    """Only permits editing by users with explicit API access."""
    def has_permission(self, request, view):
        return all([
            request.user,
            request.user.has_perm('hc_dpd.api_edit')
        ])
