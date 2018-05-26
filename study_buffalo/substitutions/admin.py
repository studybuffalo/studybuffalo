from django.contrib import admin
from .models import Apps, ModelFields

class FieldsInline(admin.TabularInline):
    model = ModelFields

    extra = 2
    verbose_name = "Model Field"
    verbose_name_plural = "Model Fields"

@admin.register(Apps)
class AppsAdmin(admin.ModelAdmin):
    list_display = ("app_name", "model_pending", "model_sub")
    ordering = ("app_name", "model_pending", "model_sub")
    fields = ["app_name", ("model_pending", "model_sub")]
    inlines = [FieldsInline]