"""Models for original Drug Product Database content."""
from django.db import models


class OriginalActiveIngredient(models.Model):
    """Model representing the QRYM_ACTIVE_INGREDIENTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_active_ingredients',
    )
    active_ingredient_code = models.CharField(
        blank=True,
        help_text='The ACTIVE_INGREDIENT_CODE entry for this item.',
        max_length=6,
        null=True,
    )
    ingredient = models.CharField(
        blank=True,
        help_text='The INGREDIENT entry for this item.',
        max_length=240,
        null=True,
    )
    ingredient_supplied_ind = models.CharField(
        blank=True,
        help_text='The INGREDIENT_SUPPLIED_IND entry for this item.',
        max_length=1,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        help_text='The STRENGTH entry for this item.',
        max_length=20,
        null=True,
    )
    strength_unit = models.CharField(
        blank=True,
        help_text='The STRENGTH_UNIT entry for this item.',
        max_length=40,
        null=True,
    )
    strength_type = models.CharField(
        blank=True,
        help_text='The STRENGTH_TYPE entry for this item.',
        max_length=40,
        null=True,
    )
    dosage_value = models.CharField(
        blank=True,
        help_text='The DOSAGE_VALUE entry for this item.',
        max_length=20,
        null=True,
    )
    base = models.CharField(
        blank=True,
        help_text='The BASE entry for this item.',
        max_length=1,
        null=True,
    )
    dosage_unit = models.CharField(
        blank=True,
        help_text='The DOSAGE_UNIT entry for this item.',
        max_length=40,
        null=True,
    )
    notes = models.CharField(
        blank=True,
        help_text='The NOTES entry for this item.',
        max_length=2000,
        null=True,
    )
    ingredient_f = models.CharField(
        blank=True,
        help_text='The INGREDIENT_F entry for this item.',
        max_length=400,
        null=True,
    )
    strength_unit_f = models.CharField(
        blank=True,
        help_text='The STRENGTH_UNIT_F entry for this item.',
        max_length=80,
        null=True,
    )
    strength_type_f = models.CharField(
        blank=True,
        help_text='The STRENGTH_TYPE_F entry for this item.',
        max_length=80,
        null=True,
    )
    dosage_unit_f = models.CharField(
        blank=True,
        help_text='The DOSAGE_UNIT_F entry for this item.',
        max_length=80,
        null=True,
    )

    # Additional attributes
    field_order = [
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


class OriginalBiosimilar(models.Model):
    """Model representing the QRYM_BIOSIMILARS file.

        This extract is not present in the DPD Read Me File - field names
        and types were implied from extract data.
    """
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_biosimilars',
    )
    biosimilar_code = models.PositiveIntegerField(
        blank=True,
        help_text='The BIOSIMILAR_CODE entry for this item.',
        null=True,
    )
    biosimilar_type = models.CharField(
        blank=True,
        help_text='The BIOSIMILAR_TYPE entry for this item.',
        max_length=20,
        null=True,
    )
    biosimilar_type_f = models.CharField(
        blank=True,
        help_text='The BIOSIMILAR_TYPE_F entry for this item.',
        max_length=20,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'biosimilar_code',
        'biosimilar_type',
        'biosimilar_type_f',
    ]


class OriginalCompany(models.Model):
    """Model representing QRYM_COMPANIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_companies',
    )
    mfr_code = models.CharField(
        blank=True,
        help_text='The MFR_CODE entry for this item.',
        max_length=5,
        null=True,
    )
    company_code = models.PositiveIntegerField(
        blank=True,
        help_text='The COMPANY_CODE entry for this item.',
        null=True,
    )
    company_name = models.CharField(
        blank=True,
        help_text='The COMPANY_NAME entry for this item.',
        max_length=80,
        null=True,
    )
    company_type = models.CharField(
        blank=True,
        help_text='The COMPANY_TYPE entry for this item.',
        max_length=40,
        null=True,
    )
    address_mailing_flag = models.CharField(
        blank=True,
        help_text='The ADDRESS_MAILING_FLAG entry for this item.',
        max_length=1,
        null=True,
    )
    address_billing_flag = models.CharField(
        blank=True,
        help_text='The ADDRESS_BILLING_FLAG entry for this item.',
        max_length=1,
        null=True,
    )
    address_notification_flag = models.CharField(
        blank=True,
        help_text='The ADDRESS_NOTIFICATION_FLAG entry for this item.',
        max_length=1,
        null=True,
    )
    address_other = models.CharField(
        blank=True,
        help_text='The ADDRESS_OTHER entry for this item.',
        max_length=1,
        null=True,
    )
    suite_number = models.CharField(
        blank=True,
        help_text='The SUITE_NUMBER entry for this item.',
        max_length=20,
        null=True,
    )
    street_name = models.CharField(
        blank=True,
        help_text='The STREET_NAME entry for this item.',
        max_length=80,
        null=True,
    )
    city_name = models.CharField(
        blank=True,
        help_text='The CITY_NAME entry for this item.',
        max_length=60,
        null=True,
    )
    province = models.CharField(
        blank=True,
        help_text='The PROVINCE entry for this item.',
        max_length=40,
        null=True,
    )
    country = models.CharField(
        blank=True,
        help_text='The COUNTRY entry for this item.',
        max_length=40,
        null=True,
    )
    postal_code = models.CharField(
        blank=True,
        help_text='The POSTAL_CODE entry for this item.',
        max_length=20,
        null=True,
    )
    post_office_box = models.CharField(
        blank=True,
        help_text='The POST_OFFICE_BOX entry for this item.',
        max_length=15,
        null=True,
    )
    province_f = models.CharField(
        blank=True,
        help_text='The PROVINCE_F entry for this item.',
        max_length=100,
        null=True,
    )
    country_f = models.CharField(
        blank=True,
        help_text='The COUNTRY_F entry for this item.',
        max_length=100,
        null=True,
    )

    # Additional attributes
    field_order = [
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


class OriginalDrugProduct(models.Model):
    """Model representing QRYM_DRUG_PRODUCT file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_drug_products',
    )
    product_categorization = models.CharField(
        blank=True,
        help_text='The PRODUCT_CATEGORIZATION entry for this item.',
        max_length=80,
        null=True,
    )
    class_e = models.CharField(
        blank=True,
        help_text='The CLASS entry for this item.',
        max_length=40,
        null=True,
    )
    drug_identification_number = models.CharField(
        blank=True,
        help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.',
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        help_text='The BRAND_NAME entry for this item.',
        max_length=200,
        null=True,
    )
    descriptor = models.CharField(
        blank=True,
        help_text='The DESCRIPTOR entry for this item.',
        max_length=150,
        null=True,
    )
    pediatric_flag = models.CharField(
        blank=True,
        help_text='The PEDIATRIC_FLAG entry for this item.',
        max_length=1,
        null=True,
    )
    accession_number = models.CharField(
        blank=True,
        help_text='The ACCESSION_NUMBER entry for this item.',
        max_length=5,
        null=True,
    )
    number_of_ais = models.CharField(
        blank=True,
        help_text='The NUMBER_OF_AIS entry for this item.',
        max_length=10,
        null=True,
    )
    last_update_date = models.DateField(
        blank=True,
        help_text='The LAST_UPDATE_DATE entry for this item.',
        null=True,
    )
    ai_group_no = models.CharField(
        blank=True,
        help_text='The AI_GROUP_NO entry for this item.',
        max_length=10,
        null=True,
    )
    class_f = models.CharField(
        blank=True,
        help_text='The CLASS_F entry for this item.',
        max_length=80,
        null=True,
    )
    brand_name_f = models.CharField(
        blank=True,
        help_text='The BRAND_NAME_F entry for this item.',
        max_length=300,
        null=True,
    )
    descriptor_f = models.CharField(
        blank=True,
        help_text='The DESCRIPTOR_F entry for this item.',
        max_length=200,
        null=True,
    )

    # Additional fields
    field_order = [
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


class OriginalForm(models.Model):
    """Model representing QRYM_FORM file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_forms',
    )
    pharm_form_code = models.PositiveIntegerField(
        blank=True,
        help_text='The PHARM_FORM_CODE entry for this item.',
        null=True,
    )
    pharmaceutical_form = models.CharField(
        blank=True,
        help_text='The PHARMACEUTICAL_FORM entry for this item.',
        max_length=40,
        null=True,
    )
    pharmaceutical_form_f = models.CharField(
        blank=True,
        help_text='The PHARMACEUTICAL_FORM_F entry for this item.',
        max_length=80,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'pharm_form_code',
        'pharmaceutical_form',
        'pharmaceutical_form_f',
    ]


