"""Tests for the HC DPD API upload serializers."""
# pylint: disable=protected-access, too-many-lines
from datetime import datetime
from unittest.mock import patch

import pytz
import pytest

from django.db import transaction

from rest_framework import serializers as drf_serializers

from hc_dpd import models

from api.hc_dpd import serializers
from api.hc_dpd.tests import utils


pytestmark = pytest.mark.django_db


def test__upload_dpd_extracts_serializer__fields():
    """Confirms that all fields used expected serializers."""
    serializer = serializers.UploadDPDExtractsSerializer(data={})

    assert isinstance(serializer.fields['active_ingredient'].child, serializers.ActiveIngredientSerializer)
    assert isinstance(serializer.fields['biosimilar'].child, serializers.BiosimilarSerializer)
    assert isinstance(serializer.fields['company'].child, serializers.CompanySerializer)
    assert isinstance(serializer.fields['drug_product'].child, serializers.DrugProductSerializer)
    assert isinstance(serializer.fields['form'].child, serializers.FormSerializer)
    assert isinstance(serializer.fields['inactive_product'].child, serializers.InactiveProductSerializer)
    assert isinstance(serializer.fields['packaging'].child, serializers.PackagingSerializer)
    assert isinstance(serializer.fields['pharmaceutical_standard'].child, serializers.PharmaceuticalStandardSerializer)
    assert isinstance(serializer.fields['route'].child, serializers.RouteSerializer)
    assert isinstance(serializer.fields['schedule'].child, serializers.ScheduleSerializer)
    assert isinstance(serializer.fields['status'].child, serializers.StatusSerializer)
    assert isinstance(serializer.fields['therapeutic_class'].child, serializers.TherapeuticClassSerializer)
    assert isinstance(serializer.fields['veterinary_species'].child, serializers.VeterinarySpeciesSerializer)


def test__upload_dpd_extracts_serializer__fields_many():
    """Confirms that all fields have expected "many" attribute."""
    serializer = serializers.UploadDPDExtractsSerializer(data={})

    assert serializer.fields['active_ingredient'].many is True
    assert serializer.fields['biosimilar'].many is True
    assert serializer.fields['company'].many is True
    assert serializer.fields['drug_product'].many is True
    assert serializer.fields['form'].many is True
    assert serializer.fields['inactive_product'].many is True
    assert serializer.fields['packaging'].many is True
    assert serializer.fields['pharmaceutical_standard'].many is True
    assert serializer.fields['route'].many is True
    assert serializer.fields['schedule'].many is True
    assert serializer.fields['status'].many is True
    assert serializer.fields['therapeutic_class'].many is True
    assert serializer.fields['veterinary_species'].many is True


def test__upload_dpd_extracts_serializer__fields_required():
    """Confirms that all fields have expected "required" attribute."""
    serializer = serializers.UploadDPDExtractsSerializer(data={})

    assert serializer.fields['active_ingredient'].required is False
    assert serializer.fields['biosimilar'].required is False
    assert serializer.fields['company'].required is False
    assert serializer.fields['drug_product'].required is False
    assert serializer.fields['form'].required is False
    assert serializer.fields['inactive_product'].required is False
    assert serializer.fields['packaging'].required is False
    assert serializer.fields['pharmaceutical_standard'].required is False
    assert serializer.fields['route'].required is False
    assert serializer.fields['schedule'].required is False
    assert serializer.fields['status'].required is False
    assert serializer.fields['therapeutic_class'].required is False
    assert serializer.fields['veterinary_species'].required is False


def test__upload_dpd_extracts_serializer__create_exists():
    """Confirms the create method is overridden correctly."""
    serializer = serializers.UploadDPDExtractsSerializer(data={})

    assert serializer.create({}) is None


def test__upload_dpd_extracts_serializer__update_exists():
    """Confirms the upad method is overridden correctly."""
    serializer = serializers.UploadDPDExtractsSerializer(data={})

    assert serializer.update(None, {}) is None


