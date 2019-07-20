"""Tests for Drug Price Calculator API views."""
import json

import pytest

from rest_framework.test import APIClient

from drug_price_calculator import models


pytestmark = pytest.mark.django_db

def create_drug(**kwargs):
    din = kwargs.get('din', '12345678')
    generic_name = kwargs.get('generic_name', 'generic')
    brand_name = kwargs.get('brand_name', 'Brand')
    generic_product = kwargs.get('generic_product', 'generic product')

    drug = models.Drug.objects.create(
        din=din, generic_name=generic_name, brand_name=brand_name,
        generic_product=generic_product,
    )

    abc_id = kwargs.get('abc_id', 1)
    unit_price = kwargs.get('unit_price', 1)
    models.Price.objects.create(
        drug=drug, abc_id=abc_id, unit_price=unit_price
    )

    return drug

def test__upload_idbl_data__valid(token):
    """Tests that iDBL data upload view functions properly with valid data."""
    # Get DIN for URL
    din = '12345678'

    # Authenticate and make request
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
    response = client.post(
        '/api/drug-price-calculator/v1/{}/upload/'.format(din),
        data={'din': din, 'abc_id': 1}
    )
    content = json.loads(response.content)

    assert 'message' in content
    assert content['message'] == 'Drug and price file successfully created.'
    assert 'drug_id' in content
    assert isinstance(content['drug_id'], int)

def test__upload_idbl_data__invalid_din(token):
    """Tests iDBL data upload handles invalid DIN."""
    # Get DIN for URL
    din = '1234567'

    # Authenticate and make request
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
    response = client.post(
        '/api/drug-price-calculator/v1/{}/upload/'.format(din),
        data={'din': din, 'abc_id': 1}
    )
    content = json.loads(response.content)

    assert response.status_code == 400
    assert 'error' in content
    assert content['error'] == 'invalid_din'
    assert 'error_description' in content
    assert content['error_description'] == 'DIN/NPN/PIN format is invalid.'

def test__upload_idbl_data__invalid_data(token):
    """Tests iDBL data upload handles invalid serializer data."""
    # Get DIN for URL
    din = '12345678'

    # Authenticate and make request
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token.key))
    response = client.post(
        '/api/drug-price-calculator/v1/{}/upload/'.format(din),
        data={'din': din, 'abc_id': 'a'}
    )
    content = json.loads(response.content)

    assert response.status_code == 400
    assert 'abc_id' in content
    assert content['abc_id'] == ['A valid integer is required.']

def test__drug_list__valid():
    """Tests DrugList view returns data with valid request."""
    # Create a drug file
    drug = create_drug()

    # Authenticate and make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/?q=a')
    content = json.loads(response.content)['results']

    assert len(content) == 1
    assert content[0]['id'] == drug.id

def test__drug_list__output_keys():
    """Tests DrugList view returns output with expected keys."""
    # Create a drug file
    drug = create_drug()

    # Authenticate and make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/?q=a')
    content = json.loads(response.content)['results'][0]

    assert 'id' in content
    assert 'brand_name' in content
    assert 'generic_name' in content
    assert 'strength' in content
    assert 'route' in content
    assert 'dosage_form' in content
    assert 'generic_product' in content

def test__drug_list__generic_name_filter():
    """Tests DrugList view filters on generic name."""
    # Create a drug file
    create_drug(din='11111111', generic_name='a1', brand_name='b')
    create_drug(din='11111112', generic_name='a2', brand_name='b')
    create_drug(din='11111113', generic_name='b1', brand_name='b')
    create_drug(din='11111114', generic_name='c1', brand_name='b')

    # Authenticate and make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/?q=a')
    content = json.loads(response.content)['results']

    assert len(content) == 2

def test__drug_list__brand_name_filter():
    """Tests DrugList view filters on generic name."""
    # Create a drug file
    create_drug(din='11111111', generic_name='g', brand_name='a1')
    create_drug(din='11111112', generic_name='g', brand_name='a2')
    create_drug(din='11111113', generic_name='g', brand_name='b1')
    create_drug(din='11111114', generic_name='g', brand_name='c1')

    # Authenticate and make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/?q=a')
    content = json.loads(response.content)['results']

    assert len(content) == 2

def test__drug_list__requires_unit_price():
    """Tests DrugList view excludes products without unit_price."""
    # Create a drug file
    drug = create_drug(din='11111111', generic_name='g', brand_name='a1')
    create_drug(din='11111112', generic_name='g', brand_name='a2')

    # Change price
    price = drug.prices.first()
    price.unit_price = None
    price.save()

    # Authenticate and make request
    client = APIClient()
    response = client.get('/api/drug-price-calculator/v1/drugs/?q=a')
    content = json.loads(response.content)['results']

    assert len(content) == 1

def test__drug_price_list__valid():
    """Tests DrugPriceList view returns data with valid request."""
    # Create drug and price files
    drug_1 = create_drug(din='11111111')
    price_1 = drug_1.prices.last()
    drug_2 = create_drug(din='11111112')
    price_2 = drug_2.prices.last()

    # Authenticate and make request
    url = '/api/drug-price-calculator/v1/drugs/prices/?ids={},{}'.format(
        drug_1.id, drug_2.id
    )

    client = APIClient()
    response = client.get(url)
    content = json.loads(response.content)

    assert len(content) == 2
    assert content[0]['id'] in (price_1.id, price_2.id)
    assert content[1]['id'] in (price_1.id, price_2.id)

def test__drug_price_list__missing_ids():
    """Tests DrugPriceList view returns error if ids parameter missing."""
    # Create a drug file
    drug = create_drug()
    price = drug.prices.last()

    # Authenticate and make request
    url = '/api/drug-price-calculator/v1/drugs/prices/'

    client = APIClient()
    response = client.get(url)
    content = json.loads(response.content)

    assert content['detail'] == 'No IDs provided in query.'

def test__drug_price_list__missing_ids():
    """Tests DrugPriceList view returns error if no ids provided."""
    # Create a drug file
    drug = create_drug()
    price = drug.prices.last()

    # Authenticate and make request
    url = '/api/drug-price-calculator/v1/drugs/prices/?ids='

    client = APIClient()
    response = client.get(url)

    content = json.loads(response.content)

    assert content['detail'] == 'No IDs provided in query.'

def test__drug_price_list__invalid_id_format():
    """Tests DrugPriceList view returns error if no ids provided."""
    # Create a drug file
    drug = create_drug()
    price = drug.prices.last()

    # Authenticate and make request
    url = '/api/drug-price-calculator/v1/drugs/prices/?ids=a'

    client = APIClient()
    response = client.get(url)

    content = json.loads(response.content)

    assert content['detail'] == 'Invalid ID format provided.'
