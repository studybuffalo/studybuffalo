"""Models for formatted Drug Product Database content."""
from django.db import models


class FormattedActiveIngredient(models.Model):
    """Model representing the formatted QRYM_ACTIVE_INGREDIENTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    active_ingredient_code = models.CharField(
        blank=True,
        help_text='The formatted version of ACTIVE_INGREDIENT_CODE.',
        max_length=6,
        null=True,
    )
    ingredient = models.CharField(
        blank=True,
        help_text='The formatted version of INGREDIENT.',
        max_length=240,
        null=True,
    )
    ingredient_supplied_ind = models.CharField(
        blank=True,
        help_text='The formatted version of INGREDIENT_SUPPLIED_IND.',
        max_length=1,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        help_text='The formatted version of STRENGTH.',
        max_length=20,
        null=True,
    )
    strength_unit = models.CharField(
        blank=True,
        help_text='The formatted version of STRENGTH_UNIT.',
        max_length=40,
        null=True,
    )
    strength_type = models.CharField(
        blank=True,
        help_text='The formatted version of STRENGTH_TYPE.',
        max_length=40,
        null=True,
    )
    dosage_value = models.CharField(
        blank=True,
        help_text='The formatted version of DOSAGE_VALUE.',
        max_length=20,
        null=True,
    )
    base = models.CharField(
        blank=True,
        help_text='The formatted version of BASE.',
        max_length=1,
        null=True,
    )
    dosage_unit = models.CharField(
        blank=True,
        help_text='The formatted version of DOSAGE_UNIT.',
        max_length=40,
        null=True,
    )
    notes = models.CharField(
        blank=True,
        help_text='The formatted version of NOTES.',
        max_length=2000,
        null=True,
    )
    ingredient_f = models.CharField(
        blank=True,
        help_text='The formatted version of INGREDIENT_F.',
        max_length=400,
        null=True,
    )
    strength_unit_f = models.CharField(
        blank=True,
        help_text='The formatted version of STRENGTH_UNIT_F.',
        max_length=80,
        null=True,
    )
    strength_type_f = models.CharField(
        blank=True,
        help_text='The formatted version of STRENGTH_TYPE_F.',
        max_length=80,
        null=True,
    )
    dosage_unit_f = models.CharField(
        blank=True,
        help_text='The formatted version of DOSAGE_UNIT_F.',
        max_length=80,
        null=True,
    )


class FormattedBiosimilars(models.Model):
    """Model representing the formatted QRYM_BIOSIMILARS file.

        This extract is not present in the DPD Read Me File - field names
        and types were implied from extract data.
    """
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    biosimilar_code = models.PositiveIntegerField(
        blank=True,
        help_text='The formatted version of BIOSIMILAR_CODE.',
        null=True,
    )
    biosimilar_type = models.CharField(
        blank=True,
        help_text='The formatted version of BIOSIMILAR_TYPE.',
        max_length=20,
        null=True,
    )
    biosimilar_type_F = models.CharField(
        blank=True,
        help_text='The formatted version of BIOSIMILAR_TYPE_F.',
        max_length=20,
        null=True,
    )


class FormattedCompany(models.Model):
    """Model representing the formatted QRYM_COMPANIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    mfr_code = models.CharField(
        blank=True,
        help_text='The formatted version of MFR_CODE.',
        max_length=5,
        null=True,
    )
    company_code = models.PositiveIntegerField(
        blank=True,
        help_text='The formatted version of COMPANY_CODE.',
        null=True,
    )
    company_name = models.CharField(
        blank=True,
        help_text='The formatted version of COMPANY_NAME.',
        max_length=80,
        null=True,
    )
    company_type = models.CharField(
        blank=True,
        help_text='The formatted version of COMPANY_TYPE.',
        max_length=40,
        null=True,
    )
    address_mailing_flag = models.CharField(
        blank=True,
        help_text='The formatted version of ADDRESS_MAILING_FLAG.',
        max_length=1,
        null=True,
    )
    address_billing_flag = models.CharField(
        blank=True,
        help_text='The formatted version of ADDRESS_BILLING_FLAG.',
        max_length=1,
        null=True,
    )
    address_notification_flag = models.CharField(
        blank=True,
        help_text='The formatted version of ADDRESS_NOTIFICATION_FLAG.',
        max_length=1,
        null=True,
    )
    address_other = models.CharField(
        blank=True,
        help_text='The formatted version of ADDRESS_OTHER.',
        max_length=1,
        null=True,
    )
    suite_number = models.CharField(
        blank=True,
        help_text='The formatted version of SUITE_NUMBER.',
        max_length=20,
        null=True,
    )
    street_name = models.CharField(
        blank=True,
        help_text='The formatted version of STREET_NAME.',
        max_length=80,
        null=True,
    )
    city_name = models.CharField(
        blank=True,
        help_text='The formatted version of CITY_NAME.',
        max_length=60,
        null=True,
    )
    province = models.CharField(
        blank=True,
        help_text='The formatted version of PROVINCE.',
        max_length=40,
        null=True,
    )
    country = models.CharField(
        blank=True,
        help_text='The formatted version of COUNTRY.',
        max_length=40,
        null=True,
    )
    postal_code = models.CharField(
        blank=True,
        help_text='The formatted version of POSTAL_CODE.',
        max_length=20,
        null=True,
    )
    post_office_box = models.CharField(
        blank=True,
        help_text='The formatted version of POST_OFFICE_BOX.',
        max_length=15,
        null=True,
    )
    province_f = models.CharField(
        blank=True,
        help_text='The formatted version of PROVINCE_F.',
        max_length=100,
        null=True,
    )
    country_f = models.CharField(
        blank=True,
        help_text='The formatted version of COUNTRY_F.',
        max_length=100,
        null=True,
    )


