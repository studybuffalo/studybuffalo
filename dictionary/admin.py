from django.contrib import admin
from .models import (
    Language, DictionaryType, DictionaryClass, Word, ExcludedWord
)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(DictionaryType)
class DictionaryTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(DictionaryClass)
class DictionaryClassAdmin(admin.ModelAdmin):
    pass

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("word", "language", "dictionary_type", "dictionary_class")
    list_filter = ("language", "dictionary_type", "dictionary_class")
    search_fields = ("word",)

@admin.register(ExcludedWord)
class ExcludedWordAdmin(admin.ModelAdmin):
    list_display = ("word", "language", "dictionary_type", "dictionary_class")
    list_filter = ("language", "dictionary_type", "dictionary_class")
    search_fields = ("word",)