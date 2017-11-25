from django.contrib import admin
from .models import (
    MonitoredApplication, MonitoredModel, MonitoredField, DictionaryType, 
    Language, Word, ExcludedWord
)

class MonitoredModelInline(admin.TabularInline):
    model = MonitoredModel

class MonitoredFieldInline(admin.TabularInline):
    model = MonitoredField

@admin.register(MonitoredApplication)
class MonitoredApplicationAdmin(admin.ModelAdmin):
    inlines = [
        MonitoredModelInline,
    ]

@admin.register(MonitoredModel)
class MonitoredModelAdmin(admin.ModelAdmin):
    inlines = [
        MonitoredFieldInline,
    ]

@admin.register(DictionaryType)
class DictionaryTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "langauge", "dictionary_type")

@admin.register(ExcludedWord)
class ExcludedWordAdmin(admin.ModelAdmin):
    list_display = ("word", "langauge", "dictionary_type")