class FormattedDrugProduct(models.Model):
    """Model representing the formatted QRYM_DRUG_PRODUCT file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    product_categorization = models.CharField(
        blank=True,
        help_text='The formatted version of PRODUCT_CATEGORIZATION.',
        max_length=80,
        null=True,
    )
    class_e = models.CharField(
        blank=True,
        help_text='The formatted version of CLASS.',
        max_length=40,
        null=True,
    )
    drug_identification_number = models.CharField(
        blank=True,
        help_text='The formatted version of DRUG_IDENTIFICATION_NUMBER.',
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        help_text='The formatted version of BRAND_NAME.',
        max_length=200,
        null=True,
    )
    descriptor = models.CharField(
        blank=True,
        help_text='The formatted version of DESCRIPTOR.',
        max_length=150,
        null=True,
    )
    pediatric_flag = models.CharField(
        blank=True,
        help_text='The formatted version of PEDIATRIC_FLAG.',
        max_length=1,
        null=True,
    )
    accession_number = models.CharField(
        blank=True,
        help_text='The formatted version of ACCESSION_NUMBER.',
        max_length=5,
        null=True,
    )
    number_of_ais = models.CharField(
        blank=True,
        help_text='The formatted version of NUMBER_OF_AIS.',
        max_length=10,
        null=True,
    )
    last_update_date = models.DateField(
        blank=True,
        help_text='The formatted version of LAST_UPDATE_DATE.',
        null=True,
    )
    ai_group_no = models.CharField(
        blank=True,
        help_text='The formatted version of AI_GROUP_NO.',
        max_length=10,
        null=True,
    )
    class_f = models.CharField(
        blank=True,
        help_text='The formatted version of CLASS_F.',
        max_length=80,
        null=True,
    )
    brand_name_f = models.CharField(
        blank=True,
        help_text='The formatted version of BRAND_NAME_F.',
        max_length=300,
        null=True,
    )
    descriptor_f = models.CharField(
        blank=True,
        help_text='The formatted version of DESCRIPTOR_F.',
        max_length=200,
        null=True,
    )


class FormattedForm(models.Model):
    """Model representing the formatted QRYM_FORM file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    pharm_form_code = models.PositiveIntegerField(
        blank=True,
        help_text='The formatted version of PHARM_FORM_CODE.',
        null=True,
    )
    pharmaceutical_form = models.CharField(
        blank=True,
        help_text='The formatted version of PHARMACEUTICAL_FORM.',
        max_length=40,
        null=True,
    )
    pharmaceutical_form_f = models.CharField(
        blank=True,
        help_text='The formatted version of PHARMACEUTICAL_FORM_F.',
        max_length=80,
        null=True,
    )


