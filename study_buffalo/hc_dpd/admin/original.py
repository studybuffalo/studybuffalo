"""Admin settings for the HC DPD Original Models."""
from django.contrib import admin

from hc_dpd import models


@admin.register(models.OriginalActiveIngredient)
class OriginalActiveIngredientAdmin(admin.ModelAdmin):
    """Admin view for the OriginalActiveIngredient model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalBiosimilar)
class OriginalBiosimilarAdmin(admin.ModelAdmin):
    """Admin view for the OriginalBiosimilar model."""
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


@admin.register(models.OriginalCompany)
class OriginalCompanyAdmin(admin.ModelAdmin):
    """Admin view for the OriginalCompany model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalDrugProduct)
class OriginalDrugProductAdmin(admin.ModelAdmin):
    """Admin view for the OriginalDrugProduct model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalForm)
class OriginalFormAdmin(admin.ModelAdmin):
    """Admin view for the OriginalForm model."""
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


@admin.register(models.OriginalInactiveProduct)
class OriginalInactiveProductAdmin(admin.ModelAdmin):
    """Admin view for the OriginalInactiveProduct model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalPackaging)
class OriginalPackagingAdmin(admin.ModelAdmin):
    """Admin view for the OriginalPackaging model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalPharmaceuticalStandard)
class OriginalPharmaceuticalStandardAdmin(admin.ModelAdmin):
    """Admin view for the OriginalPharmaceuticalStandard model."""
    list_display = (
        'drug_code',
        'pharmaceutical_std',
    )
    ordering = ('drug_code',)
    search_fields = (
        'drug_code',
        'pharmaceutical_std',
    )


@admin.register(models.OriginalRoute)
class OriginalRouteAdmin(admin.ModelAdmin):
    """Admin view for the OriginalRoute model."""
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


@admin.register(models.OriginalSchedule)
class OriginalScheduleAdmin(admin.ModelAdmin):
    """Admin view for the OriginalSchedule model."""
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


@admin.register(models.OriginalStatus)
class OriginalStatusAdmin(admin.ModelAdmin):
    """Admin view for the OriginalStatus model."""  # pylint: disable=duplicate-code
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


@admin.register(models.OriginalTherapeuticClass)
class OriginalTherapeuticClassAdmin(admin.ModelAdmin):
    """Admin view for the OriginalTherapeuticClass model."""
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


@admin.register(models.OriginalVeterinarySpecies)
class OriginalVeterinarySpeciesAdmin(admin.ModelAdmin):
    """Admin view for the OriginalVeterinarySpecies model."""
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
