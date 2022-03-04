"""Admin settings for the Dictionary app."""
from django.contrib import admin
from .models import (
    Language, DictionaryType, DictionaryClass, Word, ExcludedWord
)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """Admin for the Language model."""


@admin.register(DictionaryType)
class DictionaryTypeAdmin(admin.ModelAdmin):
    """Admin for the Dictionary Type model."""


@admin.register(DictionaryClass)
class DictionaryClassAdmin(admin.ModelAdmin):
    """Admin for the Dictionary Class model"""


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    """Admin for the Word model."""
    list_display = ('word', 'language', 'dictionary_type', 'dictionary_class')
    list_filter = ('language', 'dictionary_type', 'dictionary_class')
    search_fields = ('word',)


@admin.register(ExcludedWord)
class ExcludedWordAdmin(admin.ModelAdmin):
    """Admin for the Excluded Word model."""
    list_display = ('word', 'language', 'dictionary_type', 'dictionary_class')
    list_filter = ('language', 'dictionary_type', 'dictionary_class')
    search_fields = ('word',)
