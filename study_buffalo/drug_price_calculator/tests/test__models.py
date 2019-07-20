"""Tests for Drug Price Calculator Views."""
import pytest

from drug_price_calculator import models


pytestmark = pytest.mark.django_db


def test__drug__minimal_model_creation():
    """Tests minimal Drug model creation."""
    drug_count = models.Drug.objects.count()

    models.Drug.objects.create(din='12345678')

    assert models.Drug.objects.count() == drug_count + 1

def test__drug__str__no_brand_name():
    """Tests Drug model __str__ without brand name."""
    drug = models.Drug.objects.create(din='12345678')

    assert str(drug) == '12345678'

def test__drug__str__with_brand_name():
    """Tests Drug model __str__ with brand name."""
    drug = models.Drug.objects.create(din='12345678', brand_name='a')

    assert str(drug) == 'a (12345678)'

def test__atc__minimal_model_creation():
    """Tests minimal ATC model creation."""
    atc_count = models.ATC.objects.count()

    models.ATC.objects.create(id='1234567')

    assert models.ATC.objects.count() == atc_count + 1

def test__atc__str__id():
    """Tests ATC model __str__ with only ID."""
    atc = models.ATC.objects.create(id='1234567')

    assert str(atc) == '1234567'

def test__atc__str__atc_1():
    """Tests ATC model __str__ with atc_1."""
    atc = models.ATC.objects.create(
        id='1234567', atc_1='1', atc_1_text='a'
    )

    assert str(atc) == '1 (a)'

def test__atc__str__atc_2():
    """Tests ATC model __str__ with atc_2."""
    atc = models.ATC.objects.create(
        id='1234567', atc_1='1', atc_1_text='a', atc_2='2', atc_2_text='b'
    )

    assert str(atc) == '2 (b)'

def test__atc__str__atc_3():
    """Tests ATC model __str__ with atc_3."""
    atc = models.ATC.objects.create(
        id='1234567', atc_1='1', atc_1_text='a', atc_2='2', atc_2_text='b',
        atc_3='3', atc_3_text='c',
    )

    assert str(atc) == '3 (c)'

def test__atc__str__atc_4():
    """Tests ATC model __str__ with atc_4."""
    atc = models.ATC.objects.create(
        id='1234567', atc_1='1', atc_1_text='a', atc_2='2', atc_2_text='b',
        atc_3='3', atc_3_text='c', atc_4='4', atc_4_text='d',
    )

    assert str(atc) == '4 (d)'

def test__atc__str__atc_5():
    """Tests ATC model __str__ with atc_5."""
    atc = models.ATC.objects.create(
        id='1234567', atc_1='1', atc_1_text='a', atc_2='2', atc_2_text='b',
        atc_3='3', atc_3_text='c', atc_4='4', atc_4_text='d', atc_5='5', atc_5_text='e',
    )

    assert str(atc) == '5 (e)'

def test__ptc__minimal_model_creation():
    """Tests minimal PTC model creation."""
    ptc_count = models.PTC.objects.count()

    models.PTC.objects.create(id='12345678901')

    assert models.PTC.objects.count() == ptc_count + 1

def test__ptc__str__id():
    """Tests PTC model __str__ with only ID."""
    ptc = models.PTC.objects.create(id='12345678901')

    assert str(ptc) == '12345678901'

def test__ptc__str__ptc_1():
    """Tests PTC model __str__ with ptc_1."""
    ptc = models.PTC.objects.create(
        id='12345678901', ptc_1='1', ptc_1_text='a'
    )

    assert str(ptc) == '1 (a)'

def test__ptc__str__ptc_2():
    """Tests PTC model __str__ with ptc_2."""
    ptc = models.PTC.objects.create(
        id='12345678901', ptc_1='1', ptc_1_text='a', ptc_2='2', ptc_2_text='b'
    )

    assert str(ptc) == '2 (b)'

def test__ptc__str__ptc_3():
    """Tests PTC model __str__ with ptc_3."""
    ptc = models.PTC.objects.create(
        id='12345678901', ptc_1='1', ptc_1_text='a', ptc_2='2', ptc_2_text='b',
        ptc_3='3', ptc_3_text='c',
    )

    assert str(ptc) == '3 (c)'

def test__ptc__str__ptc_4():
    """Tests PTC model __str__ with ptc_4."""
    ptc = models.PTC.objects.create(
        id='12345678901', ptc_1='1', ptc_1_text='a', ptc_2='2', ptc_2_text='b',
        ptc_3='3', ptc_3_text='c', ptc_4='4', ptc_4_text='d',
    )

    assert str(ptc) == '4 (d)'

def test__price__minimal_model_creation():
    """Tests minimal Price model creation."""
    price_count = models.Price.objects.count()

    drug = models.Drug.objects.create(din='12345678')
    models.Price.objects.create(drug=drug, abc_id=1)

    assert models.Price.objects.count() == price_count + 1

