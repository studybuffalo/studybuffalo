"""Models for the Dictionary app."""
from django.db import models


class Language(models.Model):
    """Language of the word"""
    language = models.CharField(max_length=25,)

    def __str__(self):
        return self.language

class DictionaryType(models.Model):
    """Dictionary type for creation of specific dictionary categories"""
    dictionary_name = models.CharField(max_length=50,)
    dictionary_verbose_name = models.CharField(max_length=50,)

    def __str__(self):
        return self.dictionary_name

class DictionaryClass(models.Model):
    """Specifies a dictionary classification"""
    class_name = models.CharField(max_length=20,)
    class_verbose_name = models.CharField(max_length=50,)

    class Meta:
        verbose_name = 'Dictionary class'
        verbose_name_plural = 'Dictionary classes'

    def __str__(self):
        return self.class_name

class Word(models.Model):
    """A single word in the dictionary"""
    dictionary_type = models.ForeignKey(
        to='DictionaryType',
        on_delete=models.SET_NULL,
        null=True,
    )
    language = models.ForeignKey(
        to='Language',
        on_delete=models.SET_NULL,
        null=True,
    )
    dictionary_class = models.ForeignKey(
        to=DictionaryClass,
        on_delete=models.SET_NULL,
        null=True,
    )
    word = models.CharField(max_length=50,)

    def __str__(self):
        return self.word

class WordPending(models.Model):
    """A single word pending inclusion into Word"""
    language = models.ForeignKey(
        to='Language',
        on_delete=models.SET_NULL,
        null=True,
    )
    dictionary_type = models.ForeignKey(
        to='DictionaryType',
        on_delete=models.SET_NULL,
        null=True,
    )
    dictionary_class = models.ForeignKey(
        to=DictionaryClass,
        on_delete=models.SET_NULL,
        null=True,
    )
    original_words = models.CharField(
        max_length=300,
        null=True,
    )
    word = models.CharField(max_length=50,)

    class Meta:
        permissions = (
            ('can_view', 'Can view the dictionary review application'),
        )
        verbose_name = 'Word (Pending)'
        verbose_name_plural = 'Words (Pending)'

    def __str__(self):
        return self.word

class ExcludedWord(models.Model):
    """A single word that will not be included in the dictionary"""
    dictionary_type = models.ForeignKey(
        to='DictionaryType',
        on_delete=models.SET_NULL,
        null=True,
    )
    language = models.ForeignKey(
        to='Language',
        on_delete=models.SET_NULL,
        null=True,
    )
    dictionary_class = models.ForeignKey(
        to=DictionaryClass,
        on_delete=models.SET_NULL,
        null=True,
    )
    word = models.CharField(max_length=50,)

    def __str__(self):
        return self.word
