"""Tests for Core model of HC DPD app."""
# pylint: disable=protected-access, too-many-lines
from datetime import datetime
from unittest.mock import patch
from zlib import crc32

import pytest
import pytz

from django.db import IntegrityError

from hc_dpd import models, utils, validators


pytestmark = pytest.mark.django_db


def test__dpd__minimal_model_creation():
    """Tests minimal DPD model creation."""
    dpd_count = models.DPD.objects.count()

    models.DPD.objects.create(drug_code=1)

    assert models.DPD.objects.count() == dpd_count + 1


def test__dpd__drug_code__negative_value():
    """Confirms that that drug code cannot be negative value."""
    try:
        models.DPD.objects.create(drug_code=-1)
    except IntegrityError as e:
        assert 'new row for relation "hc_dpd_dpd" violates check constraint "hc_dpd_dpd_drug_code_check"' in str(e)
    else:
        assert False


def test__dpd__str():
    """Confirms DPD __str__ output"""
    dpd = models.DPD.objects.create(drug_code=1)

    assert str(dpd) == '1'


@patch('django.utils.timezone.now')
def test__dpd__update_modified__active_ingredient(now):
    """Tests active_ingredient modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.ACTIVE_INGREDIENT)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified == utc_now
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__biosimilar(now):
    """Tests biosimilar modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.BIOSIMILAR)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified == utc_now
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__company(now):
    """Tests company modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.COMPANY)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified == utc_now
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__drug_product(now):
    """Tests drug_product modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.DRUG_PRODUCT)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified == utc_now
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__form(now):
    """Tests form modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.FORM)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified == utc_now
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__inactive_product(now):
    """Tests inactive_product modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.INACTIVE_PRODUCT)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified == utc_now
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__packaging(now):
    """Tests packaging modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.PACKAGING)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified == utc_now
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__pharmaceutical_standard(now):
    """Tests pharmaceutical_standard modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.PHARMACEUTICAL_STANDARD)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified == utc_now
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__route(now):
    """Tests route modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.ROUTE)

    # Confirm expected update to modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified == utc_now
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__schedule(now):
    """Tests schedule modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.SCHEDULE)

    # Confirm expected update to modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified == utc_now
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__status(now):
    """Tests schedule modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.STATUS)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified == utc_now
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__therapeutic_class(now):
    """Tests therapeutic_class modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.THERAPUETIC_CLASS)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified == utc_now
    assert dpd.original_veterinary_species_modified is None


