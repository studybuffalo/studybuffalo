"""Admin settings for the HC DPD Formatted Models."""
from django.contrib import admin

from hc_dpd import models


@admin.register(models.FormattedActiveIngredient)
class FormattedActiveIngredientAdmin(admin.ModelAdmin):
    """Admin view for the FormattedActiveIngredient model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'active_ingredient_code',
        'ingredient',
        'strength',
        'strength_unit',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'active_ingredient_code',
        'ingredient',
        'notes',
        'ingredient_f',
    )
    list_filter = ('ingredient_supplied_ind', 'base')


@admin.register(models.FormattedBiosimilar)
class FormattedBiosimilarAdmin(admin.ModelAdmin):
    """Admin view for the FormattedBiosimilar model."""
    list_display = (
        'drug_code',
        'biosimilar_code',
        'biosimilar_type',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'biosimilar_code',
        'biosimilar_type',
        'biosimilar_type_f',
    )


@admin.register(models.FormattedCompany)
class FormattedCompanyAdmin(admin.ModelAdmin):
    """Admin view for the FormattedCompany model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'mfr_code',
        'company_code',
        'company_name',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'mfr_code',
        'company_code',
        'company_name',
        'suite_number',
        'street_name',
        'city_name',
        'province',
        'country',
        'postal_code',
        'post_office_box',
        'province_f',
        'country_f',
    )
    list_filter = (
        'company_type',
        'address_mailing_flag',
        'address_billing_flag',
        'address_notification_flag',
        'address_other',
    )


@admin.register(models.FormattedDrugProduct)
class FormattedDrugProductAdmin(admin.ModelAdmin):
    """Admin view for the FormattedDrugProduct model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'product_categorization',
        'drug_identification_number',
        'brand_name',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'product_categorization',
        'class_e',
        'drug_identification_number',
        'brand_name',
        'accession_number',
        'class_f',
        'brand_name_f',
    )
    list_filter = (
        'pediatric_flag',
        'number_of_ais',
        'last_update_date',
    )


@admin.register(models.FormattedForm)
class FormattedFormAdmin(admin.ModelAdmin):
    """Admin view for the FormattedForm model."""
    list_display = (
        'drug_code',
        'pharmaceutical_form',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'pharm_form_code',
        'pharmaceutical_form',
        'pharmaceutical_form_f',
    )


@admin.register(models.FormattedInactiveProduct)
class FormattedInactiveProductAdmin(admin.ModelAdmin):
    """Admin view for the FormattedInactiveProduct model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'drug_identification_number',
        'brand_name',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'drug_identification_number',
        'brand_name',
    )
    list_filter = (
        'history_date',
    )


@admin.register(models.FormattedPackaging)
class FormattedPackagingAdmin(admin.ModelAdmin):
    """Admin view for the FormattedPackaging model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'upc',
        'package_size',
        'package_size_unit',
        'product_information',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'upc',
        'package_size_unit',
        'package_type',
        'package_size',
        'product_information',
        'package_size_unit_f',
        'package_type_f',
    )


@admin.register(models.FormattedPharmaceuticalStandard)
class FormattedPharmaceuticalStandardAdmin(admin.ModelAdmin):
    """Admin view for the FormattedPharmaceuticalStandard model."""
    list_display = (
        'drug_code',
        'pharmaceutical_std',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'pharmaceutical_std',
    )


@admin.register(models.FormattedRoute)
class FormattedRouteAdmin(admin.ModelAdmin):
    """Admin view for the FormattedRoute model."""
    list_display = (
        'drug_code',
        'route_of_administration_code',
        'route_of_administration',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'route_of_administration_code',
        'route_of_administration',
        'route_of_administration_f',
    )


@admin.register(models.FormattedSchedule)
class FormattedScheduleAdmin(admin.ModelAdmin):
    """Admin view for the FormattedSchedule model."""
    list_display = (
        'drug_code',
        'schedule',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'schedule',
        'schedule_f',
    )


@admin.register(models.FormattedStatus)
class FormattedStatusAdmin(admin.ModelAdmin):
    """Admin view for the FormattedStatus model."""  # pylint: disable=duplicate-code
    list_display = (
        'drug_code',
        'status',
        'lot_number',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'status',
        'status_f',
        'lot_number',
    )
    list_filter = (
        'current_status_flag',
        'history_date',
        'expiration_date',
    )


@admin.register(models.FormattedTherapeuticClass)
class FormattedTherapeuticClassAdmin(admin.ModelAdmin):
    """Admin view for the FormattedTherapeuticClass model."""
    list_display = (
        'drug_code',
        'tc_atc_number',
        'tc_atc',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'tc_atc_number',
        'tc_atc,',
        'tc_atc_f',
    )


@admin.register(models.FormattedVeterinarySpecies)
class FormattedVeterinarySpeciesAdmin(admin.ModelAdmin):
    """Admin view for the FormattedVeterinarySpecies model."""
    list_display = (
        'drug_code',
        'vet_species',
        'vet_sub_species',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'vet_species',
        'vet_sub_species',
        'vet_species_f',
    )
