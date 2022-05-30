"""Tests for the HC DPD API serializers."""
import pytest

from rest_framework.serializers import IntegerField

from api.hc_dpd import serializers


pytestmark = pytest.mark.django_db


def test__active_ingredient_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.ActiveIngredientSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__active_ingredient_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.ActiveIngredientSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__active_ingredient_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'active_ingredient_code': '1234567'}
    serializer = serializers.ActiveIngredientSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__active_ingredient_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.ActiveIngredientSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__biosimilar_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.BiosimilarSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__biosimilar_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.BiosimilarSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__biosimilar_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'biosimilar_code': 'ABC'}
    serializer = serializers.BiosimilarSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__biosimilar_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.BiosimilarSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__company_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.CompanySerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__company_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.CompanySerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__company_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'mfr_code': '1234567'}
    serializer = serializers.CompanySerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__company_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.CompanySerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__drug_product_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.DrugProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__drug_product_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.DrugProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__drug_product_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'pediatric_flag': '1234567'}
    serializer = serializers.DrugProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__drug_product_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.DrugProductSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__form_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.FormSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__form_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.FormSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__form_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'pharm_form_code': 'ABC'}
    serializer = serializers.FormSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__form_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.FormSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__inactive_product_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.InactiveProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__inactive_product_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.InactiveProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__inactive_product_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'history_date': 'ABC'}
    serializer = serializers.InactiveProductSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__inactive_product_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.InactiveProductSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__packaging_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.PackagingSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__packaging_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.PackagingSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__packaging_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'package_size': '1234567'}
    serializer = serializers.PackagingSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__packaging_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.PackagingSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__pharmaceutical_standard_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.PharmaceuticalStandardSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__pharmaceutical_standard_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.PharmaceuticalStandardSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__pharmaceutical_standard_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'pharmaceutical_std': 'A' * 50}
    serializer = serializers.PharmaceuticalStandardSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__pharmaceutical_standard_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.PharmaceuticalStandardSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__route_serializer_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.RouteSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__route_serializer_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.RouteSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__route_serializer_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'route_of_administration_code': 'A'}
    serializer = serializers.RouteSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__route_serializer_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.RouteSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__schedule_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.ScheduleSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__schedule_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.ScheduleSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__schedule_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'schedule': 'A' * 50}
    serializer = serializers.ScheduleSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__schedule_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.ScheduleSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__status_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.StatusSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__status_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.StatusSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__status_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'current_status_flag': '1234567'}
    serializer = serializers.StatusSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__status_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.StatusSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__therapeutic_class_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.TherapeuticClassSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__therapeutic_class_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.TherapeuticClassSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__therapeutic_class_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'tc_atc_number': '123456789'}
    serializer = serializers.TherapeuticClassSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__therapeutic_class_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.TherapeuticClassSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__veterinary_species_serializer__valid():
    """Tests that correct data validates as expected."""
    data = {'drug_code': 1}
    serializer = serializers.VeterinarySpeciesSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is True


def test__veterinary_species_serializer__invalid_drug_code():
    """Tests that incorrect drug code validates as expected."""
    data = {'drug_code': 0}
    serializer = serializers.VeterinarySpeciesSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__veterinary_species_serializer__invalid_model_field():
    """Tests that incorrect model field validates as expected."""
    data = {'drug_code': 1, 'vet_species': 'A' * 100}
    serializer = serializers.VeterinarySpeciesSerializer(data=data)

    # Confirm data is valid
    assert serializer.is_valid() is False


def test__veterinary_species_serializer__drug_code_updated():
    """Tests that serializer replaces drug_code FK with Integer field."""
    data = {'drug_code': 0}
    serializer = serializers.VeterinarySpeciesSerializer(data=data)

    assert isinstance(serializer.fields['drug_code'], IntegerField)


def test__checksum_list_parameter_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.ChecksumListParameterSerializer(data={})

    try:
        serializer.create(None)
    except AttributeError:
        assert False

    assert True


def test__checksum_list_parameter_serializer__update_exists():
    """Confirms update method exists."""
    serializer = serializers.ChecksumListParameterSerializer(data={})

    try:
        serializer.update(None, None)
    except AttributeError:
        assert False

    assert True


def test__checksum_test_serializer__create_exists():
    """Confirms create method exists."""
    serializer = serializers.ChecksumTestSerializer(data={})

    try:
        serializer.create(None)
    except AttributeError:
        assert False

    assert True


def test__checksum_test_serializer__update_exists():
    """Confirms update method exists."""
    serializer = serializers.ChecksumTestSerializer(data={})

    try:
        serializer.update(None, None)
    except AttributeError:
        assert False

    assert True


def test__checksum_test_serializer__test_checksum__no_data():
    """Confirms method returns nothing on no data."""
    data = {}
    serializer = serializers.ChecksumTestSerializer(data=data)

    assert serializer.is_valid() is True

    checksum = serializer.test_checksum()

    assert not checksum


