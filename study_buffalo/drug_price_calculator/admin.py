from django.contrib import admin

from . import models





@admin.register(models.Drug)
class DrugAdmin(admin.ModelAdmin):
    """Admin for the Drug (and related) models."""
    model = models.Drug

    list_display = ('din', 'brand_name', 'generic_name', 'strength', 'dosage_form')
    ordering = ('generic_name', 'strength', 'dosage_form')

class ClientsInlineAdmin(admin.StackedInline):
    model = models.Clients

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
    inlines = (ClientsInlineAdmin,)
