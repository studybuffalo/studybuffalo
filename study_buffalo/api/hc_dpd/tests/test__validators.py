"""Tests for the HC DPD API validators."""
from collections import OrderedDict

import pytest

from rest_framework.serializers import ValidationError

from api.hc_dpd import validators


pytestmark = pytest.mark.django_db


def test__ascending_drug_code__valid_data():
    """Tests validator passes valid data as expected."""
    validator = validators.AscendingDrugCode()
    data = OrderedDict([
        ('TEST', [
            OrderedDict([('drug_code', 1)]),
            OrderedDict([('drug_code', 2)]),
            OrderedDict([('drug_code', 3)]),
        ]),
    ])

    try:
        validator(data)
    except ValidationError:
        assert False
    else:
        assert True


def test__ascending_drug_code__invalid_data():
    """Tests validator fails valid data as expected."""
    validator = validators.AscendingDrugCode()
    data = OrderedDict([
        ('TEST', [
            OrderedDict([('drug_code', 2)]),
            OrderedDict([('drug_code', 1)]),
            OrderedDict([('drug_code', 3)]),
        ]),
    ])

    try:
        validator(data)
    except ValidationError as e:
        assert 'TEST error' in str(e)
    else:
        assert False