@patch('django.utils.timezone.now')
def test__dpd__update_modified__veterinary_class(now):
    """Tests veterinary_class modified field is updated."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.VETERINARY_SPECIES)

    # Confirm expected update to modified field in database
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None
    assert dpd.original_biosimilar_modified is None
    assert dpd.original_company_modified is None
    assert dpd.original_drug_product_modified is None
    assert dpd.original_form_modified is None
    assert dpd.original_inactive_product_modified is None
    assert dpd.original_packaging_modified is None
    assert dpd.original_pharmaceutical_standard_modified is None
    assert dpd.original_route_modified is None
    assert dpd.original_schedule_modified is None
    assert dpd.original_status_modified is None
    assert dpd.original_therapeutic_class_modified is None
    assert dpd.original_veterinary_species_modified == utc_now


@patch('django.utils.timezone.now')
def test__dpd__update_modified__bulk(now):
    """Tests that update_modified will support bulk_update."""
    dpd = models.DPD.objects.create(drug_code=1)

    # Confirm no value for any modified field
    assert dpd.original_active_ingredient_modified is None

    # Update the modified field
    utc_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    now.return_value = utc_now
    dpd.update_modified(utils.ACTIVE_INGREDIENT, bulk=True)

    # Confirm field is not modified at database level
    dpd.refresh_from_db()
    assert dpd.original_active_ingredient_modified is None


def test__dpd__original_modified_field_mapping():
    """Confirms mapping is configured as expected."""
    mapping = models.DPD.original_modified_field_mapping()

    assert mapping == {
        'active_ingredient': 'original_active_ingredient_modified',
        'biosimilar': 'original_biosimilar_modified',
        'company': 'original_company_modified',
        'drug_product': 'original_drug_product_modified',
        'form': 'original_form_modified',
        'inactive_product': 'original_inactive_product_modified',
        'packaging': 'original_packaging_modified',
        'pharmaceutical_standard': 'original_pharmaceutical_standard_modified',
        'route': 'original_route_modified',
        'schedule': 'original_schedule_modified',
        'status': 'original_status_modified',
        'therapeutic_class': 'original_therapeutic_class_modified',
        'veterinary_species': 'original_veterinary_species_modified',
    }


def test__dpd_checksum__minimal_model_creation():
    """Tests minimal DPDChecksum model creation."""
    checksum_count = models.DPDChecksum.objects.count()

    models.DPDChecksum.objects.create(
        drug_code_start=0,
        drug_code_step=10000,
        extract_source=utils.ACTIVE_INGREDIENT,
    )

    assert models.DPDChecksum.objects.count() == checksum_count + 1


def test__dpd_checksum__extract_source__max_length():
    """Tests extract_source max length."""
    assert models.DPDChecksum._meta.get_field('extract_source').max_length == 32


def test__dpd_checksum__extract_source__choices():
    """Confirms the possible extract_source choices."""
    choices = models.DPDChecksum._meta.get_field('extract_source').choices
    choice_keys = [key for key, _ in choices]

    assert len(choices) == 13
    assert utils.ACTIVE_INGREDIENT in choice_keys
    assert utils.BIOSIMILAR in choice_keys
    assert utils.COMPANY in choice_keys
    assert utils.DRUG_PRODUCT in choice_keys
    assert utils.FORM in choice_keys
    assert utils.INACTIVE_PRODUCT in choice_keys
    assert utils.PACKAGING in choice_keys
    assert utils.PHARMACEUTICAL_STANDARD in choice_keys
    assert utils.ROUTE in choice_keys
    assert utils.SCHEDULE in choice_keys
    assert utils.STATUS in choice_keys
    assert utils.THERAPUETIC_CLASS in choice_keys
    assert utils.VETERINARY_SPECIES in choice_keys


def test__dpd_checksum__checksum__max_length():
    """Tests checksum max length."""
    assert models.DPDChecksum._meta.get_field('checksum').max_length == 10


def test__dpd_checksum__step_choices():
    """Confirms the possible step_choices choices."""
    choices = models.DPDChecksum.STEP_CHOICES
    choice_keys = [key for key, _ in choices]

    assert len(choices) == 6
    assert 1 in choice_keys
    assert 10 in choice_keys
    assert 100 in choice_keys
    assert 1000 in choice_keys
    assert 10000 in choice_keys
    assert 100000 in choice_keys


def test__dpd_checksum__clean__valid():
    """Tests handling of valid model instance creation."""
    checksum = models.DPDChecksum.objects.create(
        drug_code_start=0,
        drug_code_step=10000,
        extract_source=utils.ACTIVE_INGREDIENT,
    )

    try:
        checksum.drug_code_start = 20000
        checksum.clean()
    except validators.ValidationError:
        assert False
    else:
        assert True


def test__dpd_checksum__clean__invalid():
    """Tests handling of invalid model instance creation."""
    checksum = models.DPDChecksum.objects.create(
        drug_code_start=0,
        drug_code_step=10000,
        extract_source=utils.ACTIVE_INGREDIENT,
    )

    try:
        checksum.drug_code_start = 2
        checksum.clean()
    except validators.ValidationError as e:
        assert 'Start values must be multiples of the step' in str(e)
    else:
        assert False


@patch('hc_dpd.models.core.DPDChecksum.calculate_checksum')
def test__dpd_checksum__save(calculate_checksum):
    """Confirms a checksum is created when save is run."""
    calculate_checksum.return_value = 'TEST'
    checksum = models.DPDChecksum.objects.create(
        drug_code_start=0,
        drug_code_step=10000,
        extract_source=utils.ACTIVE_INGREDIENT,
    )

    assert checksum.checksum == 'TEST'


@patch('hc_dpd.models.core.DPDChecksum.calculate_checksum')
def test__dpd_checksum__create_checksum(calculate_checksum):
    """Tests that create_checksum updates expected fields."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.ACTIVE_INGREDIENT
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''
    assert checksum.checksum_date is None

    # Call method to generate checksum data
    calculate_checksum.return_value = 'TEST'
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum == 'TEST'
    assert checksum.checksum_date is None


