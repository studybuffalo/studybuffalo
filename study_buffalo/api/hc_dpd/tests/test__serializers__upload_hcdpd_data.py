"""Tests for the HC DPD API serializers."""
# pylint: disable=protected-access, too-many-lines
from datetime import datetime
from unittest.mock import patch

import pytz
import pytest

from hc_dpd import models

from api.hc_dpd import serializers
from api.hc_dpd.tests import utils


pytestmark = pytest.mark.django_db


def test__upload_hcdpd_data_serializer__fields():
    """Confirms that all fields are matched to proper serializers."""
    data = {}
    serializer = serializers.UploadHCDPDDataSerializer(
        data=data
    )

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


def test__upload_hcdpd_data_serializer__maximum_valid_data():
    """Confirms validation for all possible fields."""
    serializer = serializers.UploadHCDPDDataSerializer(data=utils.UPLOAD_ALL_DATA)

    assert serializer.is_valid() is True


def test__upload_hcdpd_data_serializer__create__single_active_ingredient():
    """Tests create method for single active_ingredient item."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    data = {'active_ingredient': [utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'active_ingredient'
    assert message[0]['drug_code'] == 1

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
    data = {'active_ingredient': [
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'active_ingredient'
    assert message[0]['drug_code'] == 1

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
    data = {'active_ingredient': [
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
    ]}
    data['active_ingredient'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'active_ingredient'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'biosimilar': [utils.UPLOAD_ALL_DATA['biosimilar'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'biosimilar'
    assert message[0]['drug_code'] == 1

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
    data = {'biosimilar': [
        utils.UPLOAD_ALL_DATA['biosimilar'][0].copy(),
        utils.UPLOAD_ALL_DATA['biosimilar'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'biosimilar'
    assert message[0]['drug_code'] == 1

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
    data = {'biosimilar': [
        utils.UPLOAD_ALL_DATA['biosimilar'][0].copy(),
        utils.UPLOAD_ALL_DATA['biosimilar'][0].copy(),
    ]}
    data['biosimilar'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'biosimilar'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'company': [utils.UPLOAD_ALL_DATA['company'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'company'
    assert message[0]['drug_code'] == 1

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
    data = {'company': [
        utils.UPLOAD_ALL_DATA['company'][0].copy(),
        utils.UPLOAD_ALL_DATA['company'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'company'
    assert message[0]['drug_code'] == 1

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
    data = {'company': [
        utils.UPLOAD_ALL_DATA['company'][0].copy(),
        utils.UPLOAD_ALL_DATA['company'][0].copy(),
    ]}
    data['company'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'company'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'drug_product': [utils.UPLOAD_ALL_DATA['drug_product'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'drug_product'
    assert message[0]['drug_code'] == 1

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
    data = {'drug_product': [
        utils.UPLOAD_ALL_DATA['drug_product'][0].copy(),
        utils.UPLOAD_ALL_DATA['drug_product'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'drug_product'
    assert message[0]['drug_code'] == 1

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
    data = {'drug_product': [
        utils.UPLOAD_ALL_DATA['drug_product'][0].copy(),
        utils.UPLOAD_ALL_DATA['drug_product'][0].copy(),
    ]}
    data['drug_product'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'drug_product'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'form': [utils.UPLOAD_ALL_DATA['form'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'form'
    assert message[0]['drug_code'] == 1

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
    data = {'form': [
        utils.UPLOAD_ALL_DATA['form'][0].copy(),
        utils.UPLOAD_ALL_DATA['form'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'form'
    assert message[0]['drug_code'] == 1

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
    data = {'form': [
        utils.UPLOAD_ALL_DATA['form'][0].copy(),
        utils.UPLOAD_ALL_DATA['form'][0].copy(),
    ]}
    data['form'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'form'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'inactive_product': [utils.UPLOAD_ALL_DATA['inactive_product'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'inactive_product'
    assert message[0]['drug_code'] == 1

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
    data = {'inactive_product': [
        utils.UPLOAD_ALL_DATA['inactive_product'][0].copy(),
        utils.UPLOAD_ALL_DATA['inactive_product'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'inactive_product'
    assert message[0]['drug_code'] == 1

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
    data = {'inactive_product': [
        utils.UPLOAD_ALL_DATA['inactive_product'][0].copy(),
        utils.UPLOAD_ALL_DATA['inactive_product'][0].copy(),
    ]}
    data['inactive_product'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'inactive_product'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'packaging': [utils.UPLOAD_ALL_DATA['packaging'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'packaging'
    assert message[0]['drug_code'] == 1

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
    data = {'packaging': [
        utils.UPLOAD_ALL_DATA['packaging'][0].copy(),
        utils.UPLOAD_ALL_DATA['packaging'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'packaging'
    assert message[0]['drug_code'] == 1

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
    data = {'packaging': [
        utils.UPLOAD_ALL_DATA['packaging'][0].copy(),
        utils.UPLOAD_ALL_DATA['packaging'][0].copy(),
    ]}
    data['packaging'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'packaging'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'pharmaceutical_standard': [utils.UPLOAD_ALL_DATA['pharmaceutical_standard'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'pharmaceutical_standard'
    assert message[0]['drug_code'] == 1

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
    data = {'pharmaceutical_standard': [
        utils.UPLOAD_ALL_DATA['pharmaceutical_standard'][0].copy(),
        utils.UPLOAD_ALL_DATA['pharmaceutical_standard'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'pharmaceutical_standard'
    assert message[0]['drug_code'] == 1

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
    data = {'pharmaceutical_standard': [
        utils.UPLOAD_ALL_DATA['pharmaceutical_standard'][0].copy(),
        utils.UPLOAD_ALL_DATA['pharmaceutical_standard'][0].copy(),
    ]}
    data['pharmaceutical_standard'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'pharmaceutical_standard'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'route': [utils.UPLOAD_ALL_DATA['route'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'route'
    assert message[0]['drug_code'] == 1

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
    data = {'route': [
        utils.UPLOAD_ALL_DATA['route'][0].copy(),
        utils.UPLOAD_ALL_DATA['route'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'route'
    assert message[0]['drug_code'] == 1

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
    data = {'route': [
        utils.UPLOAD_ALL_DATA['route'][0].copy(),
        utils.UPLOAD_ALL_DATA['route'][0].copy(),
    ]}
    data['route'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'route'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'schedule': [utils.UPLOAD_ALL_DATA['schedule'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'schedule'
    assert message[0]['drug_code'] == 1

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
    data = {'schedule': [
        utils.UPLOAD_ALL_DATA['schedule'][0].copy(),
        utils.UPLOAD_ALL_DATA['schedule'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'schedule'
    assert message[0]['drug_code'] == 1

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
    data = {'schedule': [
        utils.UPLOAD_ALL_DATA['schedule'][0].copy(),
        utils.UPLOAD_ALL_DATA['schedule'][0].copy(),
    ]}
    data['schedule'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'schedule'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'status': [utils.UPLOAD_ALL_DATA['status'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'status'
    assert message[0]['drug_code'] == 1

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
    data = {'status': [
        utils.UPLOAD_ALL_DATA['status'][0].copy(),
        utils.UPLOAD_ALL_DATA['status'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'status'
    assert message[0]['drug_code'] == 1

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
    data = {'status': [
        utils.UPLOAD_ALL_DATA['status'][0].copy(),
        utils.UPLOAD_ALL_DATA['status'][0].copy(),
    ]}
    data['status'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'status'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'therapeutic_class': [utils.UPLOAD_ALL_DATA['therapeutic_class'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'therapeutic_class'
    assert message[0]['drug_code'] == 1

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
    data = {'therapeutic_class': [
        utils.UPLOAD_ALL_DATA['therapeutic_class'][0].copy(),
        utils.UPLOAD_ALL_DATA['therapeutic_class'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'therapeutic_class'
    assert message[0]['drug_code'] == 1

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
    data = {'therapeutic_class': [
        utils.UPLOAD_ALL_DATA['therapeutic_class'][0].copy(),
        utils.UPLOAD_ALL_DATA['therapeutic_class'][0].copy(),
    ]}
    data['therapeutic_class'][1]['drug_code'] = 2
    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'therapeutic_class'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'veterinary_species': [utils.UPLOAD_ALL_DATA['veterinary_species'][0].copy()]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'veterinary_species'
    assert message[0]['drug_code'] == 1

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
    data = {'veterinary_species': [
        utils.UPLOAD_ALL_DATA['veterinary_species'][0].copy(),
        utils.UPLOAD_ALL_DATA['veterinary_species'][0].copy(),
    ]}

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'veterinary_species'
    assert message[0]['drug_code'] == 1

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
    data = {'veterinary_species': [
        utils.UPLOAD_ALL_DATA['veterinary_species'][0].copy(),
        utils.UPLOAD_ALL_DATA['veterinary_species'][0].copy(),
    ]}
    data['veterinary_species'][1]['drug_code'] = 2

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 2
    assert message[0]['status_code'] == 201
    assert message[0]['file_type'] == 'veterinary_species'
    assert 1 in [message[0]['drug_code'], message[1]['drug_code']]
    assert 2 in [message[0]['drug_code'], message[1]['drug_code']]

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
    data = {'active_ingredient': [utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy()]}
    data['active_ingredient'][0]['drug_code'] = hc_dpd_dpd.pk

    serializer = serializers.UploadHCDPDDataSerializer(data=data)

    serializer.is_valid()
    print(serializer.errors)
    assert serializer.is_valid()

    message, _ = serializer.create(serializer.validated_data)

    # Confirm old model is deleted
    assert models.OriginalActiveIngredient.objects.filter(pk=old_pk).exists() is False

    # Confirm new model exists
    new_pk = message[0]['id']
    assert models.OriginalActiveIngredient.objects.filter(pk=new_pk).exists() is True


@patch('hc_dpd.models.core.timezone.now')
def test__upload_hcdpd_data_serializer__create__confirm_update_occurs(timezone, hc_dpd_dpd):
    """Tests create method updates modified times as expected."""
    # Patch timezone return value for testing
    timezone_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    timezone.return_value = timezone_now

    # Setup data
    data = {'active_ingredient': [utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy()]}
    data['active_ingredient'][0]['drug_code'] = hc_dpd_dpd.pk

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
    data = {'active_ingredient': [utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy()]}
    data['active_ingredient'][0]['drug_code'] = hc_dpd_dpd.pk
    data['active_ingredient'][0]['active_ingredient_code'] = 'A' * 10

    serializer = serializers.UploadHCDPDDataSerializer(data=data)
    message, status_code = serializer.create(data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 400

    error_message = str(message[0]['errors'])
    assert 'Could not create entry' in error_message
    assert '\'active_ingredient_code\': \'AAAAAAAAAA\'' in error_message
    assert 'value too long for type character varying(6)' in error_message

    # Confirm status code details
    assert status_code == 400

    # Confirm models not created
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length

    # Confirm update time was not updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified is None


@patch('hc_dpd.models.core.timezone.now')
def test__upload_hcdpd_data_serializer__create__valid_and_invalid_data(timezone, hc_dpd_dpd):
    """Tests create method handles when both valid & invalid data is submitted."""
    # Patch timezone return value for testing
    timezone_now = datetime(2000, 1, 1, tzinfo=pytz.utc)
    timezone.return_value = timezone_now

    # Get initial model count
    active_ingredient_length = models.OriginalActiveIngredient.objects.count()

    # Setup data
    hc_dpd_dpd.original_active_ingredient_modified = None
    hc_dpd_dpd.save()
    data = {'active_ingredient': [
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
        utils.UPLOAD_ALL_DATA['active_ingredient'][0].copy(),
    ]}
    print(id(data['active_ingredient'][0]['active_ingredient_code']))
    print(id(data['active_ingredient'][1]['active_ingredient_code']))
    data['active_ingredient'][0]['drug_code'] = hc_dpd_dpd.pk
    data['active_ingredient'][0]['active_ingredient_code'] = 'A' * 10
    data['active_ingredient'][1]['drug_code'] = hc_dpd_dpd.pk
    print(data)
    serializer = serializers.UploadHCDPDDataSerializer(data=data)
    message, status_code = serializer.create(data)

    # Confirm message details
    print(message)
    assert len(message) == 2
    assert 400 in [message[0]['status_code'], message[1]['status_code']]
    assert 201 in [message[0]['status_code'], message[1]['status_code']]

    # Confirm status code details
    assert status_code == 207

    # Confirm only one model created
    assert models.OriginalActiveIngredient.objects.count() == active_ingredient_length + 1

    # Confirm modified time is updated
    hc_dpd_dpd.refresh_from_db()
    assert hc_dpd_dpd.original_active_ingredient_modified == timezone_now


def test__upload_hcdpd_data_serializer__create__no_data():
    """Confirms error handling for no data submitted."""
    # Get initial model count
    dpd_length = models.DPD.objects.count()

    serializer = serializers.UploadHCDPDDataSerializer(data={})

    assert serializer.is_valid()

    message, status_code = serializer.create(serializer.validated_data)

    # Confirm message details
    assert len(message) == 1
    assert message[0]['status_code'] == 400
    assert message[0]['errors'] == ['No data submitted for upload.']

    # Confirm status code details
    assert status_code == 400

    # Confirm no models created
    assert models.DPD.objects.count() == dpd_length


def test__upload_hcdpd_data_serializer__update_exists():
    """Confirms update method exists."""
    serializer = serializers.UploadHCDPDDataSerializer(data={})

    try:
        serializer.update(None, None)
    except AttributeError:
        assert False

    assert True


def test__upload_hcdpd_data_serializer__group_upload_data__one_code():
    """Confirms expected output when one drug code provided."""
    data = [
        {'drug_code': 1, 'value': 'A'},
        {'drug_code': 1, 'value': 'B'},
    ]
    grouped = serializers.UploadHCDPDDataSerializer._group_upload_data(data)

    assert grouped == {1: data}


def test__upload_hcdpd_data_serializer__group_upload_data__two_code():
    """Confirms expected output when two drug code provided."""
    data = [
        {'drug_code': 1, 'value': 'A'},
        {'drug_code': 1, 'value': 'B'},
        {'drug_code': 2, 'value': 'C'},
        {'drug_code': 2, 'value': 'D'},
    ]
    grouped = serializers.UploadHCDPDDataSerializer._group_upload_data(data)

    assert grouped == {1: [data[0], data[1]], 2: [data[2], data[3]]}
