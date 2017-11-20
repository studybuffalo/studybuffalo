from django.contrib import admin
from .models import SubAHFS, SubAHFSPend

@admin.register(SubAHFS)
class SubAHFSAdmin(admin.ModelAdmin):
    list_display = ("original", "substitution")
    ordering = ("original",)

@admin.register(SubAHFSPend)
class SubAHFSPendAdmin(admin.ModelAdmin):
    list_display = ("original", "substitution")
    ordering = ("original",)
