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
    permission_required = 'dpd.web_via'


class ActiveIngredientList(PermissionRequiredMixin, generic.ListView):
    """View of all the ActiveIngredient entries."""
    model = OriginalActiveIngredient
    context_object_name = 'active_ingredient_list'
    permission_required = 'dpd.web_via'


class BiosimilarList(PermissionRequiredMixin, generic.ListView):
    """View ofa ll the Biosimilar entries."""
    model = OriginalBiosimilar
    context_object_name = 'biolsimilar_list'
    permission_required = 'dpd.web_via'


class CompanyList(PermissionRequiredMixin, generic.ListView):
    """View of all the Company entries."""
    model = OriginalCompany
    context_object_name = 'company_list'
    permission_required = 'dpd.web_via'


class DrugProductList(PermissionRequiredMixin, generic.ListView):
    """View of all the DrugProduct entries."""
    model = OriginalDrugProduct
    context_object_name = 'drug_product_list'
    permission_required = 'dpd.web_via'


class FormList(PermissionRequiredMixin, generic.ListView):
    """View of all the Form entries."""
    model = OriginalForm
    context_object_name = 'form_list'
    permission_required = 'dpd.web_via'


class InactiveProductList(PermissionRequiredMixin, generic.ListView):
    """View of all the InactiveProduct entries."""
    model = OriginalInactiveProduct
    context_object_name = 'inactive_product_list'
    permission_required = 'dpd.web_via'


class PackagingList(PermissionRequiredMixin, generic.ListView):
    """View of all the Packaging entries."""
    model = OriginalPackaging
    context_object_name = 'packaging_list'
    permission_required = 'dpd.web_via'


class PharmaceuticalStandardList(PermissionRequiredMixin, generic.ListView):
    """View of all the PharmaceuticalStandard entries."""
    model = OriginalPharmaceuticalStandard
    context_object_name = 'pharmaceutical_standard_list'
    permission_required = 'dpd.web_via'


class RouteList(PermissionRequiredMixin, generic.ListView):
    """View of all the Route entries."""
    model = OriginalRoute
    context_object_name = 'route_list'
    permission_required = 'dpd.web_via'


class ScheduleList(PermissionRequiredMixin, generic.ListView):
    """View of all the Schedule entries."""
    model = OriginalSchedule
    context_object_name = 'schedule_list'
    permission_required = 'dpd.web_via'


class StatusList(PermissionRequiredMixin, generic.ListView):
    """View of all the Status entries."""
    model = OriginalStatus
    context_object_name = 'status_list'
    permission_required = 'dpd.web_via'


class TherapeuticClassList(PermissionRequiredMixin, generic.ListView):
    """View of all the TherapeuticClass entries."""
    model = OriginalTherapeuticClass
    context_object_name = 'therapeutic_class_list'
    permission_required = 'dpd.web_via'


class VeterinarySpeciesList(PermissionRequiredMixin, generic.ListView):
    """View of all the VeterinarySpecies entries."""
    model = OriginalVeterinarySpecies
    context_object_name = 'veterinary_species_list'
    permission_required = 'dpd.web_via'
