"""Tests for Utility functions of HC DPD app."""
from hc_dpd import models, utils

def test__extract_names():
    """Tests for expected values for extract constants."""
    assert utils.ACTIVE_INGREDIENT == 'active_ingredient'
    assert utils.BIOSIMILAR == 'biosimilar'
    assert utils.COMPANY == 'company'
    assert utils.DRUG_PRODUCT == 'drug_product'
    assert utils.FORM == 'form'
    assert utils.INACTIVE_PRODUCT == 'inactive_product'
    assert utils.PACKAGING == 'packaging'
    assert utils.PHARMACEUTICAL_STANDARD == 'pharmaceutical_standard'
    assert utils.ROUTE == 'route'
    assert utils.SCHEDULE == 'schedule'
    assert utils.STATUS == 'status'
    assert utils.THERAPUETIC_CLASS == 'therapeutic_class'
    assert utils.VETERINARY_SPECIES == 'veterinary_species'


def test__standard_to_original_mapping():
    """Tests that dictionary maps to expected models."""
    dictionary = utils.standard_to_original_model()

    assert dictionary[utils.ACTIVE_INGREDIENT] == models.OriginalActiveIngredient
    assert dictionary[utils.BIOSIMILAR] == models.OriginalBiosimilar
    assert dictionary[utils.COMPANY] == models.OriginalCompany
    assert dictionary[utils.DRUG_PRODUCT] == models.OriginalDrugProduct
    assert dictionary[utils.FORM] == models.OriginalForm
    assert dictionary[utils.PACKAGING] == models.OriginalPackaging
    assert dictionary[utils.PHARMACEUTICAL_STANDARD] == models.OriginalPharmaceuticalStandard
    assert dictionary[utils.ROUTE] == models.OriginalRoute
    assert dictionary[utils.SCHEDULE] == models.OriginalSchedule
    assert dictionary[utils.STATUS] == models.OriginalStatus
    assert dictionary[utils.THERAPUETIC_CLASS] == models.OriginalTherapeuticClass
    assert dictionary[utils.VETERINARY_SPECIES] == models.OriginalVeterinarySpecies
