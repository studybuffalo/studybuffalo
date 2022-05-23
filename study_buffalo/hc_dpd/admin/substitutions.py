"""Admin settings for the HC DPD Substitution Models."""
from django.contrib import admin

from hc_dpd import models


@admin.register(models.SubBrand)
class SubBrandAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Brand model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Brand Name'
    verbose_name_plural = 'Substitutions - Brand Name'


@admin.register(models.SubBrandPend)
class SubBrandPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Brand-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Brand Name (Pending)'
    verbose_name_plural = 'Substitutions - Brand Name (Pending)'


@admin.register(models.SubCompanyName)
class SubCompanyNameAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Company Name model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Company Name'
    verbose_name_plural = 'Substitutions - Company Name'


@admin.register(models.SubCompanyNamePend)
class SubCompanyNamePendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Company Name-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Company Name (Pending)'
    verbose_name_plural = 'Substitutions - Company Name (Pending)'


@admin.register(models.SubDescriptor)
class SubDescriptorAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Descriptor model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Descriptor'
    verbose_name_plural = 'Substitutions - Descriptor'


@admin.register(models.SubDescriptorPend)
class SubDescriptorPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Descriptor-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Descriptor (Pending)'
    verbose_name_plural = 'Substitutions - Descriptor (Pending)'


@admin.register(models.SubIngredient)
class SubIngredientAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Ingredient model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Ingredient'
    verbose_name_plural = 'Substitutions - Ingredient'


@admin.register(models.SubIngredientPend)
class SubIngredientPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Ingredient-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Ingredient (Pending)'
    verbose_name_plural = 'Substitutions - Ingredient (Pending)'


@admin.register(models.SubProductCategorization)
class SubProductCategorizationAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Product Categorization model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Product Categorization'
    verbose_name_plural = 'Substitutions - Product Categorization'


@admin.register(models.SubProductCategorizationPend)
class SubProductCategorizationPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Product Categorization-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Product Categorization (Pending)'
    verbose_name_plural = 'Substitutions - Product Categorization (Pending)'


@admin.register(models.SubRouteOfAdministration)
class SubRouteOfAdministrationAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Route model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Route of Administration'
    verbose_name_plural = 'Substitutions - Route of Administration'


@admin.register(models.SubRouteOfAdministrationPend)
class SubRouteOfAdministrationPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Route-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Route of Administration (Pending)'
    verbose_name_plural = 'Substitutions - Route of Administration (Pending)'


@admin.register(models.SubPharmaceuticalStd)
class SubPharmaceuticalStdAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Pharmaceutical Standard model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Pharmaceutical Standard'
    verbose_name_plural = 'Substitutions - Pharmaceutical Standard'


@admin.register(models.SubPharmaceuticalStdPend)
class SubPharmaceuticalStdPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Pharmaceutical Standard-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Pharmaceutical Standard (Pending)'
    verbose_name_plural = 'Substitutions - Pharmaceutical Standard (Pending)'


@admin.register(models.SubStreetName)
class SubStreetNameAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Street Name model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Street Name'
    verbose_name_plural = 'Substitutions - Street Name'


@admin.register(models.SubStreetNamePend)
class SubStreetNamePendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Street Name-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Street Name (Pending)'
    verbose_name_plural = 'Substitutions - Street Name (Pending)'


@admin.register(models.SubSuiteNumber)
class SubSuiteNumberAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Suite Number model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Suite Number'
    verbose_name_plural = 'Substitutions - Suite Number'


@admin.register(models.SubSuiteNumberPend)
class SubSuiteNumberPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Suite Number-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Suite Number (Pending)'
    verbose_name_plural = 'Substitutions - Suite Number (Pending)'


@admin.register(models.SubUnit)
class SubUnitAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Unit model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Unit'
    verbose_name_plural = 'Substitutions - Unit'


@admin.register(models.SubUnitPend)
class SubUnitPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Unit-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Unit (Pending)'
    verbose_name_plural = 'Substitutions - Unit (Pending)'