def test__dpd_checksum__create_checksum__active_ingredient(hc_dpd_original_active_ingredient):
    """Tests that checksum can be created from active ingredient model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.ACTIVE_INGREDIENT
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another active ingredient instance
    new_instance = models.OriginalActiveIngredient.objects.get(
        pk=hc_dpd_original_active_ingredient.pk
    )
    new_instance.pk = hc_dpd_original_active_ingredient.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__biosimilar(hc_dpd_original_biosimilar):
    """Tests that checksum can be created from biosimilar model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.BIOSIMILAR
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another biosimilar instance
    new_instance = models.OriginalBiosimilar.objects.get(
        pk=hc_dpd_original_biosimilar.pk
    )
    new_instance.pk = hc_dpd_original_biosimilar.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__company(hc_dpd_original_company):
    """Tests that checksum can be created from company model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.COMPANY
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another company instance
    new_instance = models.OriginalCompany.objects.get(
        pk=hc_dpd_original_company.pk
    )
    new_instance.pk = hc_dpd_original_company.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__drug_product(hc_dpd_original_drug_product):
    """Tests that checksum can be created from drug product model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.DRUG_PRODUCT
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another drug product instance
    new_instance = models.OriginalDrugProduct.objects.get(
        pk=hc_dpd_original_drug_product.pk
    )
    new_instance.pk = hc_dpd_original_drug_product.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__form(hc_dpd_original_form):
    """Tests that checksum can be created from form model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.FORM
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another form instance
    new_instance = models.OriginalForm.objects.get(
        pk=hc_dpd_original_form.pk
    )
    new_instance.pk = hc_dpd_original_form.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__inactive_product(hc_dpd_original_inactive_product):
    """Tests that checksum can be created from inactive product model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.INACTIVE_PRODUCT
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another inactive product instance
    new_instance = models.OriginalInactiveProduct.objects.get(
        pk=hc_dpd_original_inactive_product.pk
    )
    new_instance.pk = hc_dpd_original_inactive_product.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__packaging(hc_dpd_original_packaging):
    """Tests that checksum can be created from packaging model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.PACKAGING
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another packaging instance
    new_instance = models.OriginalPackaging.objects.get(
        pk=hc_dpd_original_packaging.pk
    )
    new_instance.pk = hc_dpd_original_packaging.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__pharmaceutical_standard(hc_dpd_original_pharmaceutical_standard):
    """Tests that checksum can be created from pharmaceutical standard model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.PHARMACEUTICAL_STANDARD
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another pharmaceutical standard instance
    new_instance = models.OriginalPharmaceuticalStandard.objects.get(
        pk=hc_dpd_original_pharmaceutical_standard.pk
    )
    new_instance.pk = hc_dpd_original_pharmaceutical_standard.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__route(hc_dpd_original_route):
    """Tests that checksum can be created from route model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.ROUTE
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another route instance
    new_instance = models.OriginalRoute.objects.get(
        pk=hc_dpd_original_route.pk
    )
    new_instance.pk = hc_dpd_original_route.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__schedule(hc_dpd_original_schedule):
    """Tests that checksum can be created from schedule model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.SCHEDULE
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another schedule instance
    new_instance = models.OriginalSchedule.objects.get(
        pk=hc_dpd_original_schedule.pk
    )
    new_instance.pk = hc_dpd_original_schedule.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__status(hc_dpd_original_status):
    """Tests that checksum can be created from status model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.STATUS
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another status instance
    new_instance = models.OriginalStatus.objects.get(
        pk=hc_dpd_original_status.pk
    )
    new_instance.pk = hc_dpd_original_status.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__therapeutic_class(hc_dpd_original_therapeutic_class):
    """Tests that checksum can be created from therapeutic class model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.THERAPUETIC_CLASS
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another therapeutic class instance
    new_instance = models.OriginalTherapeuticClass.objects.get(
        pk=hc_dpd_original_therapeutic_class.pk
    )
    new_instance.pk = hc_dpd_original_therapeutic_class.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__veterinary_species(hc_dpd_original_veterinary_species):
    """Tests that checksum can be created from veterinary species model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.VETERINARY_SPECIES
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another veterinary species instance
    new_instance = models.OriginalVeterinarySpecies.objects.get(
        pk=hc_dpd_original_veterinary_species.pk
    )
    new_instance.pk = hc_dpd_original_veterinary_species.pk + 9999
    new_instance.save()

    # Confirm checksum has changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum != old_checksum


def test__dpd_checksum__create_checksum__confirm_sorting():
    """Tests that sorting returns consistent result."""
    assert False


def test__dpd_checksum__create_checksum__two_models(
    hc_dpd_original_biosimilar, hc_dpd_original_company
):  # pylint: disable=unused-argument
    """Tests that checksum only pulls data from expected model."""
    # Create initial checksum model
    checksum = models.DPDChecksum(
        drug_code_start=0,
        drug_code_step=100000,
        extract_source=utils.BIOSIMILAR
    )

    # Confirm no checksum details added yet
    assert checksum.checksum == ''

    # Call method to generate checksum data
    checksum.create_checksum()

    # Confirm checksum data now added
    assert checksum.checksum != ''

    # Create another company instance
    new_instance = models.OriginalCompany.objects.get(
        pk=hc_dpd_original_company.pk
    )
    new_instance.pk = hc_dpd_original_company.pk + 9999
    new_instance.save()

    # Confirm checksum has not changed due to new data
    old_checksum = checksum.checksum
    checksum.create_checksum()

    assert checksum.checksum != ''
    assert checksum.checksum == old_checksum


def test__dpd_checksum__calculate_checksum():
    """Tests that calculate_checksum creates expected output."""
    # Create a test checksum
    checksum = crc32('TEST'.encode('utf-8'))

    assert models.DPDChecksum.calculate_checksum('TEST') == checksum


def test__dpd_checksum__compile_checksum_string(hc_dpd_original_active_ingredient):
    """Confirm that compile_checksum_string creates expected string."""
    # Update field to streamline testing
    ingredient = hc_dpd_original_active_ingredient
    ingredient.active_ingredient_code = 'ONE'
    ingredient.strength = 1
    ingredient.save()

    # Create fake field order for testing
    field_order = ['strength', 'pk', 'active_ingredient_code']

    # Confirm expected checksum string
    checksum_string = models.DPDChecksum.compile_checksum_string(ingredient, field_order)

    assert checksum_string == f'1{ingredient.pk}ONE'