def test__upload_dpd_and_extracts_serializer__fields():
    """Confirms that fields use expected serializers."""
    serializer = serializers.UploadDPDAndExtractsSerializer(data={})

    assert isinstance(serializer.fields['drug_code'], drf_serializers.IntegerField)
    assert isinstance(serializer.fields['extract_data'], serializers.UploadDPDExtractsSerializer)


def test__upload_dpd_and_extracts_serializer__fields_required():
    """Confirms that all fields have expected "required" attribute."""
    serializer = serializers.UploadDPDAndExtractsSerializer(data={})

    assert serializer.fields['drug_code'].required is True
    assert serializer.fields['extract_data'].required is True


def test__upload_dpd_and_extracts_serializer__fields_min_value():
    """Confirms that all fields have expected "min_value" attribute."""
    serializer = serializers.UploadDPDAndExtractsSerializer(data={})

    assert serializer.fields['drug_code'].min_value == 1


def test__upload_dpd_and_extracts_serializer__create_exists():
    """Confirms the create method is overridden correctly."""
    serializer = serializers.UploadDPDAndExtractsSerializer(data={})

    assert serializer.create({}) is None


def test__upload_dpd_and_extracts_serializer__update_exists():
    """Confirms the upad method is overridden correctly."""
    serializer = serializers.UploadDPDAndExtractsSerializer(data={})

    assert serializer.update(None, {}) is None


def test__upload_dpd_data_serializer__fields():
    """Confirms that fields use expected serializers."""
    serializer = serializers.UploadHCDPDDataSerializer(data={})

    assert isinstance(serializer.fields['data'].child, serializers.UploadDPDAndExtractsSerializer)


def test__upload_dpd_serializer__fields_many():
    """Confirms that all fields have expected "many" attribute."""
    serializer = serializers.UploadHCDPDDataSerializer(data={})

    assert serializer.fields['data'].many is True


def test__upload_dpd_serializer__fields_required():
    """Confirms that all fields have expected "required" attribute."""
    serializer = serializers.UploadHCDPDDataSerializer(data={})

    assert serializer.fields['data'].required is True


def test__upload_dpd_data_serializer__maximum_valid_data():
    """Confirms validation for all possible fields."""
    serializer = serializers.UploadHCDPDDataSerializer(data=utils.UPLOAD_ALL_DATA)

    assert serializer.is_valid() is True


