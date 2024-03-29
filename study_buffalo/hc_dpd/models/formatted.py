"""Models for formatted Drug Product Database content."""
from django.db import models


class FormattedActiveIngredient(models.Model):
    """Model representing the formatted QRYM_ACTIVE_INGREDIENTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_active_ingredients',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.ingredient} [{self.active_ingredient_code}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted active ingredient'
        verbose_name_plural = 'formatted active ingredients'


class FormattedBiosimilar(models.Model):
    """Model representing the formatted QRYM_BIOSIMILARS file.

        This extract is not present in the DPD Read Me File - field names
        and types were implied from extract data.
    """
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_biosimilars',
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
    biosimilar_type_f = models.CharField(
        blank=True,
        help_text='The formatted version of BIOSIMILAR_TYPE_F.',
        max_length=20,
        null=True,
    )

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.biosimilar_code} [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted biosimilar'
        verbose_name_plural = 'formatted biosimilars'


class FormattedCompany(models.Model):
    """Model representing the formatted QRYM_COMPANIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_companies',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.company_name} [{self.company_code}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted company'
        verbose_name_plural = 'formatted companies'


class FormattedDrugProduct(models.Model):
    """Model representing the formatted QRYM_DRUG_PRODUCT file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_drug_products',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.brand_name} [{self.drug_identification_number}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted drug product'
        verbose_name_plural = 'formatted drug products'


class FormattedForm(models.Model):
    """Model representing the formatted QRYM_FORM file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_forms',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.pharmaceutical_form} [{self.pharm_form_code}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted form'
        verbose_name_plural = 'formatted forms'


class FormattedInactiveProduct(models.Model):
    """Model representing the formatted QRYM_INACTIVE_PRODUCTS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_inactive_products',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.brand_name} [{self.history_date}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted inactive product'
        verbose_name_plural = 'formatted inactive products'


class FormattedPackaging(models.Model):
    """Model representing the formatted QRYM_Packaging file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_packaging',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.upc} [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted packaging'
        verbose_name_plural = 'formatted packaging'


class FormattedPharmaceuticalStandard(models.Model):
    """Model representing the formatted QRYM_PHARMACEUTICAL_STD file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_pharmaceutical_standards',
    )
    pharmaceutical_std = models.CharField(
        blank=True,
        help_text='The formatted version of PHARMACEUTICAL_STD.',
        max_length=40,
        null=True,
    )

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.pharmaceutical_std} [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted pharmaceutical standard'
        verbose_name_plural = 'formatted pharmaceutical standards'


class FormattedRoute(models.Model):
    """Model representing the formatted QRYM_ROUTE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_routes',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.route_of_administration} [{self.route_of_administration_code}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted route'
        verbose_name_plural = 'formatted routes'


class FormattedSchedule(models.Model):
    """Model representing the formatted QRYM_SCHEDULE file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_schedules',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.schedule} [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted schedule'
        verbose_name_plural = 'formatted schedules'


class FormattedStatus(models.Model):
    """Model representing the formatted QRYM_STATUS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_statuses',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.status} [{self.history_date}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted status'
        verbose_name_plural = 'formatted statuses'


class FormattedTherapeuticClass(models.Model):
    """Model representing the formatted QRYM_THERAPEUTIC_CLASS file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_therapeutic_classes',
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

    def __str__(self):
        """Returns string representation of model."""
        return f'{self.tc_atc} [{self.tc_atc_number}] [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted therapeutic class'
        verbose_name_plural = 'formatted therapeutic classes'


class FormattedVeterinarySpecies(models.Model):
    """Model representing the formatted QRYM_VETERINARY_SPECIES file."""
    drug_code = models.ForeignKey(
        'hc_dpd.dpd',
        on_delete=models.CASCADE,
        help_text='The drug code reference for this item.',
        related_name='formatted_veterinary_species',
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

    def __str__(self):
        """Returns string representation of model."""
        species_list = []

        if self.vet_species != '' and self.vet_species is not None:
            species_list.append(self.vet_species)

        if self.vet_sub_species != '' and self.vet_sub_species is not None:
            species_list.append(self.vet_sub_species)

        return f'{" - ".join(species_list)} [F; Drug Code {self.drug_code}]'

    class Meta:
        verbose_name = 'formatted veterinary species'
        verbose_name_plural = 'formatted veterinary species'
