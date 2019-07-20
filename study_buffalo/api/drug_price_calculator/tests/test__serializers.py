"""Tests for Drug Price Calculator API serializers."""
from datetime import datetime
from decimal import Decimal

import pytest

from api.drug_price_calculator import serializers
from drug_price_calculator import models


pytestmark = pytest.mark.django_db


def create_idbl_data(**kwargs):
    """Creates a dictionary for iDBLDataSerializer."""
    clients = kwargs.get('clients', {
        'group_1': True,
        'group_66': True,
        'group_19823': True,
        'group_19823a': True,
        'group_19824': True,
        'group_20400': True,
        'group_20403': True,
        'group_20514': True,
        'group_22128': True,
        'group_23609': True,
    })
    special_authorization = kwargs.get('special_authorization', [{
        'file_name': 'l',
        'pdf_title': 'm',
    }])
    coverage_criteria = kwargs.get('coverage_criteria', [{
        'header': 'n',
        'criteria': 'o'
    }])

    return {
        'abc_id': kwargs.get('abc_id', 1),
        'din': kwargs.get('din', '12345678'),
        'bsrf': kwargs.get('bsrf', 'a b c d'),
        'generic_name': kwargs.get('generic_name', 'e'),
        'ptc': kwargs.get('ptc', '1'),
        'date_listed': kwargs.get('date_listed', '2019-01-01'),
        'unit_price': kwargs.get('unit_price', 1.0001),
        'lca_price': kwargs.get('lca_price', 2.0002),
        'mac_price': kwargs.get('mac_price', 3.0003),
        'mac_text': kwargs.get('mac_text', 'f'),
        'unit_issue': kwargs.get('unit_issue', 'g'),
        'manufacturer': kwargs.get('manufacturer', 'h'),
        'atc': kwargs.get('atc', 'i'),
        'schedule': kwargs.get('schedule', 'j'),
        'interchangeable': kwargs.get('interchangeable', True),
        'coverage_status': kwargs.get('coverage_status', 'k'),
        'clients': clients,
        'special_authorization': special_authorization,
        'coverage_criteria': coverage_criteria,
    }

def test__idbl_data_serializer__valid():
    """Tests that model is properly created via iDBL serializer."""
    # Get initial model counts
    drug_count = models.Drug.objects.count()
    price_count = models.Price.objects.count()
    clients_count = models.Clients.objects.count()
    coverage_count = models.CoverageCriteria.objects.count()
    special_count = models.SpecialAuthorization.objects.count()

    # Create serializer data
    idbl_data = create_idbl_data()

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid
    assert serializer.is_valid()

    # Save the data
    serializer.save()

    # Confirm data was properly added (by model counts)
    assert drug_count + 1 == models.Drug.objects.count()
    assert price_count + 1 == models.Price.objects.count()
    assert clients_count + 1 == models.Clients.objects.count()
    assert coverage_count + 1 == models.CoverageCriteria.objects.count()
    assert special_count + 1 == models.SpecialAuthorization.objects.count()

    # Confirm data to models was properly added
    drug = models.Drug.objects.get(din=idbl_data['din'])

    assert drug == instance

def test__idbl_data_serializer__valid__din():
    """Tests handling of just a valid DIN."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    assert drug.din == idbl_data['din']

def test__idbl_data_serializer__valid__bsrf():
    """Tests handling of just a valid BSRF."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'bsrf': 'a b c d',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    assert drug.brand_name == 'A B C D'

def test__idbl_data_serializer__valid__generic_name():
    """Tests handling of just a valid generic_name."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'generic_name': 'a',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    assert drug.generic_name == 'a'

def test__idbl_data_serializer__valid__ptc():
    """Tests handling of just a valid ptc."""
    # Create a PTC instance
    ptc = models.PTC.objects.create(id='1234')

    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'ptc': ptc.id,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    assert drug.ptc == ptc

def test__idbl_data_serializer__valid__manufacturer():
    """Tests handling of just a valid manufacturer."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'manufacturer': 'a',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save the data
    serializer.is_valid()
    drug = serializer.save()

    assert drug.manufacturer == 'A'

def test__idbl_data_serializer__valid__atc():
    """Tests handling of just a valid atc."""
    # Create ATC instance
    atc = models.ATC.objects.create(id='1234')

    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'atc': atc.id,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    assert drug.atc == atc

def test__idbl_data_serializer__get_atc_instance__missing():
    """Tests handling of just a valid atc."""
    # Create ATC instances
    atc = models.ATC.objects.create(
        id='A11BC22', atc_1='A', atc_1_text='description 1',
        atc_2='A11', atc_2_text='description 2', atc_3='A11B', atc_3_text='description 3',
        atc_4='A11BC', atc_4_text='description 4', atc_5='A11BC22', atc_5_text='description 5',
    )

    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'atc': 'A11BC33',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    # Confirm new ATC was made with proper details
    new_atc = models.ATC.objects.get(id='A11BC33')
    assert new_atc.atc_1 == 'A'
    assert new_atc.atc_1_text == 'description 1'
    assert new_atc.atc_2 == 'A11'
    assert new_atc.atc_2_text == 'description 2'
    assert new_atc.atc_3 == 'A11B'
    assert new_atc.atc_3_text == 'description 3'
    assert new_atc.atc_4 == 'A11BC'
    assert new_atc.atc_4_text == 'description 4'
    assert new_atc.atc_5 == 'A11BC33'
    assert new_atc.atc_5_text is None