class OriginalInactiveProduct(models.Model):
    """Model representing QRYM_INACTIVE_PRODUCTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_inactive_products',
    )
    drug_identification_number = models.CharField(
        blank=True,
        help_text='The DRUG_IDENTIFICATION_NUMBER entry for this item.',
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        help_text='The BRAND_NAME entry for this item.',
        max_length=200,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        help_text='The HISTORY_DATE entry for this item.',
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'drug_identification_number',
        'brand_name',
        'history_date',
    ]


class OriginalPackaging(models.Model):
    """Model representing QRYM_Packaging file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_packaging',
    )
    upc = models.CharField(
        blank=True,
        help_text='The UPC entry for this item.',
        max_length=12,
        null=True,
    )
    package_size_unit = models.CharField(
        blank=True,
        help_text='The PACKAGE_SIZE_UNIT entry for this item.',
        max_length=40,
        null=True,
    )
    package_type = models.CharField(
        blank=True,
        help_text='The PACKAGE_TYPE entry for this item.',
        max_length=40,
        null=True,
    )
    package_size = models.CharField(
        blank=True,
        help_text='The PACKAGE_SIZE entry for this item.',
        max_length=5,
        null=True,
    )
    product_information = models.CharField(
        blank=True,
        help_text='The PRODUCT_INFORMATION entry for this item.',
        max_length=80,
        null=True,
    )
    package_size_unit_f = models.CharField(
        blank=True,
        help_text='The PACKAGE_SIZE_UNIT_F entry for this item.',
        max_length=80,
        null=True,
    )
    package_type_f = models.CharField(
        blank=True,
        help_text='The PACKAGE_TYPE_F entry for this item.',
        max_length=80,
        null=True,
    )

    # Additional attributees
    field_order = [
        'drug_code',
        'upc',
        'package_size_unit',
        'package_type',
        'package_size',
        'product_information',
        'package_size_unit_f',
        'package_type_f',
    ]


