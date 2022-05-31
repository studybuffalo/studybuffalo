"""Tests for Formatted models of HC DPD app."""
import pytest

from hc_dpd import models


pytestmark = pytest.mark.django_db


def test__active_ingredient__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedActiveIngredient model creation."""
    model_count = models.FormattedActiveIngredient.objects.count()

    models.FormattedActiveIngredient.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedActiveIngredient.objects.count() == model_count + 1


def test__active_ingredient__str(hc_dpd_dpd):
    """Confirms FormattedActiveIngredient __str__ output"""
    active_ingredient = models.FormattedActiveIngredient.objects.create(
        drug_code=hc_dpd_dpd,
        ingredient='A',
        active_ingredient_code='1',
    )

    assert str(active_ingredient) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__active_ingredient__max_lengths():
    """Tests FormattedActiveIngredient max lengths."""
    assert models.FormattedActiveIngredient._meta.get_field('active_ingredient_code').max_length == 6
    assert models.FormattedActiveIngredient._meta.get_field('ingredient').max_length == 240
    assert models.FormattedActiveIngredient._meta.get_field('ingredient_supplied_ind').max_length == 1
    assert models.FormattedActiveIngredient._meta.get_field('strength').max_length == 20
    assert models.FormattedActiveIngredient._meta.get_field('strength_unit').max_length == 40
    assert models.FormattedActiveIngredient._meta.get_field('strength_type').max_length == 40
    assert models.FormattedActiveIngredient._meta.get_field('dosage_value').max_length == 20
    assert models.FormattedActiveIngredient._meta.get_field('base').max_length == 1
    assert models.FormattedActiveIngredient._meta.get_field('dosage_unit').max_length == 40
    assert models.FormattedActiveIngredient._meta.get_field('notes').max_length == 2000
    assert models.FormattedActiveIngredient._meta.get_field('ingredient_f').max_length == 400
    assert models.FormattedActiveIngredient._meta.get_field('strength_unit_f').max_length == 80
    assert models.FormattedActiveIngredient._meta.get_field('strength_type_f').max_length == 80
    assert models.FormattedActiveIngredient._meta.get_field('dosage_unit_f').max_length == 80


def test__biosimilar__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedBiosimilar model creation."""
    model_count = models.FormattedBiosimilar.objects.count()

    models.FormattedBiosimilar.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedBiosimilar.objects.count() == model_count + 1


def test__biosimilar__str(hc_dpd_dpd):
    """Confirms FormattedBiosimilar __str__ output"""
    biosimilar = models.FormattedBiosimilar.objects.create(
        drug_code=hc_dpd_dpd,
        biosimilar_code=1,
    )

    assert str(biosimilar) == f'1 [F; Drug Code {hc_dpd_dpd.pk}]'


def test__biosimilar__max_lengths():
    """Tests FormattedBiosimilar max lengths."""
    assert models.FormattedBiosimilar._meta.get_field('biosimilar_type').max_length == 20
    assert models.FormattedBiosimilar._meta.get_field('biosimilar_type_f').max_length == 20


def test__company__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedCompany model creation."""
    model_count = models.FormattedCompany.objects.count()

    models.FormattedCompany.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedCompany.objects.count() == model_count + 1


def test__company__str(hc_dpd_dpd):
    """Confirms FormattedCompany __str__ output"""
    active_ingredient = models.FormattedCompany.objects.create(
        drug_code=hc_dpd_dpd,
        company_name='A',
        company_code='1',
    )

    assert str(active_ingredient) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__company__max_lengths():
    """Tests FormattedCompany max lengths."""
    assert models.FormattedCompany._meta.get_field('mfr_code').max_length == 5
    assert models.FormattedCompany._meta.get_field('company_name').max_length == 80
    assert models.FormattedCompany._meta.get_field('company_type').max_length == 40
    assert models.FormattedCompany._meta.get_field('address_mailing_flag').max_length == 1
    assert models.FormattedCompany._meta.get_field('address_billing_flag').max_length == 1
    assert models.FormattedCompany._meta.get_field('address_notification_flag').max_length == 1
    assert models.FormattedCompany._meta.get_field('address_other').max_length == 1
    assert models.FormattedCompany._meta.get_field('suite_number').max_length == 20
    assert models.FormattedCompany._meta.get_field('street_name').max_length == 80
    assert models.FormattedCompany._meta.get_field('city_name').max_length == 60
    assert models.FormattedCompany._meta.get_field('province').max_length == 40
    assert models.FormattedCompany._meta.get_field('country').max_length == 40
    assert models.FormattedCompany._meta.get_field('postal_code').max_length == 20
    assert models.FormattedCompany._meta.get_field('post_office_box').max_length == 15
    assert models.FormattedCompany._meta.get_field('province_f').max_length == 100
    assert models.FormattedCompany._meta.get_field('country_f').max_length == 100


def test__drug_product__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedDrugProduct model creation."""
    model_count = models.FormattedDrugProduct.objects.count()

    models.FormattedDrugProduct.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedDrugProduct.objects.count() == model_count + 1


