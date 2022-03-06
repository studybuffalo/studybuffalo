"""Models for the Health Canada Drug Product Database app."""
from django.db import models


class DPD(models.Model):
    """Holds the HC Drug Code as a foreign key and reference for all models."""
    drug_code = models.PositiveIntegerField(
        primary_key=True,
    )

    def __str__(self):
        return str(self.drug_code)


class OriginalActiveIngredient(models.Model):
    """Model representing QRYM_ACTIVE_INGREDIENTS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    active_ingredient_code = models.CharField(
        blank=True,
        max_length=6,
        null=True,
    )
    ingredient = models.CharField(
        blank=True,
        max_length=240,
        null=True,
    )
    ingredient_supplied_ind = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    strength_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    strength_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    dosage_value = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    base = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    dosage_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    notes = models.CharField(
        blank=True,
        max_length=2000,
        null=True,
    )
    ingredient_f = models.CharField(
        blank=True,
        max_length=400,
        null=True,
    )
    strength_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    strength_type_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    dosage_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class OriginalCompany(models.Model):
    """Model representing QRYM_COMPANIES file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    mfr_code = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    company_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    company_name = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    company_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    address_mailing_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_billing_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_notification_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_other = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    suite_number = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    street_name = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    city_name = models.CharField(
        blank=True,
        max_length=60,
        null=True,
    )
    province = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    country = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    postal_code = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    post_office_box = models.CharField(
        blank=True,
        max_length=15,
        null=True,
    )
    province_f = models.CharField(
        blank=True,
        max_length=100,
        null=True,
    )
    country_f = models.CharField(
        blank=True,
        max_length=100,
        null=True,
    )


class OriginalDrugProduct(models.Model):
    """Model representing QRYM_DRUG_PRODUCT file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    product_categorization = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    class_e = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    drug_identification_number = models.CharField(
        blank=True,
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    descriptor = models.CharField(
        blank=True,
        max_length=150,
        null=True,
    )
    pediatric_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    accession_number = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    number_of_ais = models.CharField(
        blank=True,
        max_length=10,
        null=True,
    )
    last_update_date = models.DateField(
        blank=True,
        null=True,
    )
    ai_group_no = models.CharField(
        blank=True,
        max_length=10,
        null=True,
    )
    class_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    brand_name_f = models.CharField(
        blank=True,
        max_length=300,
        null=True,
    )
    descriptor_f = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )


class OriginalForm(models.Model):
    """Model representing QRYM_FORM file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    pharm_form_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    pharmaceutical_form = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    pharmaceutical_form_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class OriginalInactiveProduct(models.Model):
    """Model representing QRYM_INACTIVE_PRODUCTS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    drug_identification_number = models.CharField(
        blank=True,
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        null=True,
    )


class OriginalPackaging(models.Model):
    """Model representing QRYM_Packaging file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    upc = models.CharField(
        blank=True,
        max_length=12,
        null=True,
    )
    package_size_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    package_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    package_size = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    product_information = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    package_size_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    package_type_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class OriginalPharmaceuticalStandard(models.Model):
    """Model representing QRYM_PHARMACEUTICAL_STD file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    pharmaceutical_std = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )


class OriginalRoute(models.Model):
    """Model representing QRYM_ROUTE file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    route_of_administration_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    route_of_administration = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    route_of_administration_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class OriginalSchedule(models.Model):
    """Model representing QRYM_SCHEDULE file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    schedule = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    schedule_f = models.CharField(
        blank=True,
        max_length=160,
        null=True,
    )


class OriginalStatus(models.Model):
    """Model representing QRYM_STATUS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    current_status_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    status = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        null=True,
    )
    status_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    lot_number = models.CharField(
        blank=True,
        max_length=50,
        null=True,
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
    )


class OriginalTherapeuticClass(models.Model):
    """Model representing QRYM_THERAPEUTIC_CLASS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    tc_atc_number = models.CharField(
        blank=True,
        max_length=8,
        null=True,
    )
    tc_atc = models.CharField(
        blank=True,
        max_length=120,
        null=True,
    )
    tc_atc_f = models.CharField(
        blank=True,
        max_length=240,
        null=True,
    )


class OriginalVeterinarySpecies(models.Model):
    """Model representing QRYM_VETERINARY_SPECIES file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    vet_species = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    vet_sub_species = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    vet_species_f = models.CharField(
        blank=True,
        max_length=160,
        null=True,
    )


