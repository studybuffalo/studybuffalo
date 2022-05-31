"""Tests for Original models of HC DPD app."""
import pytest

from hc_dpd import models


pytestmark = pytest.mark.django_db


def test__active_ingredient__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalActiveIngredient model creation."""
    model_count = models.OriginalActiveIngredient.objects.count()

    models.OriginalActiveIngredient.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalActiveIngredient.objects.count() == model_count + 1


def test__active_ingredient__str(hc_dpd_dpd):
    """Confirms OriginalActiveIngredient __str__ output"""
    active_ingredient = models.OriginalActiveIngredient.objects.create(
        drug_code=hc_dpd_dpd,
        ingredient='A',
        active_ingredient_code='1',
    )

    assert str(active_ingredient) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__active_ingredient__max_lengths():
    """Tests OriginalActiveIngredient max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalActiveIngredient._meta.get_field('active_ingredient_code').max_length == 6
    assert models.OriginalActiveIngredient._meta.get_field('ingredient').max_length == 240
    assert models.OriginalActiveIngredient._meta.get_field('ingredient_supplied_ind').max_length == 1
    assert models.OriginalActiveIngredient._meta.get_field('strength').max_length == 20
    assert models.OriginalActiveIngredient._meta.get_field('strength_unit').max_length == 40
    assert models.OriginalActiveIngredient._meta.get_field('strength_type').max_length == 40
    assert models.OriginalActiveIngredient._meta.get_field('dosage_value').max_length == 20
    assert models.OriginalActiveIngredient._meta.get_field('base').max_length == 1
    assert models.OriginalActiveIngredient._meta.get_field('dosage_unit').max_length == 40
    assert models.OriginalActiveIngredient._meta.get_field('notes').max_length == 2000
    assert models.OriginalActiveIngredient._meta.get_field('ingredient_f').max_length == 400
    assert models.OriginalActiveIngredient._meta.get_field('strength_unit_f').max_length == 80
    assert models.OriginalActiveIngredient._meta.get_field('strength_type_f').max_length == 80
    assert models.OriginalActiveIngredient._meta.get_field('dosage_unit_f').max_length == 80


def test__active_ingredient__field_order():
    """Tests OriginalActiveIngredient field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'active_ingredient_code',
        'ingredient',
        'ingredient_supplied_ind',
        'strength',
        'strength_unit',
        'strength_type',
        'dosage_value',
        'base',
        'dosage_unit',
        'notes',
        'ingredient_f',
        'strength_unit_f',
        'strength_type_f',
        'dosage_unit_f',
    ]

    assert models.OriginalActiveIngredient.dpd_field_order() == expected_order


def test__biosimilar__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalBiosimilar model creation."""
    model_count = models.OriginalBiosimilar.objects.count()

    models.OriginalBiosimilar.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalBiosimilar.objects.count() == model_count + 1


def test__biosimilar__str(hc_dpd_dpd):
    """Confirms OriginalBiosimilar __str__ output"""
    biosimilar = models.OriginalBiosimilar.objects.create(
        drug_code=hc_dpd_dpd,
        biosimilar_code=1,
    )

    assert str(biosimilar) == f'1 [O; Drug Code {hc_dpd_dpd.pk}]'


def test__biosimilar__max_lengths():
    """Tests OriginalBiosimilar max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalBiosimilar._meta.get_field('biosimilar_type').max_length == 20
    assert models.OriginalBiosimilar._meta.get_field('biosimilar_type_f').max_length == 20


def test__biosimilar__field_order():
    """Tests OriginalBiosimilar field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'biosimilar_code',
        'biosimilar_type',
        'biosimilar_type_f',
    ]

    assert models.OriginalBiosimilar.dpd_field_order() == expected_order


def test__company__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalCompany model creation."""
    model_count = models.OriginalCompany.objects.count()

    models.OriginalCompany.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalCompany.objects.count() == model_count + 1


def test__company__str(hc_dpd_dpd):
    """Confirms OriginalCompany __str__ output"""
    active_ingredient = models.OriginalCompany.objects.create(
        drug_code=hc_dpd_dpd,
        company_name='A',
        company_code='1',
    )

    assert str(active_ingredient) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__company__max_lengths():
    """Tests OriginalCompany max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalCompany._meta.get_field('mfr_code').max_length == 5
    assert models.OriginalCompany._meta.get_field('company_name').max_length == 80
    assert models.OriginalCompany._meta.get_field('company_type').max_length == 40
    assert models.OriginalCompany._meta.get_field('address_mailing_flag').max_length == 1
    assert models.OriginalCompany._meta.get_field('address_billing_flag').max_length == 1
    assert models.OriginalCompany._meta.get_field('address_notification_flag').max_length == 1
    assert models.OriginalCompany._meta.get_field('address_other').max_length == 1
    assert models.OriginalCompany._meta.get_field('suite_number').max_length == 20
    assert models.OriginalCompany._meta.get_field('street_name').max_length == 80
    assert models.OriginalCompany._meta.get_field('city_name').max_length == 60
    assert models.OriginalCompany._meta.get_field('province').max_length == 40
    assert models.OriginalCompany._meta.get_field('country').max_length == 40
    assert models.OriginalCompany._meta.get_field('postal_code').max_length == 20
    assert models.OriginalCompany._meta.get_field('post_office_box').max_length == 15
    assert models.OriginalCompany._meta.get_field('province_f').max_length == 100
    assert models.OriginalCompany._meta.get_field('country_f').max_length == 100


