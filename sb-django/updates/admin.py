from django.contrib import admin

from .models import Update

@admin.register(Update)
class UpdateSlideAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "priority", "background")
    list_filter = ("start_date", "end_date")