class FormattedActiveIngredient(models.Model):
    """Model representing the formatted QRYM_ACTIVE_INGREDIENTS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalActiveIngredient',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    active_ingredient_code = models.CharField(
        blank=True,
        max_length=6,
        null=True,
    )
    ingredient = models.CharField(
        blank=True,
        max_length=240,
        null=True,
    )
    ingredient_supplied_ind = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    strength_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    strength_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    dosage_value = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    base = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    dosage_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    notes = models.CharField(
        blank=True,
        max_length=2000,
        null=True,
    )
    ingredient_f = models.CharField(
        blank=True,
        max_length=400,
        null=True,
    )
    strength_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    strength_type_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    dosage_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class FormattedCompany(models.Model):
    """Model representing the formatted QRYM_COMPANIES file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalCompany',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    mfr_code = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    company_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    company_name = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    company_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    address_mailing_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_billing_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_notification_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    address_other = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    suite_number = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    street_name = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    city_name = models.CharField(
        blank=True,
        max_length=60,
        null=True,
    )
    province = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    country = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    postal_code = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    post_office_box = models.CharField(
        blank=True,
        max_length=15,
        null=True,
    )
    province_f = models.CharField(
        blank=True,
        max_length=100,
        null=True,
    )
    country_f = models.CharField(
        blank=True,
        max_length=100,
        null=True,
    )


class FormattedDrugProduct(models.Model):
    """Model representing the formatted QRYM_DRUG_PRODUCT file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    product_categorization = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    class_e = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    drug_identification_number = models.CharField(
        blank=True,
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    descriptor = models.CharField(
        blank=True,
        max_length=150,
        null=True,
    )
    pediatric_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    accession_number = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    number_of_ais = models.CharField(
        blank=True,
        max_length=10,
        null=True,
    )
    last_update_date = models.DateField(
        blank=True,
        null=True,
    )
    ai_group_no = models.CharField(
        blank=True,
        max_length=10,
        null=True,
    )
    class_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    brand_name_f = models.CharField(
        blank=True,
        max_length=300,
        null=True,
    )
    descriptor_f = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )


class FormattedForm(models.Model):
    """Model representing the formatted QRYM_FORM file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalForm',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    pharm_form_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    pharmaceutical_form = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    pharmaceutical_form_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class FormattedInactiveProduct(models.Model):
    """Model representing the formatted QRYM_INACTIVE_PRODUCTS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalInactiveProduct',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    drug_identification_number = models.CharField(
        blank=True,
        max_length=29,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        null=True,
    )


class FormattedPackaging(models.Model):
    """Model representing the formatted QRYM_Packaging file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalPackaging',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    upc = models.CharField(
        blank=True,
        max_length=12,
        null=True,
    )
    package_size_unit = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    package_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    package_size = models.CharField(
        blank=True,
        max_length=5,
        null=True,
    )
    product_information = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    package_size_unit_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    package_type_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class FormattedPharmaceuticalStandard(models.Model):
    """Model representing the formatted QRYM_PHARMACEUTICAL_STD file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalPharmaceuticalStandard',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    pharmaceutical_std = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )


class FormattedRoute(models.Model):
    """Model representing the formatted QRYM_ROUTE file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalRoute',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    route_of_administration_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    route_of_administration = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    route_of_administration_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class FormattedSchedule(models.Model):
    """Model representing the formatted QRYM_SCHEDULE file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalSchedule',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    schedule = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    schedule_f = models.CharField(
        blank=True,
        max_length=160,
        null=True,
    )


class FormattedStatus(models.Model):
    """Model representing the formatted QRYM_STATUS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalStatus',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    current_status_flag = models.CharField(
        blank=True,
        max_length=1,
        null=True,
    )
    status = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    history_date = models.DateField(
        blank=True,
        null=True,
    )
    status_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    lot_number = models.CharField(
        blank=True,
        max_length=50,
        null=True,
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
    )


