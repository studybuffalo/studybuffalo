"""Admin settings for the Updates app."""
from django.contrib import admin

from .models import Update

@admin.register(Update)
class UpdateSlideAdmin(admin.ModelAdmin):
    """Admin view for the Update model."""
    list_display = ('priority', 'title', 'start_date', 'end_date',)
    list_filter = ('start_date', 'end_date',)
    ordering = ('priority',)
