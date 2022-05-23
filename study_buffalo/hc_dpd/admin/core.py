"""Admin settings for the HC DPD Core Models."""
from django.contrib import admin

from hc_dpd import models


class FormattedActiveIngredientInline(admin.TabularInline):
    """Tabular inline for the FormattedActiveIngredient model."""
    model = models.FormattedActiveIngredient
    raw_id_fields = ('drug_code',)


class FormattedBiosimilarInline(admin.TabularInline):
    """Tabular inline for the FormattedBiosimilar model."""
    model = models.FormattedBiosimilar
    raw_id_fields = ('drug_code',)


class FormattedCompanyInline(admin.TabularInline):
    """Tabular inline for the FormattedCompany model."""
    model = models.FormattedCompany
    raw_id_fields = ('drug_code',)


class FormattedDrugProductInline(admin.TabularInline):
    """Tabular inline for the FormattedDrugProduct model."""
    model = models.FormattedDrugProduct
    raw_id_fields = ('drug_code',)


class FormattedFormInline(admin.TabularInline):
    """Tabular inline for the FormattedForm model."""
    model = models.FormattedForm
    raw_id_fields = ('drug_code',)


class FormattedInactiveProductInline(admin.TabularInline):
    """Tabular inline for the FormattedInactiveProduct model."""
    model = models.FormattedInactiveProduct
    raw_id_fields = ('drug_code',)


class FormattedPackagingInline(admin.TabularInline):
    """Tabular inline for the FormattedPackaging model."""
    model = models.FormattedPackaging
    raw_id_fields = ('drug_code',)


class FormattedPharmaceuticalStandardInline(admin.TabularInline):
    """Tabular inline for the FormattedPharmaceuticalStandard model."""
    model = models.FormattedPharmaceuticalStandard
    raw_id_fields = ('drug_code',)


class FormattedRouteInline(admin.TabularInline):
    """Tabular inline for the FormattedRoute model."""
    model = models.FormattedRoute
    raw_id_fields = ('drug_code',)


class FormattedScheduleInline(admin.TabularInline):
    """Tabular inline for the FormattedSchedule model."""
    model = models.FormattedSchedule
    raw_id_fields = ('drug_code',)


class FormattedStatusInline(admin.TabularInline):
    """Tabular inline for the FormattedStatus model."""
    model = models.FormattedStatus
    raw_id_fields = ('drug_code',)


class FormattedTherapeuticClassInline(admin.TabularInline):
    """Tabular inline for the FormattedTherapeuticClass model."""
    model = models.FormattedTherapeuticClass
    raw_id_fields = ('drug_code',)


class FormattedVeterinarySpeciesInline(admin.TabularInline):
    """Tabular inline for the FormattedVeterinarySpecies model."""
    model = models.FormattedVeterinarySpecies
    raw_id_fields = ('drug_code',)


class OriginalActiveIngredientInline(admin.TabularInline):
    """Tabular inline for the OriginalActiveIngredient model."""
    model = models.OriginalActiveIngredient
    raw_id_fields = ('drug_code',)


class OriginalBiosimilarInline(admin.TabularInline):
    """Tabular inline for the OriginalBiosimilar model."""
    model = models.OriginalBiosimilar
    raw_id_fields = ('drug_code',)


class OriginalCompanyInline(admin.TabularInline):
    """Tabular inline for the OriginalCompany model."""
    model = models.OriginalCompany
    raw_id_fields = ('drug_code',)


class OriginalDrugProductInline(admin.TabularInline):
    """Tabular inline for the OriginalDrugProduct model."""
    model = models.OriginalDrugProduct
    raw_id_fields = ('drug_code',)


class OriginalFormInline(admin.TabularInline):
    """Tabular inline for the OriginalForm model."""
    model = models.OriginalForm
    raw_id_fields = ('drug_code',)


