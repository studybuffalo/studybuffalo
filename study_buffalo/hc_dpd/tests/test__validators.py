"""Tests for Validators of HC DPD app."""
from django.core.exceptions import ValidationError

from hc_dpd import validators


def test__validate_check_start__passes_expected_1_step():
    """Confirms validator passes expected result with step = 1."""
    try:
        validators.validate_checksum_start(12, 1)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__passes_expected_10_step():
    """Confirms validator passes expected result with step = 10."""
    try:
        validators.validate_checksum_start(120, 10)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__passes_expected_100_step():
    """Confirms validator passes expected result with step = 100."""
    try:
        validators.validate_checksum_start(1200, 100)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__passes_expected_1000_step():
    """Confirms validator passes expected result with step = 1000."""
    try:
        validators.validate_checksum_start(12000, 1000)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__passes_expected_10000_step():
    """Confirms validator passes expected result with step = 10000."""
    try:
        validators.validate_checksum_start(120000, 10000)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__passes_expected_100000_step():
    """Confirms validator passes expected result with step = 100000."""
    try:
        validators.validate_checksum_start(1200000, 100000)
    except ValidationError:
        assert False
    else:
        assert True


def test__validate_check_start__fails_1_step():
    """Confirms validator fails with step = 1."""
    try:
        validators.validate_checksum_start(1.2, 1)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 1, 2, etc.' in e.message
        assert e.params == {'start': 1.2, 'step': 1}
    else:
        assert False


def test__validate_check_start__fails_10_step():
    """Confirms validator fails with step = 10."""
    try:
        validators.validate_checksum_start(12, 10)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 10, 20, etc.' in e.message
        assert e.params == {'start': 12, 'step': 10}
    else:
        assert False


def test__validate_check_start__fails_100_step():
    """Confirms validator fails with step = 100."""
    try:
        validators.validate_checksum_start(122, 100)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 100, 200, etc.' in e.message
        assert e.params == {'start': 122, 'step': 100}
    else:
        assert False


def test__validate_check_start__fails_1000_step():
    """Confirms validator fails with step = 1000."""
    try:
        validators.validate_checksum_start(1222, 1000)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 1000, 2000, etc.' in e.message
        assert e.params == {'start': 1222, 'step': 1000}
    else:
        assert False


def test__validate_check_start__fails_10000_step():
    """Confirms validator fails with step = 10000."""
    try:
        validators.validate_checksum_start(12222, 10000)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 10000, 20000, etc.' in e.message
        assert e.params == {'start': 12222, 'step': 10000}
    else:
        assert False


def test__validate_check_start__fails_100000_step():
    """Confirms validator fails with step = 100000."""
    try:
        validators.validate_checksum_start(122222, 100000)
    except ValidationError as e:
        assert 'Start values must be multiples of the step' in e.message
        assert '0, 100000, 200000, etc.' in e.message
        assert e.params == {'start': 122222, 'step': 100000}
    else:
        assert False
