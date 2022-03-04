"""Admin configuration for the Drug Price Calculator application."""
from django.contrib import admin

from . import models


class ClientsInlineAdmin(admin.TabularInline):
    """Inline admin for Clients."""
    model = models.Clients


class CoverageCriteriaInlineAdmin(admin.TabularInline):
    """Inline admin for Coverage Criteria."""
    model = models.CoverageCriteria
    extra = 1


class SpecialInlineAdmin(admin.TabularInline):
    """Inline admin for Special Authorizations."""
    model = models.Price.special_authorizations.through
    extra = 1


@admin.register(models.Drug)
class DrugAdmin(admin.ModelAdmin):
    """Admin for the Drug (and related) models."""
    model = models.Drug

    list_display = ('din', 'brand_name', 'generic_name', 'strength', 'dosage_form')
    ordering = ('generic_name', 'strength', 'dosage_form')
    search_fields = ('din', 'brand_name', 'generic_name')

    fields = (
        'din', 'brand_name', 'strength', 'route', 'dosage_form',
        'generic_name', 'manufacturer', 'schedule', 'atc', 'ptc',
        'generic_product',
    )


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    """Admin for the Price (and related) models."""
    model = models.Price

    list_display = ('drug', 'abc_id', 'unit_price', 'lca_price', 'mac_price')
    ordering = ('abc_id',)
    search_fields = ('drug__brand_name', 'drug__generic_name', 'abc_id')

    fields = (
        'drug', 'abc_id', 'date_listed', 'unit_price', 'lca_price', 'mac_price',
        'mac_text', 'unit_issue', 'interchangeable', 'coverage_status',
    )
    inlines = (ClientsInlineAdmin, CoverageCriteriaInlineAdmin, SpecialInlineAdmin)


@admin.register(models.ATC)
class ATCAdmin(admin.ModelAdmin):
    """Admin for the ATC model."""
    model = models.ATC

    list_display = ('id', 'atc_1', 'atc_2', 'atc_3', 'atc_4', 'atc_5')
    ordering = ('id',)
    search_fields = (
        'atc_1', 'atc_1_text', 'atc_2', 'atc_2_text',
        'atc_3', 'atc_3_text', 'atc_4', 'atc_4_text',
        'atc_5', 'atc_5_text'
    )

    fields = (
        'id', 'atc_1', 'atc_1_text',
        'atc_2', 'atc_2_text', 'atc_3', 'atc_3_text',
        'atc_4', 'atc_4_text', 'atc_5', 'atc_5_text'
    )


@admin.register(models.PTC)
class PTCAdmin(admin.ModelAdmin):
    """Admin for the PTC model."""
    model = models.PTC

    list_display = ('id', 'ptc_1', 'ptc_2', 'ptc_3', 'ptc_4')
    ordering = ('id',)
    search_fields = (
        'ptc_1', 'ptc_1_text', 'ptc_2', 'ptc_2_text',
        'ptc_3', 'ptc_3_text', 'ptc_4', 'ptc_4_text',
    )

    fields = (
        'id', 'ptc_1', 'ptc_1_text', 'ptc_2', 'ptc_2_text',
        'ptc_3', 'ptc_3_text', 'ptc_4', 'ptc_4_text',
    )


@admin.register(models.SpecialAuthorization)
class SpecialAuthorizationAdmin(admin.ModelAdmin):
    """Admin for the PTC model."""
    model = models.SpecialAuthorization

    list_display = ('file_name', 'pdf_title')
    ordering = ('pdf_title',)

    fields = ('file_name', 'pdf_title')


@admin.register(models.SubsBSRF)
class SubsBSRFAdmin(admin.ModelAdmin):
    """Admin for the BSRF substitution model."""
    model = models.SubsBSRF

    list_display = ('original', 'brand_name', 'strength', 'route', 'dosage_form')
    ordering = ('brand_name', 'route', 'dosage_form', 'strength')

    fields = ('original', 'brand_name', 'strength', 'route', 'dosage_form')


@admin.register(models.SubsGeneric)
class SubsGenericAdmin(admin.ModelAdmin):
    """Admin for the generic substitution model."""
    model = models.SubsGeneric

    list_display = ('original', 'correction')
    ordering = ('original', 'correction')

    fields = ('original', 'correction')


@admin.register(models.SubsManufacturer)
class SubsManufacturerAdmin(admin.ModelAdmin):
    """Admin for the manufacturer substitution model."""
    model = models.SubsManufacturer

    list_display = ('original', 'correction')
    ordering = ('original', 'correction')

    fields = ('original', 'correction')


@admin.register(models.SubsUnit)
class SubsUnitAdmin(admin.ModelAdmin):
    """Admin for the unit substitution model."""
    model = models.SubsUnit

    list_display = ('original', 'correction')
    ordering = ('original', 'correction')

    fields = ('original', 'correction')


@admin.register(models.PendBSRF)
class PendBSRFAdmin(admin.ModelAdmin):
    """Admin for the pending BSRF substitution model."""
    model = models.PendBSRF

    list_display = ('original', 'brand_name', 'strength', 'route', 'dosage_form')
    ordering = ('brand_name', 'route', 'dosage_form', 'strength')

    fields = ('original', 'brand_name', 'strength', 'route', 'dosage_form')


@admin.register(models.PendGeneric)
class PendGenericAdmin(admin.ModelAdmin):
    """Admin for the pending generic substitution model."""
    model = models.PendGeneric

    list_display = ('original', 'correction')
    ordering = ('original', 'correction')

    fields = ('original', 'correction')


@admin.register(models.PendManufacturer)
class PendManufacturerAdmin(admin.ModelAdmin):
    """Admin for the pending manufacturer substitution model."""
    model = models.PendManufacturer

    list_display = ('original', 'correction')
    ordering = ('original', 'correction')

    fields = ('original', 'correction')
