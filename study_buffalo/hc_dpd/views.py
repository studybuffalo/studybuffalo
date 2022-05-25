"""View for the Health Canada Drug Product Database app."""
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic

from .models import (
    DPD, OriginalActiveIngredient, OriginalBiosimilar, OriginalCompany,
    OriginalDrugProduct, OriginalForm, OriginalInactiveProduct,
    OriginalPackaging, OriginalPharmaceuticalStandard, OriginalRoute,
    OriginalSchedule, OriginalStatus, OriginalTherapeuticClass,
    OriginalVeterinarySpecies,
)


class DPDList(PermissionRequiredMixin, generic.ListView):
    """View of all the DPD entries."""
    model = DPD
    context_object_name = 'dpd_list'
    permission_required = 'hc_dpd.web_view'


class OriginalActiveIngredientList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalActiveIngredient entries."""
    model = OriginalActiveIngredient
    context_object_name = 'active_ingredient_list'
    permission_required = 'hc_dpd.web_view'


class OriginalBiosimilarList(PermissionRequiredMixin, generic.ListView):
    """View ofa ll the OriginalBiosimilar entries."""
    model = OriginalBiosimilar
    context_object_name = 'biosimilar_list'
    permission_required = 'hc_dpd.web_view'


class OriginalCompanyList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalCompany entries."""
    model = OriginalCompany
    context_object_name = 'company_list'
    permission_required = 'hc_dpd.web_view'


class OriginalDrugProductList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalDrugProduct entries."""
    model = OriginalDrugProduct
    context_object_name = 'drug_product_list'
    permission_required = 'hc_dpd.web_view'


class OriginalFormList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalForm entries."""
    model = OriginalForm
    context_object_name = 'form_list'
    permission_required = 'hc_dpd.web_view'


class OriginalInactiveProductList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalInactiveProduct entries."""
    model = OriginalInactiveProduct
    context_object_name = 'inactive_product_list'
    permission_required = 'hc_dpd.web_view'


class OriginalPackagingList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalPackaging entries."""
    model = OriginalPackaging
    context_object_name = 'packaging_list'
    permission_required = 'hc_dpd.web_view'


class OriginalPharmaceuticalStandardList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalPharmaceuticalStandard entries."""
    model = OriginalPharmaceuticalStandard
    context_object_name = 'pharmaceutical_standard_list'
    permission_required = 'hc_dpd.web_view'


class OriginalRouteList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalRoute entries."""
    model = OriginalRoute
    context_object_name = 'route_list'
    permission_required = 'hc_dpd.web_view'


class OriginalScheduleList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalSchedule entries."""
    model = OriginalSchedule
    context_object_name = 'schedule_list'
    permission_required = 'hc_dpd.web_view'


class OriginalStatusList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalStatus entries."""
    model = OriginalStatus
    context_object_name = 'status_list'
    permission_required = 'hc_dpd.web_view'


class OriginalTherapeuticClassList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalTherapeuticClass entries."""
    model = OriginalTherapeuticClass
    context_object_name = 'therapeutic_class_list'
    permission_required = 'hc_dpd.web_view'


class OriginalVeterinarySpeciesList(PermissionRequiredMixin, generic.ListView):
    """View of all the OriginalVeterinarySpecies entries."""
    model = OriginalVeterinarySpecies
    context_object_name = 'veterinary_species_list'
    permission_required = 'hc_dpd.web_view'
