"""Utility functions, classes, and references for the HC DPD app."""
from . import models


# Standard references to use as keys for HC DPD files/tables
ACTIVE_INGREDIENT = 'active_ingredient'
BIOSIMILAR = 'biosimilar'
COMPANY = 'company'
DRUG_PRODUCT = 'drug_product'
FORM = 'form'
INACTIVE_PRODUCT = 'inactive_product'
PACKAGING = 'packaging'
PHARMACEUTICAL_STANDARD = 'pharmaceutical_standard'
ROUTE = 'route'
SCHEDULE = 'schedule'
STATUS = 'status'
THERAPUETIC_CLASS = 'therapeutic_class'
VETERINARY_SPECIES = 'veterinary_species'


# Dictionary mapping serializer field name to Django model
def standard_to_original_model():
    """Mapping between standard naming and original models.

        Has to be called as function as models may not be
        initialized when function is imported into other
        modules.
    """
    return {
        ACTIVE_INGREDIENT: models.OriginalActiveIngredient,
        BIOSIMILAR: models.OriginalBiosimilar,
        COMPANY: models.OriginalCompany,
        DRUG_PRODUCT: models.OriginalDrugProduct,
        FORM: models.OriginalForm,
        INACTIVE_PRODUCT: models.OriginalInactiveProduct,
        PACKAGING: models.OriginalPackaging,
        PHARMACEUTICAL_STANDARD: models.OriginalPharmaceuticalStandard,
        ROUTE: models.OriginalRoute,
        SCHEDULE: models.OriginalSchedule,
        STATUS: models.OriginalStatus,
        THERAPUETIC_CLASS: models.OriginalTherapeuticClass,
        VETERINARY_SPECIES: models.OriginalVeterinarySpecies,
    }