def test__price__str__without_brand_name():
    """Tests Price __str__ without drug brand name."""
    drug = models.Drug.objects.create(din='12345678')
    price = models.Price.objects.create(drug=drug, abc_id=1)

    assert str(price) == '12345678 price (1)'

def test__price__str__with_brand_name():
    """Tests Price __str__ with drug brand name."""
    drug = models.Drug.objects.create(din='12345678', brand_name='a')
    price = models.Price.objects.create(drug=drug, abc_id=1)

    assert str(price) == 'a price (1)'

def test__clients__minimal_model_creation():
    """Tests minimal Clients model creation."""
    clients_count = models.Clients.objects.count()

    drug = models.Drug.objects.create(din='12345678')
    price = models.Price.objects.create(drug=drug, abc_id=1)
    models.Clients.objects.create(price=price)

    assert models.Clients.objects.count() == clients_count + 1

def test__clients__str():
    """Tests Clients __str__ output."""
    drug = models.Drug.objects.create(din='12345678')
    price = models.Price.objects.create(drug=drug, abc_id=1)
    clients = models.Clients.objects.create(price=price)

    assert str(clients) == '12345678 price (1) clients'

def test__coverage_criteria__minimal_model_creation():
    """Tests minimal CoverageCriteria model creation."""
    coverage_criteria_count = models.CoverageCriteria.objects.count()

    drug = models.Drug.objects.create(din='12345678')
    price = models.Price.objects.create(drug=drug, abc_id=1)
    models.CoverageCriteria.objects.create(price=price, criteria='a')

    assert models.CoverageCriteria.objects.count() == coverage_criteria_count + 1

def test__coverage_criteria__str():
    """Tests CoverageCriteria __str__ output."""
    drug = models.Drug.objects.create(din='12345678')
    price = models.Price.objects.create(drug=drug, abc_id=1)
    criteria = models.CoverageCriteria.objects.create(price=price, criteria='a')

    assert str(criteria) == '12345678 price (1) coverage criteria'

def test__special_authorization__minimal_model_creation():
    """Tests minimal SpecialAuthorization model creation."""
    special_count = models.SpecialAuthorization.objects.count()

    models.SpecialAuthorization.objects.create(file_name='a', pdf_title='b')

    assert models.SpecialAuthorization.objects.count() == special_count + 1

def test__special_authorization__str():
    """Tests SpecialAuthorization __str__ output."""
    special = models.SpecialAuthorization.objects.create(
        file_name='a', pdf_title='b'
    )

    assert str(special) == 'b'

def test__subs_bsrf__minimal_model_creation():
    """Tests minimal SubsBSRF model creation."""
    sub_count = models.SubsBSRF.objects.count()

    models.SubsBSRF.objects.create(
        original='a', brand_name='b', strength='c', route='d', dosage_form='e'
    )

    assert models.SubsBSRF.objects.count() == sub_count + 1

def test__subs_generic__minimal_model_creation():
    """Tests minimal SubsGeneric model creation."""
    sub_count = models.SubsGeneric.objects.count()

    models.SubsGeneric.objects.create(original='a', correction='b')

    assert models.SubsGeneric.objects.count() == sub_count + 1

def test__subs_manufacturer__minimal_model_creation():
    """Tests minimal SubsManufacturer model creation."""
    sub_count = models.SubsManufacturer.objects.count()

    models.SubsManufacturer.objects.create(original='a', correction='b')

    assert models.SubsManufacturer.objects.count() == sub_count + 1

def test__subs_unit__minimal_model_creation():
    """Tests minimal SubsUnit model creation."""
    sub_count = models.SubsUnit.objects.count()

    models.SubsUnit.objects.create(original='a', correction='b')

    assert models.SubsUnit.objects.count() == sub_count + 1

def test__pend_bsrf__minimal_model_creation():
    """Tests minimal PendBSRF model creation."""
    pend_count = models.PendBSRF.objects.count()

    models.PendBSRF.objects.create(
        original='a', brand_name='b', strength='c', route='d', dosage_form='e'
    )

    assert models.PendBSRF.objects.count() == pend_count + 1

def test__pend_generic__minimal_model_creation():
    """Tests minimal PendGeneric model creation."""
    pend_count = models.PendGeneric.objects.count()

    models.PendGeneric.objects.create(original='a', correction='b')

    assert models.PendGeneric.objects.count() == pend_count + 1

def test__pend_manufacturer__minimal_model_creation():
    """Tests minimal PendManufacturer model creation."""
    pend_count = models.PendManufacturer.objects.count()

    models.PendManufacturer.objects.create(original='a', correction='b')

    assert models.PendManufacturer.objects.count() == pend_count + 1
