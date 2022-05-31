"""Tests for the API utility functions."""
from api.utils import utils


def test__convert_serializer_errors__with_non_field():
    """Tests error conversion when non_field_errors present."""
    serializer_errors = {
        'non_field_errors': ['A'],
        'field_1': ['B'],
        'field_2': ['C'],
    }

    errors = utils.convert_serializer_errors(serializer_errors)

    assert 'field' in errors
    assert isinstance(errors['field'], dict)
    assert errors['field']['field_1'] == ['B']
    assert errors['field']['field_2'] == ['C']

    assert 'non_field' in errors
    assert isinstance(errors['non_field'], list)
    assert errors['non_field'] == ['A']


def test__convert_serializer_errors__without_non_field():
    """Tests error conversion when non_field_errors absence."""
    serializer_errors = {
        'field_1': ['A'],
        'field_2': ['B'],
    }

    errors = utils.convert_serializer_errors(serializer_errors)

    assert 'field' in errors
    assert isinstance(errors['field'], dict)
    assert errors['field']['field_1'] == ['A']
    assert errors['field']['field_2'] == ['B']

    assert 'non_field' in errors
    assert isinstance(errors['non_field'], list)
    assert errors['non_field'] == []