class OriginalPharmaceuticalStandard(models.Model):
    """Model representing QRYM_PHARMACEUTICAL_STD file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_pharmaceutical_standards',
    )
    pharmaceutical_std = models.CharField(
        blank=True,
        help_text='The PHARMACEUTICAL_STD entry for this item.',
        max_length=40,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'pharmaceutical_std',
    ]


class OriginalRoute(models.Model):
    """Model representing QRYM_ROUTE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_routes',
    )
    route_of_administration_code = models.PositiveIntegerField(
        blank=True,
        help_text='The ROUTE_OF_ADMINISTRATION_CODE entry for this item.',
        null=True,
    )
    route_of_administration = models.CharField(
        blank=True,
        help_text='The ROUTE_OF_ADMINISTRATION entry for this item.',
        max_length=40,
        null=True,
    )
    route_of_administration_f = models.CharField(
        blank=True,
        help_text='The ROUTE_OF_ADMINISTRATION_FFootnote entry for this item.',
        max_length=80,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'route_of_administration_code',
        'route_of_administration',
        'route_of_administration_f',
    ]


class OriginalSchedule(models.Model):
    """Model representing QRYM_SCHEDULE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_schedules',
    )
    schedule = models.CharField(
        blank=True,
        help_text='The SCHEDULE entry for this item.',
        max_length=40,
        null=True,
    )
    schedule_f = models.CharField(
        blank=True,
        help_text='The SCHEDULE_F entry for this item.',
        max_length=160,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'schedule',
        'schedule_f',
    ]


class OriginalStatus(models.Model):
    """Model representing QRYM_STATUS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_statuses',
    )
    current_status_flag = models.CharField(
        blank=True,
        help_text='The CURRENT_STATUS_FLAG entry for this item.',
        max_length=1,
        null=True,
    )
    status = models.CharField(
        blank=True,
        help_text='The STATUS entry for this item.',
        max_length=40,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        help_text='The HISTORY_DATE entry for this item.',
        null=True,
    )
    status_f = models.CharField(
        blank=True,
        help_text='The STATUS_F entry for this item.',
        max_length=80,
        null=True,
    )
    lot_number = models.CharField(
        blank=True,
        help_text='The LOT_NUMBER entry for this item.',
        max_length=50,
        null=True,
    )
    expiration_date = models.DateField(
        blank=True,
        help_text='The EXPIRATION_DATEFootnote entry for this item.',
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'current_status_flag',
        'status',
        'history_date',
        'status_f',
        'lot_number',
        'expiration_date',
    ]


class OriginalTherapeuticClass(models.Model):
    """Model representing QRYM_THERAPEUTIC_CLASS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_therapeutic_classes',
    )
    tc_atc_number = models.CharField(
        blank=True,
        help_text='The TC_ATC_NUMBER entry for this item.',
        max_length=8,
        null=True,
    )
    tc_atc = models.CharField(
        blank=True,
        help_text='The TC_ATC entry for this item.',
        max_length=120,
        null=True,
    )
    tc_atc_f = models.CharField(
        blank=True,
        help_text='The TC_ATC_F entry for this item.',
        max_length=240,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'tc_atc_number',
        'tc_atc',
        'tc_atc_f',
    ]


class OriginalVeterinarySpecies(models.Model):
    """Model representing QRYM_VETERINARY_SPECIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='original_veterinary_species',
    )
    vet_species = models.CharField(
        blank=True,
        help_text='The VET_SPECIES entry for this item.',
        max_length=80,
        null=True,
    )
    vet_sub_species = models.CharField(
        blank=True,
        help_text='The VET_SUB_SPECIES entry for this item.',
        max_length=80,
        null=True,
    )
    vet_species_f = models.CharField(
        blank=True,
        help_text='The VET_SPECIES_F entry for this item.',
        max_length=160,
        null=True,
    )

    # Additional attributes
    field_order = [
        'drug_code',
        'vet_species',
        'vet_sub_species',
        'vet_species_f',
    ]
