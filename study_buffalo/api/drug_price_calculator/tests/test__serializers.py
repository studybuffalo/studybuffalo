"""Tests for Drug Price Calculator API serializers."""
import pytest

from api.drug_price_calculator import serializers
from drug_price_calculator.models import Drug

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
    # Create serializer data
    idbl_data = create_idbl_data()

    # Create initial instance to work from
    instance = Drug.objects.create(din=idbl_data['din'])

    serializer = serializers.iDBLDataSerializer(
        instance=instance, data=idbl_data
    )

    # Confirm data is valid
    assert serializer.is_valid()

    # Save the data
    serializer.save()
