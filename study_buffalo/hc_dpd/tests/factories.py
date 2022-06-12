"""Factories for testing the HC DPD app."""
import factory

from hc_dpd import models


class DPDFactory(factory.django.DjangoModelFactory):
    """Factory to generate a DPD instance."""
    # Add 1 to sequence since it starts at 0 and drug_code must be > 1
    drug_code = factory.Sequence(lambda n: n + 1)

    class Meta:
        model = models.DPD


class OriginalActiveIngredientFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalActiveIngredient instance."""
    drug_code = factory.SubFactory(DPDFactory)
    active_ingredient_code = factory.Sequence(str)
    ingredient = factory.Sequence(lambda n: f'INGREDIENT {n}')
    ingredient_supplied_ind = 'I'
    strength = factory.Sequence(str)
    strength_unit = 'MG'
    strength_type = factory.Sequence(lambda n: f'STRENGTH TYPE {n}')
    dosage_value = factory.Sequence(str)
    base = 'N'
    dosage_unit = 'MG'
    notes = factory.Sequence(lambda n: f'NOTES {n}')
    ingredient_f = factory.Sequence(lambda n: f'INGREDIENT F {n}')
    strength_unit_f = 'MG F'
    strength_type_f = factory.Sequence(lambda n: f'STRENGTH TYPE F {n}')
    dosage_unit_f = 'MG F'

    class Meta:
        model = models.OriginalActiveIngredient


class OriginalBiosimilarFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalBiosimilar instance."""
    drug_code = factory.SubFactory(DPDFactory)
    biosimilar_code = factory.Sequence(str)
    biosimilar_type = factory.Sequence(lambda n: f'TYPE {n}')
    biosimilar_type_f = factory.Sequence(lambda n: f'TYPE F {n}')

    class Meta:
        model = models.OriginalBiosimilar


class OriginalCompanyFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalCompany instance."""
    drug_code = factory.SubFactory(DPDFactory)
    mfr_code = factory.Sequence(str)
    company_code = factory.Sequence(str)
    company_name = factory.Sequence(lambda n: f'NAME {n}')
    company_type = factory.Sequence(lambda n: f'TYPE {n}')
    address_mailing_flag = 'Y'
    address_billing_flag = 'Y'
    address_notification_flag = 'Y'
    address_other = 'N'
    suite_number = factory.Sequence(lambda n: f'SUITE {n}')
    street_name = factory.Sequence(lambda n: f'STREET {n}')
    city_name = factory.Sequence(lambda n: f'CITY {n}')
    province = factory.Sequence(lambda n: f'PROVINCE {n}')
    country = factory.Sequence(lambda n: f'COUNTRY {n}')
    postal_code = factory.Sequence(lambda n: f'POSTAL {n}')
    post_office_box = factory.Sequence(lambda n: f'POST {n}')
    province_f = factory.Sequence(lambda n: f'PROVINCE F {n}')
    country_f = factory.Sequence(lambda n: f'COUNTRY F {n}')

    class Meta:
        model = models.OriginalCompany


class OriginalDrugProductFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalDrugProduct instance."""
    drug_code = factory.SubFactory(DPDFactory)
    product_categorization = factory.Sequence(lambda n: f'CATEGORY {n}')
    class_e = factory.Sequence(lambda n: f'CLASS {n}')
    drug_identification_number = factory.Sequence(str)
    brand_name = factory.Sequence(lambda n: f'BRAND {n}')
    descriptor = factory.Sequence(lambda n: f'DESCRIPTOR {n}')
    pediatric_flag = 'N'
    accession_number = factory.Sequence(str)
    number_of_ais = factory.Sequence(str)
    last_update_date = '01-JAN-2000'
    ai_group_no = factory.Sequence(str)
    class_f = factory.Sequence(lambda n: f'CLASS F {n}')
    brand_name_f = factory.Sequence(lambda n: f'BRAND F {n}')
    descriptor_f = factory.Sequence(lambda n: f'DESCRIPTOR F {n}')

    class Meta:
        model = models.OriginalDrugProduct


class OriginalFormFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalForm instance."""
    drug_code = factory.SubFactory(DPDFactory)
    pharm_form_code = factory.Sequence(str)
    pharmaceutical_form = factory.Sequence(lambda n: f'FORM {n}')
    pharmaceutical_form_f = factory.Sequence(lambda n: f'FORM F {n}')

    class Meta:
        model = models.OriginalForm


class OriginalInactiveProductFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalInactiveProduct instance."""
    drug_code = factory.SubFactory(DPDFactory)
    drug_identification_number = factory.Sequence(str)
    brand_name = factory.Sequence(lambda n: f'NAME {n}')
    history_date = '01-JAN-2000'
    brand_name_f = factory.Sequence(lambda n: f'NAME F {n}')

    class Meta:
        model = models.OriginalInactiveProduct


class OriginalPackagingFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalPackaging instance."""
    drug_code = factory.SubFactory(DPDFactory)
    upc = factory.Sequence(lambda n: f'UPC {n}')
    package_size_unit = factory.Sequence(lambda n: f'UNIT {n}')
    package_type = factory.Sequence(lambda n: f'TYPE {n}')
    package_size = factory.Sequence(str)
    product_information = factory.Sequence(lambda n: f'PRODUCT {n}')
    package_size_unit_f = factory.Sequence(lambda n: f'UNIT F {n}')
    package_type_f = factory.Sequence(lambda n: f'TYPE F {n}')

    class Meta:
        model = models.OriginalPackaging


class OriginalPharmaceuticalStandardFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalPharmaceuticalStandard instance."""
    drug_code = factory.SubFactory(DPDFactory)
    pharmaceutical_std = factory.Sequence(lambda n: f'STD {n}')

    class Meta:
        model = models.OriginalPharmaceuticalStandard


class OriginalRouteFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalRoute instance."""
    drug_code = factory.SubFactory(DPDFactory)
    route_of_administration_code = factory.Sequence(str)
    route_of_administration = factory.Sequence(lambda n: f'ROUTE {n}')
    route_of_administration_f = factory.Sequence(lambda n: f'ROUTE F {n}')

    class Meta:
        model = models.OriginalRoute


class OriginalScheduleFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalSchedule instance."""
    drug_code = factory.SubFactory(DPDFactory)
    schedule = factory.Sequence(lambda n: f'SCHEDULE {n}')
    schedule_f = factory.Sequence(lambda n: f'SCHEDULE F {n}')

    class Meta:
        model = models.OriginalSchedule


class OriginalStatusFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalStatus instance."""
    drug_code = factory.SubFactory(DPDFactory)
    current_status_flag = 'A'
    status = factory.Sequence(lambda n: f'STATUS {n}')
    history_date = '01-JAN-2000'
    status_f = factory.Sequence(lambda n: f'STATUS F {n}')
    lot_number = factory.Sequence(lambda n: f'LOT {n}')
    expiration_date = '01-JAN-2001'

    class Meta:
        model = models.OriginalStatus


class OriginalTherapeuticClassFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalTherapeuticClass instance."""
    drug_code = factory.SubFactory(DPDFactory)
    tc_atc_number = factory.Sequence(lambda n: f'ATC {n}')
    tc_atc = factory.Sequence(lambda n: f'ATC TEXT {n}')
    tc_atc_f = factory.Sequence(lambda n: f'ATC TEXT F {n}')

    class Meta:
        model = models.OriginalTherapeuticClass


class OriginalVeterinarySpeciesFactory(factory.django.DjangoModelFactory):
    """Factory to generate an OriginalVeterinarySpecies instance."""
    drug_code = factory.SubFactory(DPDFactory)
    vet_species = factory.Sequence(lambda n: f'SPECIES {n}')
    vet_sub_species = factory.Sequence(lambda n: f'SUB SPECIES {n}')
    vet_species_f = factory.Sequence(lambda n: f'SPECIES F {n}')

    class Meta:
        model = models.OriginalVeterinarySpecies


class DPDChecksumActiveIngredientFactory(factory.django.DjangoModelFactory):
    """Factory to generate a DPDChecksum with OriginalActiveIngredient."""
    drug_code_start = 0
    drug_code_step = 100000
    extract_source = 'active_ingredient'

    ai_1 = factory.RelatedFactory(OriginalActiveIngredientFactory)
    ai_2 = factory.RelatedFactory(OriginalActiveIngredientFactory)

    class Meta:
        model = models.DPDChecksum


class SubBrandFactory(factory.django.DjangoModelFactory):
    """Factory to generate a SubBrand instance."""
    original = 'Original Brand 1'
    substitution = 'Sub Brand 1'

    class Meta:
        model = models.SubBrand
        django_get_or_create = ('original', 'substitution')


class SubBrandPendFactory(factory.django.DjangoModelFactory):
    """Factory to generate a SubBrandPend instance."""
    original = 'Original Brand 1 Pending'
    substitution = 'Sub Brand 1 Pending'

    class Meta:
        model = models.SubBrandPend
        django_get_or_create = ('original', 'substitution')
