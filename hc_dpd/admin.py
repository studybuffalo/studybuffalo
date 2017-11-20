from django.contrib import admin
from .models import SubAHFS

@admin.register(SubAHFS)
class SubAHFSAdmin(admin.ModelAdmin):
    list_display = ("original", "substitution")
    ordering = ("original",)