def test__drug_product__str(hc_dpd_dpd):
    """Confirms FormattedDrugProduct __str__ output"""
    drug_product = models.FormattedDrugProduct.objects.create(
        drug_code=hc_dpd_dpd,
        brand_name='A',
        drug_identification_number='1',
    )

    assert str(drug_product) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__drug_product__max_lengths():
    """Tests FormattedDrugProduct max lengths."""
    assert models.FormattedDrugProduct._meta.get_field('product_categorization').max_length == 80
    assert models.FormattedDrugProduct._meta.get_field('class_e').max_length == 40
    assert models.FormattedDrugProduct._meta.get_field('drug_identification_number').max_length == 29
    assert models.FormattedDrugProduct._meta.get_field('brand_name').max_length == 200
    assert models.FormattedDrugProduct._meta.get_field('descriptor').max_length == 150
    assert models.FormattedDrugProduct._meta.get_field('pediatric_flag').max_length == 1
    assert models.FormattedDrugProduct._meta.get_field('accession_number').max_length == 5
    assert models.FormattedDrugProduct._meta.get_field('number_of_ais').max_length == 10
    assert models.FormattedDrugProduct._meta.get_field('ai_group_no').max_length == 10
    assert models.FormattedDrugProduct._meta.get_field('class_f').max_length == 80
    assert models.FormattedDrugProduct._meta.get_field('brand_name_f').max_length == 300
    assert models.FormattedDrugProduct._meta.get_field('descriptor_f').max_length == 200


def test__form__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedForm model creation."""
    model_count = models.FormattedForm.objects.count()

    models.FormattedForm.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedForm.objects.count() == model_count + 1


def test__form__str(hc_dpd_dpd):
    """Confirms FormattedForm __str__ output"""
    form = models.FormattedForm.objects.create(
        drug_code=hc_dpd_dpd,
        pharmaceutical_form='A',
        pharm_form_code=1,
    )

    assert str(form) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__form__max_lengths():
    """Tests FormattedForm max lengths."""
    assert models.FormattedForm._meta.get_field('pharmaceutical_form').max_length == 40
    assert models.FormattedForm._meta.get_field('pharmaceutical_form_f').max_length == 80


def test__inactive_product__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedInactiveProduct model creation."""
    model_count = models.FormattedInactiveProduct.objects.count()

    models.FormattedInactiveProduct.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedInactiveProduct.objects.count() == model_count + 1


def test__inactive_product__str(hc_dpd_dpd):
    """Confirms FormattedInactiveProduct __str__ output"""
    inactive_product = models.FormattedInactiveProduct.objects.create(
        drug_code=hc_dpd_dpd,
        brand_name='A',
        history_date='2000-01-01',
    )

    assert str(inactive_product) == f'A [2000-01-01] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__inactive_product__max_lengths():
    """Tests FormattedInactiveProduct max lengths."""
    assert models.FormattedInactiveProduct._meta.get_field('drug_identification_number').max_length == 29
    assert models.FormattedInactiveProduct._meta.get_field('brand_name').max_length == 200


def test__packaging__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedPackaging model creation."""
    model_count = models.FormattedPackaging.objects.count()

    models.FormattedPackaging.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedPackaging.objects.count() == model_count + 1


def test__packaging__str(hc_dpd_dpd):
    """Confirms FormattedPackaging __str__ output"""
    active_ingredient = models.FormattedPackaging.objects.create(
        drug_code=hc_dpd_dpd,
        upc='A',
    )

    assert str(active_ingredient) == f'A [F; Drug Code {hc_dpd_dpd.pk}]'


def test__packaging__max_lengths():
    """Tests FormattedPackaging max lengths."""
    assert models.FormattedPackaging._meta.get_field('upc').max_length == 12
    assert models.FormattedPackaging._meta.get_field('package_size_unit').max_length == 40
    assert models.FormattedPackaging._meta.get_field('package_type').max_length == 40
    assert models.FormattedPackaging._meta.get_field('package_size').max_length == 5
    assert models.FormattedPackaging._meta.get_field('product_information').max_length == 80
    assert models.FormattedPackaging._meta.get_field('package_size_unit_f').max_length == 80
    assert models.FormattedPackaging._meta.get_field('package_type_f').max_length == 80


def test__pharmaceutical_standard__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedPharmaceuticalStandard model creation."""
    model_count = models.FormattedPharmaceuticalStandard.objects.count()

    models.FormattedPharmaceuticalStandard.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedPharmaceuticalStandard.objects.count() == model_count + 1


def test__pharmaceutical_standard__str(hc_dpd_dpd):
    """Confirms FormattedPharmaceuticalStandard __str__ output"""
    pharmaceutical_standard = models.FormattedPharmaceuticalStandard.objects.create(
        drug_code=hc_dpd_dpd,
        pharmaceutical_std='A',
    )

    assert str(pharmaceutical_standard) == f'A [F; Drug Code {hc_dpd_dpd.pk}]'