def test__idbl_data_serializer__valid__schedule():
    """Tests handling of just a valid schedule."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'schedule': 'a',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save the data
    serializer.is_valid()
    drug = serializer.save()

    assert drug.schedule == 'a'

def test__idbl_data_serializer__valid__date_listed():
    """Tests handling of just a valid date_listed."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'date_listed': '2019-01-01',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.date_listed == datetime(2019, 1, 1).date()

def test__idbl_data_serializer__valid__unit_price():
    """Tests handling of just a valid unit_price."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'unit_price': 0.0001,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.unit_price == Decimal('0.0001')

def test__idbl_data_serializer__valid__lca_price():
    """Tests handling of just a valid lca_price."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'lca_price': 0.0001,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid and save serializer
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.lca_price == Decimal('0.0001')

def test__idbl_data_serializer__valid__mac_price():
    """Tests handling of just a valid mac_price."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'mac_price': 0.0001,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.mac_price == Decimal('0.0001')

def test__idbl_data_serializer__valid__mac_text():
    """Tests handling of just a valid mac_text."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'mac_text': 'a',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.mac_text == 'a'

def test__idbl_data_serializer__valid__interchangeable():
    """Tests handling of just a valid interchangeable."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'interchangeable': True,
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.interchangeable is True

def test__idbl_data_serializer__valid__coverage_status():
    """Tests handling of just a valid coverage_status."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'coverage_status': 'a',
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.coverage_status == 'a'

def test__idbl_data_serializer__valid__clients():
    """Tests handling of just a valid coverage_status."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'clients': {
            'group_1': True,
            'group_66': False,
            'group_19823': False,
            'group_19823a': False,
            'group_19824': False,
            'group_20400': False,
            'group_20403': False,
            'group_20514': False,
            'group_22128': False,
            'group_23609': False,
        },
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.clients.group_1 == True
    assert price.clients.group_66 == False

def test__idbl_data_serializer__valid__special_authorization():
    """Tests handling of just a valid special_authorization."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'special_authorization': [{
            'file_name': 'a',
            'pdf_title': 'b',
        }]
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.special_authorizations.count() == 1
    assert price.special_authorizations.last().file_name == 'a'
    assert price.special_authorizations.last().pdf_title == 'b'

def test__idbl_data_serializer__valid__coverage_criteria():
    """Tests handling of just a valid coverage_criteria."""
    # Create serializer data
    idbl_data = {
        'abc_id': 1,
        'din': '00000001',
        'coverage_criteria': [{
            'header': 'a',
            'criteria': 'b'
        }]
    }

    # Create initial instance to work from
    instance = models.Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Save data
    serializer.is_valid()
    drug = serializer.save()

    # Get the price model for this drug
    price = drug.prices.last()

    assert price.coverage_criteria.count() == 1
    assert price.coverage_criteria.last().header == 'a'
    assert price.coverage_criteria.last().criteria == 'b'

def test__idbl_data_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLDataSerializer(data={})

    try:
        serializer.is_valid()
        serializer.create(serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_data_serializer__max_lengths_match():
    """Tests that serializer and model max lengths match."""
    serializer = serializers.iDBLDataSerializer(data={})

def test__idbl_clients_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLClientsSerializer(data={})

    try:
        serializer.is_valid()
        serializer.create(serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_clients_serializer__update_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLClientsSerializer(data={})

    try:
        drug = models.Drug.objects.create(din='12345678')
        price = models.Price.objects.create(drug=drug, abc_id=1)
        clients = models.Clients.objects.create(price=price)

        serializer.is_valid()
        serializer.update(clients, serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_special_authorization_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLSpecialAuthorizationSerializer(
        data={'file_name': 'a', 'pdf_title': 'b'}
    )

    try:
        serializer.is_valid()
        serializer.create(serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_special_authorization_serializer__update_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLSpecialAuthorizationSerializer(
        data={'file_name': 'a', 'pdf_title': 'b'}
    )

    try:
        special = models.SpecialAuthorization.objects.create(file_name='a', pdf_title='b')

        serializer.is_valid()
        serializer.update(special, serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_coverage_criteria_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLCoverageCriteriaSerializer(
        data={'header': 'a', 'criteria': 'b'}
    )

    try:
        serializer.is_valid()
        serializer.create(serializer.validated_data)
    except AttributeError:
        assert False

    assert True

def test__idbl_coverage_criteria_serializer__update_exists():
    """Confirms create method exists."""
    serializer = serializers.iDBLCoverageCriteriaSerializer(
        data={'header': 'a', 'criteria': 'b'}
    )

    try:
        drug = models.Drug.objects.create(din='12345678')
        price = models.Price.objects.create(drug=drug, abc_id=1)
        criteria = models.CoverageCriteria.objects.create(price=price, criteria='a')

        serializer.is_valid()
        serializer.update(criteria, serializer.validated_data)
    except AttributeError:
        assert False

    assert True