class FormattedInactiveProduct(models.Model):
    """Model representing the formatted QRYM_INACTIVE_PRODUCTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    drug_identification_number = models.CharField(
        blank=True,
        help_text='The formatted version of DRUG_IDENTIFICATION_NUMBER.',
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        help_text='The formatted version of BRAND_NAME.',
        max_length=200,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        help_text='The formatted version of HISTORY_DATE.',
        null=True,
    )


class FormattedPackaging(models.Model):
    """Model representing the formatted QRYM_Packaging file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    upc = models.CharField(
        blank=True,
        help_text='The formatted version of UPC.',
        max_length=12,
        null=True,
    )
    package_size_unit = models.CharField(
        blank=True,
        help_text='The formatted version of PACKAGE_SIZE_UNIT.',
        max_length=40,
        null=True,
    )
    package_type = models.CharField(
        blank=True,
        help_text='The formatted version of PACKAGE_TYPE.',
        max_length=40,
        null=True,
    )
    package_size = models.CharField(
        blank=True,
        help_text='The formatted version of PACKAGE_SIZE.',
        max_length=5,
        null=True,
    )
    product_information = models.CharField(
        blank=True,
        help_text='The formatted version of PRODUCT_INFORMATION.',
        max_length=80,
        null=True,
    )
    package_size_unit_f = models.CharField(
        blank=True,
        help_text='The formatted version of PACKAGE_SIZE_UNIT_F.',
        max_length=80,
        null=True,
    )
    package_type_f = models.CharField(
        blank=True,
        help_text='The formatted version of PACKAGE_TYPE_F.',
        max_length=80,
        null=True,
    )


class FormattedPharmaceuticalStandard(models.Model):
    """Model representing the formatted QRYM_PHARMACEUTICAL_STD file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    pharmaceutical_std = models.CharField(
        blank=True,
        help_text='The formatted version of PHARMACEUTICAL_STD.',
        max_length=40,
        null=True,
    )


class FormattedRoute(models.Model):
    """Model representing the formatted QRYM_ROUTE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    route_of_administration_code = models.PositiveIntegerField(
        blank=True,
        help_text='The formatted version of ROUTE_OF_ADMINISTRATION_CODE.',
        null=True,
    )
    route_of_administration = models.CharField(
        blank=True,
        help_text='The formatted version of ROUTE_OF_ADMINISTRATION.',
        max_length=40,
        null=True,
    )
    route_of_administration_f = models.CharField(
        blank=True,
        help_text='The formatted version of ROUTE_OF_ADMINISTRATION_F.',
        max_length=80,
        null=True,
    )


class FormattedSchedule(models.Model):
    """Model representing the formatted QRYM_SCHEDULE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    schedule = models.CharField(
        blank=True,
        help_text='The formatted version of SCHEDULE.',
        max_length=40,
        null=True,
    )
    schedule_f = models.CharField(
        blank=True,
        help_text='The formatted version of SCHEDULE_F.',
        max_length=160,
        null=True,
    )


class FormattedStatus(models.Model):
    """Model representing the formatted QRYM_STATUS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    current_status_flag = models.CharField(
        blank=True,
        help_text='The formatted version of CURRENT_STATUS_FLAG.',
        max_length=1,
        null=True,
    )
    status = models.CharField(
        blank=True,
        help_text='The formatted version of STATUS.',
        max_length=40,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        help_text='The formatted version of HISTORY_DATE.',
        null=True,
    )
    status_f = models.CharField(
        blank=True,
        help_text='The formatted version of STATUS_F.',
        max_length=80,
        null=True,
    )
    lot_number = models.CharField(
        blank=True,
        help_text='The formatted version of LOT_NUMBER.',
        max_length=50,
        null=True,
    )
    expiration_date = models.DateField(
        blank=True,
        help_text='The formatted version of EXPIRATION_DATE.',
        null=True,
    )


class FormattedTherapeuticClass(models.Model):
    """Model representing the formatted QRYM_THERAPEUTIC_CLASS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    tc_atc_number = models.CharField(
        blank=True,
        help_text='The formatted version of TC_ATC_NUMBER.',
        max_length=8,
        null=True,
    )
    tc_atc = models.CharField(
        blank=True,
        help_text='The formatted version of TC_ATC.',
        max_length=120,
        null=True,
    )
    tc_atc_f = models.CharField(
        blank=True,
        help_text='The formatted version of TC_ATC_F.',
        max_length=240,
        null=True,
    )


class FormattedVeterinarySpecies(models.Model):
    """Model representing the formatted QRYM_VETERINARY_SPECIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
    )
    vet_species = models.CharField(
        blank=True,
        help_text='The formatted version of VET_SPECIES.',
        max_length=80,
        null=True,
    )
    vet_sub_species = models.CharField(
        blank=True,
        help_text='The formatted version of VET_SUB_SPECIES.',
        max_length=80,
        null=True,
    )
    vet_species_f = models.CharField(
        blank=True,
        help_text='The formatted version of VET_SPECIES_F.',
        max_length=160,
        null=True,
    )
