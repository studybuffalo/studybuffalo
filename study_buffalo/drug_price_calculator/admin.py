from django.contrib import admin

from . import models





@admin.register(models.Drug)
class DrugAdmin(admin.ModelAdmin):
    """Admin for the Drug (and related) models."""
    model = models.Drug

    list_display = ('din', 'brand_name', 'generic_name', 'strength', 'dosage_form')
    ordering = ('generic_name', 'strength', 'dosage_form')

class ClientsInlineAdmin(admin.TabularInline):
    model = models.Clients

class CoverageCriteriaInlineAdmin(admin.TabularInline):
    model = models.CoverageCriteria
    extra = 1

class SpecialInlineAdmin(admin.TabularInline):
    model = models.Price.special_authorizations.through
    extra = 1

@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    """Admin for the Price (and related) models."""
    model = models.Price

    list_display = ('drug', 'abc_id', 'unit_price', 'lca_price', 'mac_price')
    ordering = ('abc_id',)

    fields = (
        'drug', 'abc_id', 'date_listed', 'unit_price', 'lca_price', 'mac_price',
        'mac_text', 'unit_issue', 'interchangeable', 'coverage_status',
    )
    inlines = (ClientsInlineAdmin, CoverageCriteriaInlineAdmin, SpecialInlineAdmin)

@admin.register(models.ATC)
class ATCAdmin(admin.ModelAdmin):
    """Admin for the ATC model."""
    model = models.ATC

    list_display = ('id', 'atc_1', 'atc_2', 'atc_3', 'atc_4')
    orders = ('id',)

    fields = (
        'id', 'atc_1', 'atc_1_text', 'atc_2', 'atc_2_text',
        'atc_3', 'atc_3_text', 'atc_4', 'atc_4_text',
    )

@admin.register(models.PTC)
class PTCAdmin(admin.ModelAdmin):
    """Admin for the PTC model."""
    model = models.PTC

    list_display = ('id', 'ptc_1', 'ptc_2', 'ptc_3', 'ptc_4')
    orders = ('id',)

    fields = (
        'id', 'ptc_1', 'ptc_1_text', 'ptc_2', 'ptc_2_text',
        'ptc_3', 'ptc_3_text', 'ptc_4', 'ptc_4_text',
    )
