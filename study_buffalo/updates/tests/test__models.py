"""Tests for the Models module of the Updates app."""
import pytest

from django.utils import timezone

from updates import models


pytestmark = pytest.mark.django_db


def test__update__minimal_creation(updates_update):
    """Tests minimal Update model creation."""
    update_count = models.Update.objects.count()

    models.Update.objects.create(
        title='Update 1',
        icon=updates_update.icon,
        html='<html>Update 1</html>',
        priority=1,
    )

    assert models.Update.objects.count() == update_count + 1


def test__update__title__max_length():
    """Confirms title field's max length in Update model."""
    max_length = models.Update._meta.get_field('title').max_length

    assert max_length == 256


def test__update__priority__default():
    """Confirms priority field's default in Update model."""
    default = models.Update._meta.get_field('priority').default

    assert default == 1


def test__publication__str(updates_update):
    """Tests for expected output of the Update __str__ method."""
    update = models.Update.objects.create(
        title='Update 1',
        icon=updates_update.icon,
        html='<html>Update 1</html>',
        priority=1,
    )
    assert str(update) == 'Update 1'
