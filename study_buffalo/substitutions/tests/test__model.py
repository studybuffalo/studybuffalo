"""Tests for the Model module of the Substitutions app."""
import pytest

from substitutions import models


pytestmark = pytest.mark.django_db


def test__apps__minimal_creation():
    """Tests minimal Apps model creation."""
    apps_count = models.Apps.objects.count()

    models.Apps.objects.create(
        app_name='dpd_hc',
        model_pending='BrandSubPending',
        model_sub='BrandSub',
    )

    assert models.Apps.objects.count() == apps_count + 1


def test__apps__app_name__max_length():
    """Confirms app_name field's max length in Apps model."""
    max_length = models.Apps._meta.get_field('app_name').max_length

    assert max_length == 50


def test__apps__model_pending__max_length():
    """Confirms model_pending field's max length in Apps model."""
    max_length = models.Apps._meta.get_field('model_pending').max_length

    assert max_length == 50


def test__apps__model_sub__max_length():
    """Confirms model_sub field's max length in Apps model."""
    max_length = models.Apps._meta.get_field('model_sub').max_length

    assert max_length == 50


def test__apps__str():
    """Tests expected output of Apps __str__ method."""
    apps = models.Apps.objects.create(
        app_name='dpd_hc',
        model_pending='BrandSubPending',
        model_sub='BrandSub',
    )

    assert str(apps) == 'dpd_hc'


def test__model_fields__minimal_creation(substitutions_apps):
    """Tests minimal ModelFields model creation."""
    fields_count = models.ModelFields.objects.count()

    models.ModelFields.objects.create(
        app=substitutions_apps,
        field_name='original',
        field_type='o',
        dictionary_check=False,
        google_check=True,
    )

    assert models.ModelFields.objects.count() == fields_count + 1


def test__model_fields__field_name__max_length():
    """Confirms field_name field's max length in ModelFields model."""
    max_length = models.ModelFields._meta.get_field('field_name').max_length

    assert max_length == 50


def test__model_fields__field_type__max_length_default():
    """Confirms field_type field's max length and default in ModelFields model."""
    max_length = models.ModelFields._meta.get_field('field_type').max_length
    default = models.ModelFields._meta.get_field('field_type').default

    assert max_length == 1
    assert default == 's'


def test__model_fields__str(substitutions_apps):
    """Tests expected output of ModelFields __str__ method."""
    fields = models.ModelFields.objects.create(
        app=substitutions_apps,
        field_name='original',
        field_type='o',
        dictionary_check=False,
        google_check=True,
    )

    assert str(fields) == f'{substitutions_apps} - original'