class FormattedTherapeuticClass(models.Model):
    """Model representing the formatted QRYM_THERAPEUTIC_CLASS file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='OriginalTherapeuticClass',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    tc_atc_number = models.CharField(
        blank=True,
        max_length=8,
        null=True,
    )
    tc_atc = models.CharField(
        blank=True,
        max_length=120,
        null=True,
    )
    tc_atc_f = models.CharField(
        blank=True,
        max_length=240,
        null=True,
    )


class FormattedVeterinarySpecies(models.Model):
    """Model representing the formatted QRYM_VETERINARY_SPECIES file"""
    drug_code = models.ForeignKey(
        'DPD',
        on_delete=models.CASCADE,
    )
    original = models.OneToOneField(
        to='Original',
        on_delete=models.CASCADE,
        related_name='formatted',
    )
    vet_species = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    vet_sub_species = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    vet_species_f = models.CharField(
        blank=True,
        max_length=160,
        null=True,
    )



class SubAHFS(models.Model):
    """Model representing the substitutions for AHFS code."""
    original = models.CharField(
        max_length=80,
        unique=True,
    )
    substitution = models.CharField(
        max_length=80,
    )

    class Meta:
        verbose_name = 'Substitution - AHFS'
        verbose_name_plural = 'Substitutions - AHFS'


class SubAHFSPend(models.Model):
    """Model representing the pending substitutions for AHFS code."""
    original = models.CharField(
        max_length=80,
        unique=True,
    )
    substitution = models.CharField(
        max_length=80,
    )

    class Meta:
        verbose_name = 'Substitution - AHFS (Pending)'
        verbose_name_plural = 'Substitutions - AHFS (Pending)'


class SubBrand(models.Model):
    """Model representing the substitutions for Brand."""
    original = models.CharField(
        max_length=200,
        unique=True,
    )
    substitution = models.CharField(
        max_length=200,
    )

    class Meta:
        verbose_name = 'Substitution - Brand Name'
        verbose_name_plural = 'Substitutions - Brand Name'


class SubBrandPend(models.Model):
    """Model representing the pending substitutions for Brand."""
    original = models.CharField(
        max_length=200,
        unique=True,
    )
    substitution = models.CharField(
        max_length=200,
    )

    class Meta:
        verbose_name = 'Substitution - Brand Name (Pending)'
        verbose_name_plural = 'Substitutions - Brand Name (Pending)'


class SubCompanyName(models.Model):
    """Model representing the substitutions for Company Name."""
    original = models.CharField(
        max_length=90,
        unique=True,
    )
    substitution = models.CharField(
        max_length=90,
    )

    class Meta:
        verbose_name = 'Substitution - Company Name'
        verbose_name_plural = 'Substitutions - Company Name'


class SubCompanyNamePend(models.Model):
    """Model representing pending substitutions for Company Name."""
    original = models.CharField(
        max_length=90,
        unique=True,
    )
    substitution = models.CharField(
        max_length=90,
    )

    class Meta:
        verbose_name = 'Substitution - Company Name (Pending)'
        verbose_name_plural = 'Substitutions - Company Name (Pending)'


class SubDescriptor(models.Model):
    """Model representing substitutions for Descriptor."""
    original = models.CharField(
        max_length=210,
        unique=True,
    )
    substitution = models.CharField(
        max_length=210,
    )

    class Meta:
        verbose_name = 'Substitution - Descriptor'
        verbose_name_plural = 'Substitutions - Descriptor'


class SubDescriptorPend(models.Model):
    """Model representing pending substitutions for Descriptor."""
    original = models.CharField(
        max_length=210,
        unique=True,
    )
    substitution = models.CharField(
        max_length=210,
    )

    class Meta:
        verbose_name = 'Substitution - Descriptor (Pending)'
        verbose_name_plural = 'Substitutions - Descriptor (Pending)'


class SubIngredient(models.Model):
    """Model representing substitutions for Ingredient."""
    original = models.CharField(
        max_length=240,
        unique=True,
    )
    substitution = models.CharField(
        max_length=240,
    )

    class Meta:
        verbose_name = 'Substitution - Ingredient'
        verbose_name_plural = 'Substitutions - Ingredient'


class SubIngredientPend(models.Model):
    """Model representing pending substitutions for Ingredient."""
    original = models.CharField(
        max_length=240,
        unique=True,
    )
    substitution = models.CharField(
        max_length=240,
    )

    class Meta:
        verbose_name = 'Substitution - Ingredient (Pending)'
        verbose_name_plural = 'Substitutions - Ingredient (Pending)'


class SubProductCategorization(models.Model):
    """Model representing substitutions for Product Categorization."""
    original = models.CharField(
        max_length=80,
        unique=True,
    )
    substitution = models.CharField(
        max_length=80,
    )

    class Meta:
        verbose_name = 'Substitution - Product Categorization'
        verbose_name_plural = 'Substitutions - Product Categorization'


class SubProductCategorizationPend(models.Model):
    """Model representing pending substitutions for Product Categorization."""
    original = models.CharField(
        max_length=80,
        unique=True,
    )
    substitution = models.CharField(
        max_length=80,
    )

    class Meta:
        verbose_name = 'Substitution - Product Categorization (Pending)'
        verbose_name_plural = 'Substitutions - Product Categorization (Pending)'


class SubRouteOfAdministration(models.Model):
    """Model representing substitutions for Route."""
    original = models.CharField(
        max_length=50,
        unique=True,
    )
    substitution = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name = 'Substitution - Route of Administration'
        verbose_name_plural = 'Substitutions - Route of Administration'


class SubRouteOfAdministrationPend(models.Model):
    """Model representing pending substitutions for Route."""
    original = models.CharField(
        max_length=50,
        unique=True,
    )
    substitution = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name = 'Substitution - Route of Administration (Pending)'
        verbose_name_plural = 'Substitutions - Route of Administration (Pending)'


class SubPharmaceuticalStd(models.Model):
    """Model representing substitutions for Pharmaceutical Standard."""
    original = models.CharField(
        max_length=40,
        unique=True,
    )
    substitution = models.CharField(
        max_length=40,
    )

    class Meta:
        verbose_name = 'Substitution - Pharmaceutical Standard'
        verbose_name_plural = 'Substitutions - Pharmaceutical Standard'


class SubPharmaceuticalStdPend(models.Model):
    """Model representing pending substitutions for Pharmaceutical Standard."""
    original = models.CharField(
        max_length=40,
        unique=True,
    )
    substitution = models.CharField(
        max_length=40,
    )

    class Meta:
        verbose_name = 'Substitution - Pharmaceutical Standard (Pending)'
        verbose_name_plural = 'Substitutions - Pharmaceutical Standard (Pending)'


class SubStreetName(models.Model):
    """Model representing substitutions for Street Name."""
    original = models.CharField(
        max_length=90,
        unique=True,
    )
    substitution = models.CharField(
        max_length=90,
    )

    class Meta:
        verbose_name = 'Substitution - Street Name'
        verbose_name_plural = 'Substitutions - Street Name'


class SubStreetNamePend(models.Model):
    """Model representing pending substitutions for Street Name."""
    original = models.CharField(
        max_length=90,
        unique=True,
    )
    substitution = models.CharField(
        max_length=90,
    )

    class Meta:
        verbose_name = 'Substitution - Street Name (Pending)'
        verbose_name_plural = 'Substitutions - Street Name (Pending)'


class SubSuiteNumber(models.Model):
    """Model representing substitutions for Suite Number."""
    original = models.CharField(
        max_length=20,
        unique=True,
    )
    substitution = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = 'Substitution - Suite Number'
        verbose_name_plural = 'Substitutions - Suite Number'


class SubSuiteNumberPend(models.Model):
    """Model representing pending substitutions for Suite Number."""
    original = models.CharField(
        max_length=20,
        unique=True,
    )
    substitution = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = 'Substitution - Suite Number (Pending)'
        verbose_name_plural = 'Substitutions - Suite Number (Pending)'


class SubUnit(models.Model):
    """Model representing substitutions for Unit."""
    original = models.CharField(
        max_length=40,
        unique=True,
    )
    substitution = models.CharField(
        max_length=40,
    )

    class Meta:
        verbose_name = 'Substitution - Unit'
        verbose_name_plural = 'Substitutions - Unit'


class SubUnitPend(models.Model):
    """Model representing pending substitutions for Unit."""
    original = models.CharField(
        max_length=40,
        unique=True,
    )
    substitution = models.CharField(
        max_length=40,
    )

    class Meta:
        verbose_name = 'Substitution - Unit (Pending)'
        verbose_name_plural = 'Substitutions - Unit (Pending)'
