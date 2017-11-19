from django.db import models

class DPD(models.Model):
    """Holds drug_code as a foreign_key and records origin file"""
    drug_code = models.PositiveIntegerField(
        primary_key=True
    )
    origin_file = models.CharField(
        choices=(
            ("a", "approved"),
            ("c", "cancelled"),
            ("d", "dormant"),
            ("m", "marketed"),
        ),
        max_length=1,
    )

class ActiveIngredients(models.Model):
    """Model representing QRYM_ACTIVE_INGREDIENTS file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
        max_length=160,
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

class Companies(models.Model):
    """Model representing QRYM_COMPANIES file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    late_update_date = models.DateField(
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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

class InactiveProducts(models.Model):
    """Model representing QRYM_INACTIVE_PRODUCTS file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
    pharmaceutical_std = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )

class Route(models.Model):
    """Model representing QRYM_ROUTE file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
        max_length=60,
        null=True,
    )

class Schedule(models.Model):
    """Model representing QRYM_SCHEDULE file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    expiration_date = models.DateField()

class TherapeuticClass(models.Model):
    """Model representing QRYM_THERAPEUTIC_CLASS file"""
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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
    drug_code = models.ForeignKey("DPD", on_delete=models.CASCADE)
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