"""Tests for the Model module of the Dictionary app."""
import pytest

from dictionary import models


pytestmark = pytest.mark.django_db


def test__language__minimal_creation():
    """Tests minimal Language model creation."""
    language_count = models.Language.objects.count()

    models.Language.objects.create(language='English')

    assert models.Language.objects.count() == language_count + 1


def test__language__language__max_length():
    """Confirms language fields max length in Language model."""
    max_length = models.Language._meta.get_field('language').max_length

    assert max_length == 25


def test__language__str():
    """Tests for expected output of the Language __str__ method."""
    language = models.Language.objects.create(language='English')

    assert str(language) == 'English'


def test__dictionary_type__minimal_creation():
    """Tests minimal DictionaryType model creation."""
    dictionary_count = models.DictionaryType.objects.count()

    models.DictionaryType.objects.create(
        dictionary_name='A',
        dictionary_verbose_name='ABC',
    )

    assert models.DictionaryType.objects.count() == dictionary_count + 1


def test__dictionary_type__dictionary_name__max_length():
    """Confirms dictionary_name field's max length in DictionaryType model."""
    max_length = models.DictionaryType._meta.get_field('dictionary_name').max_length

    assert max_length == 50


def test__dictionary_type__dictionary_verbose_name__max_length():
    """Confirms dictionary_verbose_name field's max length in DictionaryType model."""
    max_length = models.DictionaryType._meta.get_field('dictionary_verbose_name').max_length

    assert max_length == 50


def test__dictionary_type__str():
    """Tests for expected output of the DictionaryType __str__ method."""
    dictionary = models.DictionaryType.objects.create(
        dictionary_name='A',
        dictionary_verbose_name='ABC',
    )

    assert str(dictionary) == 'A'


def test__dictionary_class__minimal_creation():
    """Tests minimal DictionaryClass model creation."""
    dictionary_count = models.DictionaryClass.objects.count()

    models.DictionaryClass.objects.create(
        class_name='A',
        class_verbose_name='ABC',
    )

    assert models.DictionaryClass.objects.count() == dictionary_count + 1


def test__dictionary_class__class_name__max_length():
    """Confirms dictionary_class field's max length in DictionaryClass model."""
    max_length = models.DictionaryClass._meta.get_field('class_name').max_length

    assert max_length == 20


def test__dictionary_class__class_verbose_name__max_length():
    """Confirms dictionary_class_name field's max length in DictionaryClass model."""
    max_length = models.DictionaryClass._meta.get_field('class_verbose_name').max_length

    assert max_length == 50


def test__dictionary_class__str():
    """Tests for expected output of the DictionaryClass __str__ method."""
    dictionary = models.DictionaryClass.objects.create(
        class_name='A',
        class_verbose_name='ABC',
    )

    assert str(dictionary) == 'A'


def test__word__minimal_creation():
    """Tests minimal Word model creation."""
    word_count = models.Word.objects.count()

    models.Word.objects.create(word='A')

    assert models.Word.objects.count() == word_count + 1


def test__word__word__max_length():
    """Confirms word field's max length in Word model."""
    max_length = models.Word._meta.get_field('word').max_length

    assert max_length == 50


def test__word__str():
    """Tests for expected output of the Word __str__ method."""
    word = models.Word.objects.create(word='A')

    assert str(word) == 'A'


def test__word_pending__minimal_creation():
    """Tests minimal WordPending model creation."""
    word_count = models.WordPending.objects.count()

    models.WordPending.objects.create(word='A')

    assert models.WordPending.objects.count() == word_count + 1


def test__word_pending__original_words__max_length():
    """Confirms original_words field's max length in WordPending model."""
    max_length = models.WordPending._meta.get_field('original_words').max_length

    assert max_length == 300


def test__word_pending__word__max_length():
    """Confirms word field's max length in WordPending model."""
    max_length = models.WordPending._meta.get_field('word').max_length

    assert max_length == 50


def test__word_pending__str():
    """Tests for expected output of the WordPending __str__ method."""
    word = models.WordPending.objects.create(word='A')

    assert str(word) == 'A'


def test__excluded_word__minimal_creation():
    """Tests minimal ExcludedWord model creation."""
    word_count = models.ExcludedWord.objects.count()

    models.ExcludedWord.objects.create(word='A')

    assert models.ExcludedWord.objects.count() == word_count + 1


def test__excluded_word__word__max_length():
    """Confirms word field's max length in ExcludedWord model."""
    max_length = models.ExcludedWord._meta.get_field('word').max_length

    assert max_length == 50


def test__excluded_word__str():
    """Tests for expected output of the ExcludedWord __str__ method."""
    word = models.ExcludedWord.objects.create(word='A')

    assert str(word) == 'A'
