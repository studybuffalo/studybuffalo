"""Admin settings for the Health Canda Drug Product Database app."""
from django.contrib import admin
from .models import (
    SubAHFS, SubAHFSPend, SubBrand, SubBrandPend,
    SubCompanyName, SubCompanyNamePend, SubDescriptor, SubDescriptorPend,
    SubIngredient, SubIngredientPend, SubProductCategorization,
    SubProductCategorizationPend, SubRouteOfAdministration,
    SubRouteOfAdministrationPend, SubPharmaceuticalStd,
    SubPharmaceuticalStdPend, SubStreetName, SubStreetNamePend,
    SubSuiteNumber, SubSuiteNumberPend, SubUnit, SubUnitPend
)


@admin.register(SubAHFS)
class SubAHFSAdmin(admin.ModelAdmin):
    """Admin view for the Sub-AHFS model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - AHFS'
    verbose_name_plural = 'Substitutions - AHFS'

@admin.register(SubAHFSPend)
class SubAHFSPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-AHFS-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - AHFS (Pending)'
    verbose_name_plural = 'Substitutions - AHFS (Pending)'

@admin.register(SubBrand)
class SubBrandAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Brand model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Brand Name'
    verbose_name_plural = 'Substitutions - Brand Name'

@admin.register(SubBrandPend)
class SubBrandPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Brand-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Brand Name (Pending)'
    verbose_name_plural = 'Substitutions - Brand Name (Pending)'

@admin.register(SubCompanyName)
class SubCompanyNameAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Company Name model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Company Name'
    verbose_name_plural = 'Substitutions - Company Name'

@admin.register(SubCompanyNamePend)
class SubCompanyNamePendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Company Name-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Company Name (Pending)'
    verbose_name_plural = 'Substitutions - Company Name (Pending)'

@admin.register(SubDescriptor)
class SubDescriptorAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Descriptor model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Descriptor'
    verbose_name_plural = 'Substitutions - Descriptor'

@admin.register(SubDescriptorPend)
class SubDescriptorPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Descriptor-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Descriptor (Pending)'
    verbose_name_plural = 'Substitutions - Descriptor (Pending)'

@admin.register(SubIngredient)
class SubIngredientAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Ingredient model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Ingredient'
    verbose_name_plural = 'Substitutions - Ingredient'

@admin.register(SubIngredientPend)
class SubIngredientPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Ingredient-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Ingredient (Pending)'
    verbose_name_plural = 'Substitutions - Ingredient (Pending)'

@admin.register(SubProductCategorization)
class SubProductCategorizationAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Product Categorization model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Product Categorization'
    verbose_name_plural = 'Substitutions - Product Categorization'

@admin.register(SubProductCategorizationPend)
class SubProductCategorizationPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Product Categorization-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Product Categorization (Pending)'
    verbose_name_plural = 'Substitutions - Product Categorization (Pending)'

@admin.register(SubRouteOfAdministration)
class SubRouteOfAdministrationAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Route model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Route of Administration'
    verbose_name_plural = 'Substitutions - Route of Administration'

@admin.register(SubRouteOfAdministrationPend)
class SubRouteOfAdministrationPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Route-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Route of Administration (Pending)'
    verbose_name_plural = 'Substitutions - Route of Administration (Pending)'

@admin.register(SubPharmaceuticalStd)
class SubPharmaceuticalStdAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Pharmaceutical Standard model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Pharmaceutical Standard'
    verbose_name_plural = 'Substitutions - Pharmaceutical Standard'

@admin.register(SubPharmaceuticalStdPend)
class SubPharmaceuticalStdPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Pharmaceutical Standard-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Pharmaceutical Standard (Pending)'
    verbose_name_plural = 'Substitutions - Pharmaceutical Standard (Pending)'

@admin.register(SubStreetName)
class SubStreetNameAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Street Name model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Street Name'
    verbose_name_plural = 'Substitutions - Street Name'

@admin.register(SubStreetNamePend)
class SubStreetNamePendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Street Name-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Street Name (Pending)'
    verbose_name_plural = 'Substitutions - Street Name (Pending)'

@admin.register(SubSuiteNumber)
class SubSuiteNumberAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Suite Number model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Suite Number'
    verbose_name_plural = 'Substitutions - Suite Number'

@admin.register(SubSuiteNumberPend)
class SubSuiteNumberPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Suite Number-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Suite Number (Pending)'
    verbose_name_plural = 'Substitutions - Suite Number (Pending)'

@admin.register(SubUnit)
class SubUnitAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Unit model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Unit'
    verbose_name_plural = 'Substitutions - Unit'

@admin.register(SubUnitPend)
class SubUnitPendAdmin(admin.ModelAdmin):
    """Admin view for the Sub-Unit-Pending model."""
    list_display = ('original', 'substitution')
    ordering = ('original',)
    search_fields = ('original', 'substitution',)
    verbose_name = 'Substitution - Unit (Pending)'
    verbose_name_plural = 'Substitutions - Unit (Pending)'