def test__company__field_order():
    """Tests OriginalCompany field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'mfr_code',
        'company_code',
        'company_name',
        'company_type',
        'address_mailing_flag',
        'address_billing_flag',
        'address_notification_flag',
        'address_other',
        'suite_number',
        'street_name',
        'city_name',
        'province',
        'country',
        'postal_code',
        'post_office_box',
        'province_f',
        'country_f',
    ]

    assert models.OriginalCompany.dpd_field_order() == expected_order


def test__drug_product__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalDrugProduct model creation."""
    model_count = models.OriginalDrugProduct.objects.count()

    models.OriginalDrugProduct.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalDrugProduct.objects.count() == model_count + 1


def test__drug_product__str(hc_dpd_dpd):
    """Confirms OriginalDrugProduct __str__ output"""
    drug_product = models.OriginalDrugProduct.objects.create(
        drug_code=hc_dpd_dpd,
        brand_name='A',
        drug_identification_number='1',
    )

    assert str(drug_product) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__drug_product__max_lengths():
    """Tests OriginalDrugProduct max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalDrugProduct._meta.get_field('product_categorization').max_length == 80
    assert models.OriginalDrugProduct._meta.get_field('class_e').max_length == 40
    assert models.OriginalDrugProduct._meta.get_field('drug_identification_number').max_length == 29
    assert models.OriginalDrugProduct._meta.get_field('brand_name').max_length == 200
    assert models.OriginalDrugProduct._meta.get_field('descriptor').max_length == 150
    assert models.OriginalDrugProduct._meta.get_field('pediatric_flag').max_length == 1
    assert models.OriginalDrugProduct._meta.get_field('accession_number').max_length == 5
    assert models.OriginalDrugProduct._meta.get_field('number_of_ais').max_length == 10
    assert models.OriginalDrugProduct._meta.get_field('ai_group_no').max_length == 10
    assert models.OriginalDrugProduct._meta.get_field('class_f').max_length == 80
    assert models.OriginalDrugProduct._meta.get_field('brand_name_f').max_length == 300
    assert models.OriginalDrugProduct._meta.get_field('descriptor_f').max_length == 200


def test__drug_product__field_order():
    """Tests OriginalDrugProduct field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'product_categorization',
        'class_e',
        'drug_identification_number',
        'brand_name',
        'descriptor',
        'pediatric_flag',
        'accession_number',
        'number_of_ais',
        'last_update_date',
        'ai_group_no',
        'class_f',
        'brand_name_f',
        'descriptor_f',
    ]

    assert models.OriginalDrugProduct.dpd_field_order() == expected_order


def test__form__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalForm model creation."""
    model_count = models.OriginalForm.objects.count()

    models.OriginalForm.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalForm.objects.count() == model_count + 1


def test__form__str(hc_dpd_dpd):
    """Confirms OriginalForm __str__ output"""
    form = models.OriginalForm.objects.create(
        drug_code=hc_dpd_dpd,
        pharmaceutical_form='A',
        pharm_form_code=1,
    )

    assert str(form) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__form__max_lengths():
    """Tests OriginalForm max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalForm._meta.get_field('pharmaceutical_form').max_length == 40
    assert models.OriginalForm._meta.get_field('pharmaceutical_form_f').max_length == 80


def test__form__field_order():
    """Tests OriginalForm field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'pharm_form_code',
        'pharmaceutical_form',
        'pharmaceutical_form_f',
    ]

    assert models.OriginalForm.dpd_field_order() == expected_order


def test__inactive_product__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalInactiveProduct model creation."""
    model_count = models.OriginalInactiveProduct.objects.count()

    models.OriginalInactiveProduct.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalInactiveProduct.objects.count() == model_count + 1