def test__upload_hcdpd_data_serializer__create__single_active_ingredient():
    """Tests create method for single active_ingredient item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'active_ingredient'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_active_ingredient_one_drug_code():
    """Tests create method for multiple active_ingredient items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'active_ingredient'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_active_ingredient_two_drug_code():
    """Tests create method for multiple active_ingredient items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'active_ingredient': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'active_ingredient': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'active_ingredient'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length + 2


def test__upload_hcdpd_data_serializer__create__single_biosimilar():
    """Tests create method for single biosimilar item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    biosimilar_length = models.OriginalBiosimilar.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['biosimilar'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'biosimilar': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'biosimilar'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalBiosimilar.objects.count() == biosimilar_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_biosimilar_one_drug_code():
    """Tests create method for multiple biosimilar items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    biosimilar_length = models.OriginalBiosimilar.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['biosimilar'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'biosimilar': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'biosimilar'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalBiosimilar.objects.count() == biosimilar_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_biosimilar_two_drug_code():
    """Tests create method for multiple biosimilar items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    biosimilar_length = models.OriginalBiosimilar.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['biosimilar'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'biosimilar': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'biosimilar': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'biosimilar'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalBiosimilar.objects.count() == biosimilar_length + 2


def test__upload_hcdpd_data_serializer__create__single_company():
    """Tests create method for single company item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    company_length = models.OriginalCompany.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['company'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'company': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'company'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalCompany.objects.count() == company_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_company_one_drug_code():
    """Tests create method for multiple company items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    company_length = models.OriginalCompany.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['company'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'company': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'company'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalCompany.objects.count() == company_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_company_two_drug_code():
    """Tests create method for multiple company items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    company_length = models.OriginalCompany.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['company'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'company': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'company': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'company'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalCompany.objects.count() == company_length + 2


def test__upload_hcdpd_data_serializer__create__single_drug_product():
    """Tests create method for single drug_product item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    drug_product_length = models.OriginalDrugProduct.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['drug_product'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'drug_product': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'drug_product'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalDrugProduct.objects.count() == drug_product_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_drug_product_one_drug_code():
    """Tests create method for multiple drug_product items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    drug_product_length = models.OriginalDrugProduct.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['drug_product'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'drug_product': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'drug_product'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalDrugProduct.objects.count() == drug_product_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_drug_product_two_drug_code():
    """Tests create method for multiple drug_product items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    drug_product_length = models.OriginalDrugProduct.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['drug_product'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'drug_product': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'drug_product': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'drug_product'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalDrugProduct.objects.count() == drug_product_length + 2


def test__upload_hcdpd_data_serializer__create__single_form():
    """Tests create method for single form item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    form_length = models.OriginalForm.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['form'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'form': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'form'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalForm.objects.count() == form_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_form_one_drug_code():
    """Tests create method for multiple form items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    form_length = models.OriginalForm.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['form'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'form': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'form'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalForm.objects.count() == form_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_form_two_drug_code():
    """Tests create method for multiple form items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    form_length = models.OriginalForm.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['form'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'form': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'form': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'form'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalForm.objects.count() == form_length + 2


def test__upload_hcdpd_data_serializer__create__single_inactive_product():
    """Tests create method for single inactive_product item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    inactive_product_length = models.OriginalInactiveProduct.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['inactive_product'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'inactive_product': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'inactive_product'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalInactiveProduct.objects.count() == inactive_product_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_inactive_product_one_drug_code():
    """Tests create method for multiple inactive_product items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    inactive_product_length = models.OriginalInactiveProduct.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['inactive_product'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'inactive_product': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'inactive_product'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalInactiveProduct.objects.count() == inactive_product_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_inactive_product_two_drug_code():
    """Tests create method for multiple inactive_product items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    inactive_product_length = models.OriginalInactiveProduct.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['inactive_product'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'inactive_product': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'inactive_product': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'inactive_product'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalInactiveProduct.objects.count() == inactive_product_length + 2


def test__upload_hcdpd_data_serializer__create__single_packaging():
    """Tests create method for single packaging item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    packaging_length = models.OriginalPackaging.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['packaging'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'packaging': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'packaging'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalPackaging.objects.count() == packaging_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_packaging_one_drug_code():
    """Tests create method for multiple packaging items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    packaging_length = models.OriginalPackaging.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['packaging'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'packaging': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'packaging'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalPackaging.objects.count() == packaging_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_packaging_two_drug_code():
    """Tests create method for multiple packaging items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    packaging_length = models.OriginalPackaging.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['packaging'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'packaging': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'packaging': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'packaging'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalPackaging.objects.count() == packaging_length + 2


def test__upload_hcdpd_data_serializer__create__single_pharmaceutical_standard():
    """Tests create method for single pharmaceutical_standard item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    pharmaceutical_standard_length = models.OriginalPharmaceuticalStandard.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['pharmaceutical_standard'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'pharmaceutical_standard': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'pharmaceutical_standard'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalPharmaceuticalStandard.objects.count() == pharmaceutical_standard_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_pharmaceutical_standard_one_drug_code():
    """Tests create method for multiple pharmaceutical_standard items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    pharmaceutical_standard_length = models.OriginalPharmaceuticalStandard.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['pharmaceutical_standard'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'pharmaceutical_standard': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'pharmaceutical_standard'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalPharmaceuticalStandard.objects.count() == pharmaceutical_standard_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_pharmaceutical_standard_two_drug_code():
    """Tests create method for multiple pharmaceutical_standard items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    pharmaceutical_standard_length = models.OriginalPharmaceuticalStandard.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['pharmaceutical_standard'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'pharmaceutical_standard': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'pharmaceutical_standard': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'pharmaceutical_standard'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalPharmaceuticalStandard.objects.count() == pharmaceutical_standard_length + 2


def test__upload_hcdpd_data_serializer__create__single_route():
    """Tests create method for single route item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    route_length = models.OriginalRoute.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['route'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'route': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'route'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalRoute.objects.count() == route_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_route_one_drug_code():
    """Tests create method for multiple route items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    route_length = models.OriginalRoute.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['route'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'route': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'route'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalRoute.objects.count() == route_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_route_two_drug_code():
    """Tests create method for multiple route items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    route_length = models.OriginalRoute.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['route'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'route': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'route': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'route'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalRoute.objects.count() == route_length + 2


def test__upload_hcdpd_data_serializer__create__single_schedule():
    """Tests create method for single schedule item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    schedule_length = models.OriginalSchedule.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['schedule'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'schedule': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'schedule'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalSchedule.objects.count() == schedule_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_schedule_one_drug_code():
    """Tests create method for multiple schedule items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    schedule_length = models.OriginalSchedule.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['schedule'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'schedule': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'schedule'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalSchedule.objects.count() == schedule_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_schedule_two_drug_code():
    """Tests create method for multiple schedule items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    schedule_length = models.OriginalSchedule.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['schedule'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'schedule': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'schedule': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'schedule'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalSchedule.objects.count() == schedule_length + 2


def test__upload_hcdpd_data_serializer__create__single_status():
    """Tests create method for single status item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    status_length = models.OriginalStatus.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['status'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'status': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'status'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalStatus.objects.count() == status_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_status_one_drug_code():
    """Tests create method for multiple status items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    status_length = models.OriginalStatus.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['status'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'status': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'status'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalStatus.objects.count() == status_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_status_two_drug_code():
    """Tests create method for multiple status items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    status_length = models.OriginalStatus.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['status'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'status': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'status': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'status'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalStatus.objects.count() == status_length + 2


def test__upload_hcdpd_data_serializer__create__single_therapeutic_class():
    """Tests create method for single therapeutic_class item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    therapeutic_class_length = models.OriginalTherapeuticClass.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['therapeutic_class'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'therapeutic_class': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'therapeutic_class'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalTherapeuticClass.objects.count() == therapeutic_class_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_therapeutic_class_one_drug_code():
    """Tests create method for multiple therapeutic_class items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    therapeutic_class_length = models.OriginalTherapeuticClass.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['therapeutic_class'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'therapeutic_class': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'therapeutic_class'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalTherapeuticClass.objects.count() == therapeutic_class_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_therapeutic_class_two_drug_code():
    """Tests create method for multiple therapeutic_class items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    therapeutic_class_length = models.OriginalTherapeuticClass.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['therapeutic_class'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'therapeutic_class': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'therapeutic_class': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'therapeutic_class'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalTherapeuticClass.objects.count() == therapeutic_class_length + 2


def test__upload_hcdpd_data_serializer__create__single_veterinary_species():
    """Tests create method for single veterinary_species item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    veterinary_species_length = models.OriginalVeterinarySpecies.objects.count()

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['veterinary_species'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'veterinary_species': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'veterinary_species'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalVeterinarySpecies.objects.count() == veterinary_species_length + 1


def test__upload_hcdpd_data_serializer__create__multiple_veterinary_species_one_drug_code():
    """Tests create method for multiple veterinary_species items with same drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    veterinary_species_length = models.OriginalVeterinarySpecies.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['veterinary_species'][0].copy()
    item_data_2 = item_data_1.copy()
    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'veterinary_species': [item_data_1, item_data_2],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'veterinary_species'
    assert message['message'][0]['drug_codes'] == [drug_code]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 1
    assert models.OriginalVeterinarySpecies.objects.count() == veterinary_species_length + 2


def test__upload_hcdpd_data_serializer__create__multiple_veterinary_species_two_drug_code():
    """Tests create method for multiple veterinary_species items with different drug code."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    veterinary_species_length = models.OriginalVeterinarySpecies.objects.count()

    # Setup data
    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['veterinary_species'][0].copy()
    drug_code_1 = item_data_1['drug_code']
    drug_code_2 = 2
    item_data_2 = item_data_1.copy()
    item_data_2['drug_code'] = drug_code_2

    data = {
        'data': [
            {
                'drug_code': drug_code_1,
                'extract_data': {
                    'veterinary_species': [item_data_1],
                },
            },
            {
                'drug_code': drug_code_2,
                'extract_data': {
                    'veterinary_species': [item_data_2],
                },

            }
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert message['status_code'] == 201
    assert len(message['message']) == 1
    assert message['message'][0]['file_type'] == 'veterinary_species'
    assert message['message'][0]['drug_codes'] == [drug_code_1, drug_code_2]

    # Confirm status code details
    assert status_code == 201

    # Confirm expected model creation
    assert models.DPD.objects.count() == dpd_length + 2
    assert models.OriginalVeterinarySpecies.objects.count() == veterinary_species_length + 2


def test__upload_hcdpd_data_serializer__create__confirm_old_data_deleted(hc_dpd_dpd):
    """Tests create method clears any existing data prior to updates."""
    # Create initial test models
    old_model = models.OriginalActiveIngredient.objects.create(drug_code=hc_dpd_dpd)
    old_pk = old_model.pk

    # Setup data
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, _ = serializer.create(serializer.validated_data)

    # Confirm old model is deleted
    assert models.OriginalActiveIngredient.objects.filter(pk=old_pk).exists() is False

    # Confirm new model exists
    new_drug_code = message['message'][0]['drug_codes'][0]
    new_dpd = models.DPD.objects.get(pk=new_drug_code)
    new_model = models.OriginalActiveIngredient.objects.get(drug_code=new_dpd)
    new_pk = new_model.pk
    assert models.OriginalActiveIngredient.objects.filter(pk=new_pk).exists() is True


@patch('hc_dpd.models.core.timezone.now')
def test__upload_hcdpd_data_serializer__create__confirm_update_occurs(timezone, hc_dpd_dpd):
    """Tests create method updates modified times as expected."""
    # Patch timezone return value for testing
    timezone_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    timezone.return_value = timezone_now

    # Setup data
    drug_code = hc_dpd_dpd.pk
    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    item_data['drug_code'] = drug_code
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data],
                },
            },
        ],
    }

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    serializer.create(serializer.validated_data)

    # Confirm modified time is updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified == timezone_now


def test__upload_hcdpd_data_serializer__create__invalid_model_data(hc_dpd_dpd):
    """Tests create method handles when invalid model data is submitted."""
    # Get initial model count
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    hc_dpd_dpd.original_active_ingredient_modified = None
    hc_dpd_dpd.save()

    item_data = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    item_data['drug_code'] = hc_dpd_dpd.pk
    item_data['active_ingredient_code'] = 'A' * 10

    drug_code = item_data['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data],
                },
            },
        ],
    }

    # Need to explicitly make this section a single transaction.
    # Unit tests are normally wrapped in one transaction and the
    # intentional DB failure will prevent any future DB queries
    # until the test completes.
    with transaction.atomic():
        serializer = serializers.UploadHCDPDDataSerializer(data=data)
        message, status_code = serializer.create(data)

    # Confirm message details
    assert message['status_code'] == 400
    assert message['errors']['field'] == {}
    assert len(message['errors']['non_field']) == 1

    error_message = message['errors']['non_field'][0]
    assert 'Could not complete upload' in error_message
    assert 'value too long for type character varying(6)' in error_message

    # Confirm status code details
    assert status_code == 400

    # Confirm models not created
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length

    # Confirm update time was not updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified is None


def test__upload_hcdpd_data_serializer__create__valid_and_invalid_data_one_type(hc_dpd_dpd):
    """Tests create method with valid & invalid data submitted in one extract type."""
    # Get initial model count
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    # Setup data
    hc_dpd_dpd.original_active_ingredient_modified = None
    hc_dpd_dpd.save()

    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    item_data_2 = item_data_1.copy()
    item_data_1['drug_code'] = hc_dpd_dpd.pk
    item_data_2['drug_code'] = hc_dpd_dpd.pk
    item_data_1['active_ingredient_code'] = 'A' * 10

    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data_1, item_data_2],
                },
            },
        ],
    }

    # Need to explicitly make this section a single transaction.
    # Unit tests are normally wrapped in one transaction and the
    # intentional DB failure will prevent any future DB queries
    # until the test completes.
    with transaction.atomic():
        serializer = serializers.UploadHCDPDDataSerializer(data=data)
        message, status_code = serializer.create(data)

    # Confirm message details
    assert message['status_code'] == 400
    assert message['errors']['field'] == {}
    assert len(message['errors']['non_field']) == 1

    error_message = message['errors']['non_field'][0]
    assert 'Could not complete upload' in error_message
    assert 'value too long for type character varying(6)' in error_message

    # Confirm status code details
    assert status_code == 400

    # Confirm models not created
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length

    # Confirm update time was not updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified is None


def test__upload_hcdpd_data_serializer__create__valid_and_invalid_data_two_type(hc_dpd_dpd):
    """Tests create method with valid & invalid data submitted in two extract type."""
    # Get initial model count
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()
    biosimilar_length = models.OriginalBiosimilar.objects.count()

    # Setup data
    hc_dpd_dpd.original_active_ingredient_modified = None
    hc_dpd_dpd.original_biosimilar_modified = None
    hc_dpd_dpd.save()

    item_data_1 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['active_ingredient'][0].copy()
    item_data_2 = utils.UPLOAD_ALL_DATA['data'][0]['extract_data']['biosimilar'][0].copy()
    item_data_1['drug_code'] = hc_dpd_dpd.pk
    item_data_2['drug_code'] = hc_dpd_dpd.pk
    item_data_1['active_ingredient_code'] = 'A' * 10

    drug_code = item_data_1['drug_code']
    data = {
        'data': [
            {
                'drug_code': drug_code,
                'extract_data': {
                    'active_ingredient': [item_data_1],
                    'biosimilar': [item_data_2],
                },
            },
        ],
    }

    # Need to explicitly make this section a single transaction.
    # Unit tests are normally wrapped in one transaction and the
    # intentional DB failure will prevent any future DB queries
    # until the test completes.
    with transaction.atomic():
        serializer = serializers.UploadHCDPDDataSerializer(data=data)
        message, status_code = serializer.create(data)

    # Confirm message details
    assert message['status_code'] == 400
    assert message['errors']['field'] == {}
    assert len(message['errors']['non_field']) == 1

    error_message = message['errors']['non_field'][0]
    assert 'Could not complete upload' in error_message
    assert 'value too long for type character varying(6)' in error_message

    # Confirm status code details
    assert status_code == 400

    # Confirm models not created
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length
    assert models.OriginalBiosimilar.objects.count() == biosimilar_length

    # Confirm update time was not updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified is None
    assert hc_dpd_dpd.original_biosimilar_modified is None


def test__upload_hcdpd_data_serializer__create__no_data():
    """Confirms error handling for no data submitted."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()

    # Setup data
    data = {
        'data': [
            {
                'drug_code': 1,
                'extract_data': {},
            },
        ],
    }

    # Need to explicitly make this section a single transaction.
    # Unit tests are normally wrapped in one transaction and the
    # intentional DB failure will prevent any future DB queries
    # until the test completes.
    with transaction.atomic():
        serializer = serializers.UploadHCDPDDataSerializer(data=data)
        message, status_code = serializer.create(data)

    # Confirm message details
    assert message['status_code'] == 422
    assert message['errors']['field'] == {}
    assert len(message['errors']['non_field']) == 1
    assert  message['errors']['non_field'] == ['No data submitted for upload.']

    # Confirm status code details
    assert status_code == 422

    # Confirm no models created
    assert models.DPD.objects.count() == dpd_length


def test__upload_hcdpd_data_serializer__update_exists():
    """Confirms update method exists."""
    serializer = serializers.UploadHCDPDDataSerializer(data={})

    assert serializer.update(None, {}) is None
