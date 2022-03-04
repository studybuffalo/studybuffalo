"""Admin settings for the Substitution App."""
from django.contrib import admin

from .models import Apps, ModelFields


class FieldsInline(admin.TabularInline):
    """Admin inline for the Model Fields model."""
    model = ModelFields

    extra = 2
    verbose_name = 'Model Field'
    verbose_name_plural = 'Model Fields'

@admin.register(Apps)
class AppsAdmin(admin.ModelAdmin):
    """Admin for the Apps model."""
    list_display = ('app_name', 'model_pending', 'model_sub')
    ordering = ('app_name', 'model_pending', 'model_sub')
    fields = ['app_name', ('model_pending', 'model_sub')]
    inlines = [FieldsInline]
