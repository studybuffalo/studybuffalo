from rest_framework.permissions import BasePermission

class HasDrugPriceCalculatorAPIAccess(BasePermission):
    """Only permits users with explicit API access."""
    def has_permission(self, request, view):
        return all([
            request.user,
            request.user.has_perm('drug_price_calculator.access_api')
        ])
