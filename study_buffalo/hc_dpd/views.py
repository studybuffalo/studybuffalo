"""View for the Health Canada Drug Product Database app."""
from django.views import generic
from .models import (
    DPD, OriginalActiveIngredient, OriginalCompany, OriginalDrugProduct,
    OriginalForm, OriginalInactiveProduct, OriginalPackaging,
    OriginalPharmaceuticalStandard, OriginalRoute, OriginalSchedule,
    OriginalStatus, OriginalTherapeuticClass, OriginalVeterinarySpecies
)


class DPDList(generic.ListView):
    """View of all the DPD entries"""
    model = DPD

    context_object_name = 'dpd_list'


class ActiveIngredientList(generic.ListView):
    """View of all the ActiveIngredients entries"""
    model = OriginalActiveIngredient

    context_object_name = 'active_ingredient_list'


class CompanyList(generic.ListView):
    """View of all the Companies entries"""
    model = OriginalCompany

    context_object_name = 'company_list'


class DrugProductList(generic.ListView):
    """View of all the DrugProduct entries"""
    model = OriginalDrugProduct

    context_object_name = 'drug_product_list'


class FormList(generic.ListView):
    """View of all the Form entries"""
    model = OriginalForm

    context_object_name = 'form_list'


class InactiveProductList(generic.ListView):
    """View of all the InactiveProducts entries"""
    model = OriginalInactiveProduct

    context_object_name = 'inactive_product_list'


class PackagingList(generic.ListView):
    """View of all the Packaging entries"""
    model = OriginalPackaging

    context_object_name = 'packaging_list'


class PharmaceuticalStandardList(generic.ListView):
    """View of all the PharmaceuticalStandard entries"""
    model = OriginalPharmaceuticalStandard

    context_object_name = 'pharmaceutical_standard_list'


class RouteList(generic.ListView):
    """View of all the Route entries"""
    model = OriginalRoute

    context_object_name = 'route_list'


class ScheduleList(generic.ListView):
    """View of all the Schedule entries"""
    model = OriginalSchedule

    context_object_name = 'schedule_list'


class StatusList(generic.ListView):
    """View of all the Status entries"""
    model = OriginalStatus

    context_object_name = 'status_list'


class TherapeuticClassList(generic.ListView):
    """View of all the TherapeuticClass entries"""
    model = OriginalTherapeuticClass

    context_object_name = 'therapeutic_class_list'


class VeterinarySpeciesList(generic.ListView):
    """View of all the VeterinarySpecies entries"""
    model = OriginalVeterinarySpecies

    context_object_name = 'veterinary_species_list'
