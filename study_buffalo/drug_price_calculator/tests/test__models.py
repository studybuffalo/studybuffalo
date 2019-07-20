"""Tests for Drug Price Calculator Views."""
import pytest

from drug_price_calculator import models


pytestmark = pytest.mark.django_db


def test__drug__minimal_model_creation():
    """Tests minimal Drug model creation."""
    drug_count = models.Drug.objects.count()

    models.Drug.objects.create(din='12345678')

    assert models.Drug.objects.count() == drug_count + 1

def test__atc__minimal_model_creation():
    """Tests minimal ATC model creation."""
    atc_count = models.ATC.objects.count()

    models.ATC.objects.create(id='1234567')

    assert models.ATC.objects.count() == atc_count + 1