class OriginalInactiveProductInline(admin.TabularInline):
    """Tabular inline for the OriginalInactiveProduct model."""
    model = models.OriginalInactiveProduct
    raw_id_fields = ('drug_code',)


class OriginalPackagingInline(admin.TabularInline):
    """Tabular inline for the OriginalPackaging model."""
    model = models.OriginalPackaging
    raw_id_fields = ('drug_code',)


class OriginalPharmaceuticalStandardInline(admin.TabularInline):
    """Tabular inline for the OriginalPharmaceuticalStandard model."""
    model = models.OriginalPharmaceuticalStandard
    raw_id_fields = ('drug_code',)


class OriginalRouteInline(admin.TabularInline):
    """Tabular inline for the OriginalRoute model."""
    model = models.OriginalRoute
    raw_id_fields = ('drug_code',)


class OriginalScheduleInline(admin.TabularInline):
    """Tabular inline for the OriginalSchedule model."""
    model = models.OriginalSchedule
    raw_id_fields = ('drug_code',)


class OriginalStatusInline(admin.TabularInline):
    """Tabular inline for the OriginalStatus model."""
    model = models.OriginalStatus
    raw_id_fields = ('drug_code',)


class OriginalTherapeuticClassInline(admin.TabularInline):
    """Tabular inline for the OriginalTherapeuticClass model."""
    model = models.OriginalTherapeuticClass
    raw_id_fields = ('drug_code',)


class OriginalVeterinarySpeciesInline(admin.TabularInline):
    """Tabular inline for the OriginalVeterinarySpecies model."""
    model = models.OriginalVeterinarySpecies
    raw_id_fields = ('drug_code',)


@admin.register(models.DPD)
class DPDAdmin(admin.ModelAdmin):
    """Admin view for the DPD model."""
    list_display = ('drug_code', 'trade_name')
    ordering = ('drug_code',)
    search_fields = ('drug_code',)
    list_filter = (
        'original_active_ingredient_modified',
        'original_biosimilar_modified',
        'original_company_modified',
        'original_drug_product_modified',
        'original_form_modified',
        'original_inactive_product_modified',
        'original_packaging_modified',
        'original_pharmaceutical_standard_modified',
        'original_route_modified',
        'original_schedule_modified',
        'original_status_modified',
        'original_therapeutic_class_modified',
        'original_veterinary_species_modified',
    )
    inlines = (
        FormattedActiveIngredientInline, OriginalActiveIngredientInline,
        FormattedBiosimilarInline, OriginalBiosimilarInline,
        FormattedCompanyInline, OriginalCompanyInline,
        FormattedDrugProductInline, OriginalDrugProductInline,
        FormattedFormInline, OriginalFormInline,
        FormattedInactiveProductInline, OriginalInactiveProductInline,
        FormattedPackagingInline, OriginalPackagingInline,
        FormattedPharmaceuticalStandardInline, OriginalPharmaceuticalStandardInline,
        FormattedRouteInline, OriginalRouteInline,
        FormattedScheduleInline, OriginalScheduleInline,
        FormattedStatusInline, OriginalStatusInline,
        FormattedTherapeuticClassInline, OriginalTherapeuticClassInline,
        FormattedVeterinarySpeciesInline, OriginalVeterinarySpeciesInline
    )

    @admin.display(description='Trade name')
    @classmethod
    def trade_name(cls, obj):
        """Returns the likely trade name for this DPD entry."""
        return obj.original_drug_products.first().brand_name


@admin.register(models.DPDChecksum)
class DPDChecksumAdmin(admin.ModelAdmin):
    """Admin view for the DPDChecksum model."""
    list_display = (
        'drug_code_start',
        'drug_code_step',
        'extract_source',
        'checksum',
        'checksum_date',
    )
    ordering = ('pk',)
    search_fields = (
        'drug_code_start',
        'checksum',
    )
    list_filter = (
        'drug_code_step',
        'extract_source',
        'checksum_date',
    )