def test__checksum_test_serializer__test_checksum__one_field():
    """Confirms method returns one checksum when one field provided."""
    data = {
        'biosimilar': [
            {'drug_code': 1, 'biosimilar_code': 1, 'biosimilar_type': 'A', 'biosimilar_type_f': 'B'},
            {'drug_code': 2, 'biosimilar_code': 2, 'biosimilar_type': 'C', 'biosimilar_type_f': 'D'},
            {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E', 'biosimilar_type_f': 'F'},
        ]
    }
    serializer = serializers.ChecksumTestSerializer(data=data)

    assert serializer.is_valid() is True

    checksum = serializer.test_checksum()

    # Confirm 1 key in dictionary
    assert len(checksum) == 1
    assert 'biosimilar' in checksum

    # Confirm checksum string returned as expected
    assert checksum['biosimilar']['server_checksum_string'] == '11AB22CD33EF'

    # Confirm a 10 character checksum returned
    assert len(str(checksum['biosimilar']['server_checksum'])) == 10


def test__checksum_test_serializer__test_checksum__two_field():
    """Confirms method returns two checksums when two field provided."""
    data = {
        'biosimilar': [
            {'drug_code': 1, 'biosimilar_code': 1, 'biosimilar_type': 'A', 'biosimilar_type_f': 'B'},
            {'drug_code': 2, 'biosimilar_code': 2, 'biosimilar_type': 'C', 'biosimilar_type_f': 'D'},
            {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E', 'biosimilar_type_f': 'F'},
        ],
        'schedule': [
            {'drug_code': 4, 'schedule': 'G', 'schedule_f': 'H'},
            {'drug_code': 5, 'schedule': 'I', 'schedule_f': 'J'},
            {'drug_code': 6, 'schedule': 'K', 'schedule_f': 'L'},
        ]
    }
    serializer = serializers.ChecksumTestSerializer(data=data)

    assert serializer.is_valid() is True

    checksum = serializer.test_checksum()

    # Confirm 2 keys in dictionary
    assert len(checksum) == 2
    assert 'biosimilar' in checksum
    assert 'schedule' in checksum

    # Confirm checksum string returned as expected
    assert checksum['biosimilar']['server_checksum_string'] == '11AB22CD33EF'
    assert checksum['schedule']['server_checksum_string'] == '4GH5IJ6KL'

    # Confirm a 10 character checksum returned
    assert len(str(checksum['biosimilar']['server_checksum'])) == 10
    assert len(str(checksum['schedule']['server_checksum'])) == 10


def test__checksum_test_serializer__compile_checksum_string__no_data():
    """Confirms method returns empty string when no data provided."""
    data = []
    serializer = serializers.ChecksumTestSerializer(data=data)

    checksum_string = serializer.compile_checksum_string(data, [])

    # Confirm string result
    assert checksum_string == ''


def test__checksum_test_serializer__compile_checksum_string__all_fields():
    """Confirms method returns expected string when all dict keys match field list."""
    data = [
        {'drug_code': 1, 'biosimilar_code': 1, 'biosimilar_type': 'A', 'biosimilar_type_f': 'B'},
        {'drug_code': 2, 'biosimilar_code': 2, 'biosimilar_type': 'C', 'biosimilar_type_f': 'D'},
        {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E', 'biosimilar_type_f': 'F'},
    ]
    field_order = ['drug_code', 'biosimilar_code', 'biosimilar_type', 'biosimilar_type_f']
    serializer = serializers.ChecksumTestSerializer(data={})

    checksum_string = serializer.compile_checksum_string(data, field_order)

    # Confirm string result
    assert checksum_string == '11AB22CD33EF'


def test__checksum_test_serializer__compile_checksum_string__some_fields():
    """Confirms method returns expected string when only some dict keys match field list."""
    data = [
        {'drug_code': 1, 'biosimilar_code': 1, 'biosimilar_type': 'A'},
        {'drug_code': 2, 'biosimilar_code': 2, 'biosimilar_type': 'C'},
        {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E'},
    ]
    field_order = ['drug_code', 'biosimilar_code', 'biosimilar_type', 'biosimilar_type_f']
    serializer = serializers.ChecksumTestSerializer(data={})

    checksum_string = serializer.compile_checksum_string(data, field_order)

    # Confirm string result
    assert checksum_string == '11A22C33E'


def test__checksum_test_serializer__valid_drug_code_order():
    """Confirms serializer passes data with proper drug_code order."""
    data = {
        'biosimilar': [
            {'drug_code': 1, 'biosimilar_code': 1, 'biosimilar_type': 'A', 'biosimilar_type_f': 'B'},
            {'drug_code': 2, 'biosimilar_code': 2, 'biosimilar_type': 'C', 'biosimilar_type_f': 'D'},
            {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E', 'biosimilar_type_f': 'F'},
        ]
    }
    serializer = serializers.ChecksumTestSerializer(data=data)

    assert serializer.is_valid() is True


def test__checksum_test_serializer__invalid_drug_code_order():
    """Confirms serializer fails data with invalid drug_code order."""
    data = {
        'biosimilar': [
            {'drug_code': 2, 'biosimilar_code': 1, 'biosimilar_type': 'A', 'biosimilar_type_f': 'B'},
            {'drug_code': 1, 'biosimilar_code': 2, 'biosimilar_type': 'C', 'biosimilar_type_f': 'D'},
            {'drug_code': 3, 'biosimilar_code': 3, 'biosimilar_type': 'E', 'biosimilar_type_f': 'F'},
        ]
    }
    serializer = serializers.ChecksumTestSerializer(data=data)

    assert serializer.is_valid() is False

    # Confirm error details
    errors = serializer.errors

    assert 'non_field_errors' in errors
    assert len(errors['non_field_errors']) == 1
    assert 'biosimilar error: ' in errors['non_field_errors'][0]