def test__inactive_product__str(hc_dpd_dpd):
    """Confirms OriginalInactiveProduct __str__ output"""
    inactive_product = models.OriginalInactiveProduct.objects.create(
        drug_code=hc_dpd_dpd,
        brand_name='A',
        history_date='2000-01-01',
    )

    assert str(inactive_product) == f'A [2000-01-01] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__inactive_product__max_lengths():
    """Tests OriginalInactiveProduct max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalInactiveProduct._meta.get_field('drug_identification_number').max_length == 29
    assert models.OriginalInactiveProduct._meta.get_field('brand_name').max_length == 200


def test__inactive_product__field_order():
    """Tests OriginalInactiveProduct field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'drug_identification_number',
        'brand_name',
        'history_date',
    ]

    assert models.OriginalInactiveProduct.dpd_field_order() == expected_order


def test__packaging__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalPackaging model creation."""
    model_count = models.OriginalPackaging.objects.count()

    models.OriginalPackaging.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalPackaging.objects.count() == model_count + 1


def test__packaging__str(hc_dpd_dpd):
    """Confirms OriginalPackaging __str__ output"""
    active_ingredient = models.OriginalPackaging.objects.create(
        drug_code=hc_dpd_dpd,
        upc='A',
    )

    assert str(active_ingredient) == f'A [O; Drug Code {hc_dpd_dpd.pk}]'


def test__packaging__max_lengths():
    """Tests OriginalPackaging max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalPackaging._meta.get_field('upc').max_length == 12
    assert models.OriginalPackaging._meta.get_field('package_size_unit').max_length == 40
    assert models.OriginalPackaging._meta.get_field('package_type').max_length == 40
    assert models.OriginalPackaging._meta.get_field('package_size').max_length == 5
    assert models.OriginalPackaging._meta.get_field('product_information').max_length == 80
    assert models.OriginalPackaging._meta.get_field('package_size_unit_f').max_length == 80
    assert models.OriginalPackaging._meta.get_field('package_type_f').max_length == 80


def test__packaging__field_order():
    """Tests OriginalPackaging field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'upc',
        'package_size_unit',
        'package_type',
        'package_size',
        'product_information',
        'package_size_unit_f',
        'package_type_f',
    ]

    assert models.OriginalPackaging.dpd_field_order() == expected_order


def test__pharmaceutical_standard__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalPharmaceuticalStandard model creation."""
    model_count = models.OriginalPharmaceuticalStandard.objects.count()

    models.OriginalPharmaceuticalStandard.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalPharmaceuticalStandard.objects.count() == model_count + 1


def test__pharmaceutical_standard__str(hc_dpd_dpd):
    """Confirms OriginalPharmaceuticalStandard __str__ output"""
    pharmaceutical_standard = models.OriginalPharmaceuticalStandard.objects.create(
        drug_code=hc_dpd_dpd,
        pharmaceutical_std='A',
    )

    assert str(pharmaceutical_standard) == f'A [O; Drug Code {hc_dpd_dpd.pk}]'


def test__pharmaceutical_standard__max_lengths():
    """Tests OriginalPharmaceuticalStandard max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalPharmaceuticalStandard._meta.get_field('pharmaceutical_std').max_length == 40


def test__pharmaceutical_standard__field_order():
    """Tests OriginalPharmaceuticalStandard field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'pharmaceutical_std',
    ]

    assert models.OriginalPharmaceuticalStandard.dpd_field_order() == expected_order


def test__route__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalRoute model creation."""
    model_count = models.OriginalRoute.objects.count()

    models.OriginalRoute.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalRoute.objects.count() == model_count + 1


def test__route__str(hc_dpd_dpd):
    """Confirms OriginalRoute __str__ output"""
    route = models.OriginalRoute.objects.create(
        drug_code=hc_dpd_dpd,
        route_of_administration_code=1,
        route_of_administration='A',
    )

    assert str(route) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__route__max_lengths():
    """Tests OriginalRoute max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalRoute._meta.get_field('route_of_administration').max_length == 40
    assert models.OriginalRoute._meta.get_field('route_of_administration_f').max_length == 80


def test__route__field_order():
    """Tests OriginalRoute field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'route_of_administration_code',
        'route_of_administration',
        'route_of_administration_f',
    ]

    assert models.OriginalRoute.dpd_field_order() == expected_order


def test__schedule__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalSchedule model creation."""
    model_count = models.OriginalSchedule.objects.count()

    models.OriginalSchedule.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalSchedule.objects.count() == model_count + 1


def test__schedule__str(hc_dpd_dpd):
    """Confirms OriginalSchedule __str__ output"""
    schedule = models.OriginalSchedule.objects.create(
        drug_code=hc_dpd_dpd,
        schedule='A',
    )

    assert str(schedule) == f'A [O; Drug Code {hc_dpd_dpd.pk}]'


