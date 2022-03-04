"""Models for the Health Canada Drug Product Database app."""
from django.db import models


class DPD(models.Model):
    """Holds drug_code as a foreign_key and records origin file"""
    drug_code = models.PositiveIntegerField(
        primary_key=True
    )
    origin_file = models.CharField(
        choices=(
            ('a', 'approved'),
            ('c', 'cancelled'),
            ('d', 'dormant'),
            ('m', 'marketed'),
        ),
        max_length=1,
    )

    def __str__(self):
        return f'{self.drug_code} ({self.origin_file})'


class ActiveIngredient(models.Model):
    """Model representing QRYM_ACTIVE_INGREDIENTS file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    active_ingredient_code = models.CharField(
        blank=True,
        max_length=5,
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
    base = models.BooleanField()
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
        max_length=260,
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


class Company(models.Model):
    """Model representing QRYM_COMPANIES file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
        max_length=90,
        null=True,
    )
    company_type = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    address_mailing_flag = models.BooleanField()
    address_billing_flag = models.BooleanField()
    address_notification_flag = models.BooleanField()
    address_other = models.BooleanField()
    suite_number = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    street_name = models.CharField(
        blank=True,
        max_length=90,
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
        max_length=40,
        null=True,
    )
    country_f = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )


class DrugProduct(models.Model):
    """Model representing QRYM_DRUG_PRODUCT file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
        max_length=8,
        null=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    descriptor = models.CharField(
        blank=True,
        max_length=210,
        null=True,
    )
    pediatric_flag = models.BooleanField()
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
        max_length=40,
        null=True,
    )
    brand_name_f = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    descriptor_f = models.CharField(
        blank=True,
        max_length=150,
        null=True,
    )


class Form(models.Model):
    """Model representing QRYM_FORM file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
        max_length=60,
        null=True,
    )


class InactiveProduct(models.Model):
    """Model representing QRYM_INACTIVE_PRODUCTS file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    drug_identification_number = models.CharField(
        blank=True,
        max_length=8,
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


class Packaging(models.Model):
    """Model representing QRYM_Packaging file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
        max_length=10,
        null=True,
    )
    product_information = models.CharField(
        blank=True,
        max_length=90,
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


class PharmaceuticalStandard(models.Model):
    """Model representing QRYM_PHARMACEUTICAL_STD file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    pharmaceutical_std = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )


class Route(models.Model):
    """Model representing QRYM_ROUTE file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    route_of_administration_code = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    route_of_administration = models.CharField(
        blank=True,
        max_length=50,
        null=True,
    )
    route_of_administration_f = models.CharField(
        blank=True,
        max_length=60,
        null=True,
    )


class Schedule(models.Model):
    """Model representing QRYM_SCHEDULE file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    schedule = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )
    schedule_f = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )


class Status(models.Model):
    """Model representing QRYM_STATUS file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
    current_status_flag = models.BooleanField()
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
        max_length=80,
        null=True,
    )
    expiration_date = models.DateField(
        blank=True,
        null=True,
    )


class TherapeuticClass(models.Model):
    """Model representing QRYM_THERAPEUTIC_CLASS file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
    tc_ahfs_number = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    tc_ahfs = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    tc_atc_f = models.CharField(
        blank=True,
        max_length=120,
        null=True,
    )
    tc_ahfs_f = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )


class VeterinarySpecies(models.Model):
    """Model representing QRYM_VETERINARY_SPECIES file"""
    drug_code = models.ForeignKey('DPD', on_delete=models.CASCADE)
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
        max_length=80,
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