def test__pharmaceutical_standard__max_lengths():
    """Tests FormattedPharmaceuticalStandard max lengths."""
    assert models.FormattedPharmaceuticalStandard._meta.get_field('pharmaceutical_std').max_length == 40


def test__route__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedRoute model creation."""
    model_count = models.FormattedRoute.objects.count()

    models.FormattedRoute.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedRoute.objects.count() == model_count + 1


def test__route__str(hc_dpd_dpd):
    """Confirms FormattedRoute __str__ output"""
    route = models.FormattedRoute.objects.create(
        drug_code=hc_dpd_dpd,
        route_of_administration_code=1,
        route_of_administration='A',
    )

    assert str(route) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__route__max_lengths():
    """Tests FormattedRoute max lengths."""
    assert models.FormattedRoute._meta.get_field('route_of_administration').max_length == 40
    assert models.FormattedRoute._meta.get_field('route_of_administration_f').max_length == 80


def test__schedule__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedSchedule model creation."""
    model_count = models.FormattedSchedule.objects.count()

    models.FormattedSchedule.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedSchedule.objects.count() == model_count + 1


def test__schedule__str(hc_dpd_dpd):
    """Confirms FormattedSchedule __str__ output"""
    schedule = models.FormattedSchedule.objects.create(
        drug_code=hc_dpd_dpd,
        schedule='A',
    )

    assert str(schedule) == f'A [F; Drug Code {hc_dpd_dpd.pk}]'


def test__schedule__max_lengths():
    """Tests FormattedSchedule max lengths."""
    assert models.FormattedSchedule._meta.get_field('schedule').max_length == 40
    assert models.FormattedSchedule._meta.get_field('schedule_f').max_length == 160


def test__status__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedStatus model creation."""
    model_count = models.FormattedStatus.objects.count()

    models.FormattedStatus.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedStatus.objects.count() == model_count + 1


def test__status__str(hc_dpd_dpd):
    """Confirms FormattedStatus __str__ output"""
    status = models.FormattedStatus.objects.create(
        drug_code=hc_dpd_dpd,
        status='A',
        history_date='2000-01-01',
    )

    assert str(status) == f'A [2000-01-01] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__status__max_lengths():
    """Tests FormattedStatus max lengths."""
    assert models.FormattedStatus._meta.get_field('current_status_flag').max_length == 1
    assert models.FormattedStatus._meta.get_field('status').max_length == 40
    assert models.FormattedStatus._meta.get_field('status_f').max_length == 80
    assert models.FormattedStatus._meta.get_field('lot_number').max_length == 50


def test__therapeutic_class__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedTherapeuticClass model creation."""
    model_count = models.FormattedTherapeuticClass.objects.count()

    models.FormattedTherapeuticClass.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedTherapeuticClass.objects.count() == model_count + 1


def test__therapeutic_class__str(hc_dpd_dpd):
    """Confirms FormattedTherapeuticClass __str__ output"""
    therapeutic_class = models.FormattedTherapeuticClass.objects.create(
        drug_code=hc_dpd_dpd,
        tc_atc='A',
        tc_atc_number='1',
    )

    assert str(therapeutic_class) == f'A [1] [F; Drug Code {hc_dpd_dpd.pk}]'


def test__therapeutic_class__max_lengths():
    """Tests FormattedTherapeuticClass max lengths."""
    assert models.FormattedTherapeuticClass._meta.get_field('tc_atc_number').max_length == 8
    assert models.FormattedTherapeuticClass._meta.get_field('tc_atc').max_length == 120
    assert models.FormattedTherapeuticClass._meta.get_field('tc_atc_f').max_length == 240


def test__veterinary_species__minimal_model_creation(hc_dpd_dpd):
    """Tests minimal FormattedVeterinarySpecies model creation."""
    model_count = models.FormattedVeterinarySpecies.objects.count()

    models.FormattedVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
    )

    assert models.FormattedVeterinarySpecies.objects.count() == model_count + 1


def test__veterinary_species__str__without_sub_species(hc_dpd_dpd):
    """Confirms FormattedVeterinarySpecies __str__ output without sub species"""
    veterinary_species = models.FormattedVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
        vet_species='A',
    )

    assert str(veterinary_species) == f'A [F; Drug Code {hc_dpd_dpd.pk}]'


def test__veterinary_species__str__with_sub_species(hc_dpd_dpd):
    """Confirms FormattedVeterinarySpecies __str__ output with sub species"""
    veterinary_species = models.FormattedVeterinarySpecies.objects.create(
        drug_code=hc_dpd_dpd,
        vet_species='A',
        vet_sub_species='B',
    )

    assert str(veterinary_species) == f'A - B [F; Drug Code {hc_dpd_dpd.pk}]'


def test__veterinary_species__max_lengths():
    """Tests FormattedVeterinarySpecies max lengths."""
    assert models.FormattedVeterinarySpecies._meta.get_field('vet_species').max_length == 80
    assert models.FormattedVeterinarySpecies._meta.get_field('vet_sub_species').max_length == 80
    assert models.FormattedVeterinarySpecies._meta.get_field('vet_species_f').max_length == 160