def test__schedule__max_lengths():
    """Tests OriginalSchedule max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalSchedule._meta.get_field('schedule').max_length == 40
    assert models.OriginalSchedule._meta.get_field('schedule_f').max_length == 160


def test__schedule__field_order():
    """Tests OriginalSchedule field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'schedule',
        'schedule_f',
    ]

    assert models.OriginalSchedule.dpd_field_order() == expected_order


def test__status__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalStatus model creation."""
    model_count = models.OriginalStatus.objects.count()

    models.OriginalStatus.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalStatus.objects.count() == model_count + 1


def test__status__str(hc_dpd_dpd):
    """Confirms OriginalStatus __str__ output"""
    status = models.OriginalStatus.objects.create(
        drug_code=hc_dpd_dpd,
        status='A',
        history_date='2000-01-01',
    )

    assert str(status) == f'A [2000-01-01] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__status__max_lengths():
    """Tests OriginalStatus max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalStatus._meta.get_field('current_status_flag').max_length == 1
    assert models.OriginalStatus._meta.get_field('status').max_length == 40
    assert models.OriginalStatus._meta.get_field('status_f').max_length == 80
    assert models.OriginalStatus._meta.get_field('lot_number').max_length == 50


def test__status__field_order():
    """Tests OriginalStatus field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'current_status_flag',
        'status',
        'history_date',
        'status_f',
        'lot_number',
        'expiration_date',
    ]

    assert models.OriginalStatus.dpd_field_order() == expected_order


def test__therapeutic_class__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalTherapeuticClass model creation."""
    model_count = models.OriginalTherapeuticClass.objects.count()

    models.OriginalTherapeuticClass.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalTherapeuticClass.objects.count() == model_count + 1


def test__therapeutic_class__str(hc_dpd_dpd):
    """Confirms OriginalTherapeuticClass __str__ output"""
    therapeutic_class = models.OriginalTherapeuticClass.objects.create(
        drug_code=hc_dpd_dpd,
        tc_atc='A',
        tc_atc_number='1',
    )

    assert str(therapeutic_class) == f'A [1] [O; Drug Code {hc_dpd_dpd.pk}]'


def test__therapeutic_class__max_lengths():
    """Tests OriginalTherapeuticClass max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalTherapeuticClass._meta.get_field('tc_atc_number').max_length == 8
    assert models.OriginalTherapeuticClass._meta.get_field('tc_atc').max_length == 120
    assert models.OriginalTherapeuticClass._meta.get_field('tc_atc_f').max_length == 240


def test__therapeutic_class__field_order():
    """Tests OriginalTherapeuticClass field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'tc_atc_number',
        'tc_atc',
        'tc_atc_f',
    ]

    assert models.OriginalTherapeuticClass.dpd_field_order() == expected_order


def test__veterinary_species__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal OriginalVeterinarySpecies model creation."""
    model_count = models.OriginalVeterinarySpecies.objects.count()

    models.OriginalVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.OriginalVeterinarySpecies.objects.count() == model_count + 1


def test__veterinary_species__str__without_sub_species(hc_dpd_dpd):
    """Confirms OriginalVeterinarySpecies __str__ output without sub species"""
    veterinary_species = models.OriginalVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
        vet_species='A',
    )

    assert str(veterinary_species) == f'A [O; Drug Code {hc_dpd_dpd.pk}]'


def test__veterinary_species__str__with_sub_species(hc_dpd_dpd):
    """Confirms OriginalVeterinarySpecies __str__ output with sub species"""
    veterinary_species = models.OriginalVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
        vet_species='A',
        vet_sub_species='B',
    )

    assert str(veterinary_species) == f'A - B [O; Drug Code {hc_dpd_dpd.pk}]'


def test__veterinary_species__max_lengths():
    """Tests OriginalVeterinarySpecies max lengths.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    assert models.OriginalVeterinarySpecies._meta.get_field('vet_species').max_length == 80
    assert models.OriginalVeterinarySpecies._meta.get_field('vet_sub_species').max_length == 80
    assert models.OriginalVeterinarySpecies._meta.get_field('vet_species_f').max_length == 160


def test__veterinary_species__field_order():
    """Tests OriginalVeterinarySpecies field_order.

        When updating this test, ensure values are independently
        entered based on HC DPD Data Extract Readme:
        https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html
    """  # pylint: disable=line-too-long
    expected_order = [
        'drug_code',
        'vet_species',
        'vet_sub_species',
        'vet_species_f',
    ]

    assert models.OriginalVeterinarySpecies.dpd_field_order() == expected_order
