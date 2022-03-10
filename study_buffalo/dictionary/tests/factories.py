"""Factories for testing the Dictionary app."""
import factory

from dictionary import models


class LanguageFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Language."""
    language = 'English'

    class Meta:
        model = models.Language
        django_get_or_create = ('language',)


class DictionaryTypeFactory(factory.django.DjangoModelFactory):
    """Factory to generate a DictionaryType."""
    dictionary_name = 'Test Type'
    dictionary_verbose_name = 'Verbose Test Type'

    class Meta:
        model = models.DictionaryType
        django_get_or_create = ('dictionary_name', 'dictionary_verbose_name')


class DictionaryClassFactory(factory.django.DjangoModelFactory):
    """Factory to generate a DictionaryClass."""
    class_name = 'Test Class'
    class_verbose_name = 'Verbose Test Class'

    class Meta:
        model = models.DictionaryClass
        django_get_or_create = ('class_name', 'class_verbose_name')


class WordFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Language."""
    dictionary_type = factory.SubFactory(DictionaryTypeFactory)
    dictionary_class = factory.SubFactory(DictionaryClassFactory)
    language = factory.SubFactory(LanguageFactory)
    word = 'TestWord'

    class Meta:
        model = models.Word
        django_get_or_create = (
            'dictionary_type', 'dictionary_class', 'language', 'word',
        )


class WordPendingFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Language."""
    dictionary_type = factory.SubFactory(DictionaryTypeFactory)
    dictionary_class = factory.SubFactory(DictionaryClassFactory)
    language = factory.SubFactory(LanguageFactory)
    original_words = 'The original words go here.'
    word = 'Pending'

    class Meta:
        model = models.WordPending
        django_get_or_create = (
            'dictionary_type', 'dictionary_class', 'language', 'word',
        )


class ExcludedWordFactory(factory.django.DjangoModelFactory):
    """Factory to generate a Language."""
    dictionary_type = factory.SubFactory(DictionaryTypeFactory)
    dictionary_class = factory.SubFactory(DictionaryClassFactory)
    language = factory.SubFactory(LanguageFactory)
    word = 'Excluded'

    class Meta:
        model = models.ExcludedWord
        django_get_or_create = (
            'dictionary_type', 'dictionary_class', 'language', 'word',
        )
