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
    """Tests handling of just a valid generic_name."""
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

# Add tests to confirm data addition through each key individually

# Confirm handling of missing values (should switch to default)
