from django.db import models

class ATC(models.Model):
    """Defines the ATC for each extracted URL"""
    url = models.PositiveIntegerField()

    atc_1 = models.CharField(
        max_length=7,
        null=True,
    )

    atc_1_text = models.CharField(
        max_length=200,
        null=True,
    )

    atc_2 = models.CharField(
        max_length=7,
        null=True,
    )

    atc_2_text = models.CharField(
        max_length=200,
        null=True,
    )

    atc_3 = models.CharField(
        max_length=7,
        null=True,
    )

    atc_3_text = models.CharField(
        max_length=200,
        null=True,
    )

    atc_4 = models.CharField(
        max_length=7,
        null=True,
    )

    atc_4_text = models.CharField(
        max_length=200,
        null=True,
    )

    # Meta Settings
    class Meta:
        verbose_name = "Anatomical Therapeutic Category"
        verbose_name_plural = "Anatomical Therapeutic Categories"

    # Methods
    def __str__(self):
        """String of the ATC"""
        if self.atc_4:
            return "{0} - {1}".format(self.atc_4, self.atc_4_text)
        elif self.atc_3:
            return "{0} - {1}".format(self.atc_3, self.atc_3_text)
        elif self.atc_2:
            return "{0} - {1}".format(self.atc_2, self.atc_2_text)
        elif self.atc_1:
            return "{0} - {1}".format(self.atc_1, self.atc_1_text)
        else:
            return "No atc for {0}".format(self.url)

class ATCDescriptions(models.Model):
    """Defines each ATC description for each code"""
    code = models.CharField(
        max_length=5,
        unique=True,
    )

    description = models.CharField(
        max_length=80,
        null=True,
    )

class Coverage(models.Model):
    """Defines coverage criteria for each URL"""
    url = models.PositiveIntegerField()

    coverage = models.CharField(
        max_length=60,
    )

    criteria = models.BooleanField(

    )

    criteria_sa = models.CharField(
        max_length=100,
        null=True,
    )

    criteria_p = models.CharField(
        max_length=70,
        null=True,
    )

    group_1 = models.BooleanField(
        default=False,
    )

    group_66 = models.BooleanField(
        default=False,
    )

    group_66a = models.BooleanField(
        default=False,
    )

    group_19823 = models.BooleanField(
        default=False,
    )

    group_19823a = models.BooleanField(
        default=False,
    )

    group_19824 = models.BooleanField(
        default=False,
    )

    group_20400 = models.BooleanField(
        default=False,
    )

    group_20403 = models.BooleanField(
        default=False,
    )

    group_20514 = models.BooleanField(
        default=False,
    )

    group_22128 = models.BooleanField(
        default=False,
    )

    group_23609 = models.BooleanField(
        default=False,
    )

class ExtraInformation(models.Model):
    """Defines additional information for each URL"""
    url = models.PositiveIntegerField()

    date_listed = models.DateField(
        null=True,
    )

    date_discontinued = models.DateField(
        null=True,
    )

    manufacturer = models.CharField(
        max_length=75,
    )

    schedule = models.CharField(
        max_length=10,
    )

    interchangeable = models.CharField(
        max_length=3,
    )

class Price(models.Model):
    url = models.PositiveIntegerField()

    din = models.PositiveIntegerField()

    brand_name = models.CharField(
        max_length=70,
        null=True,
    )

    strength = models.CharField(
        max_length=200,
        null=True,
    )

    route = models.CharField(
        max_length=20,
        null=True,
    )

    dosage_form = models.CharField(
        max_length=35,
        null=True,
    )

    generic_name = models.CharField(
        max_length=450,
        null=True,
    )

    unit_price = models.DecimalField(
        decimal_places=4,
        max_digits=10,
        null=True,
    )

    lca = models.DecimalField(
        decimal_places=4,
        max_digits=10,
        null=True,
    )

    lca_text = models.CharField(
        max_length=150,
        null=True,
    )

    unit_issue = models.CharField(
        max_length=25,
        null=True,
    )

class PTC(models.Model):
    """Defines the PTC for the specified URL"""
    url = models.PositiveIntegerField()

    ptc_1 = models.PositiveIntegerField(
        null=True,
    )

    ptc_1_text = models.CharField(
        max_length=75,
        null=True,
    )

    ptc_2 = models.PositiveIntegerField(
        null=True,
    )

    ptc_2_text = models.CharField(
        max_length=75,
        null=True,
    )

    ptc_3 = models.PositiveIntegerField(
        null=True,
    )

    ptc_3_text = models.CharField(
        max_length=75,
        null=True,
    )

    ptc_4 = models.PositiveIntegerField(
        null=True,
    )

    ptc_4_text = models.CharField(
        max_length=75,
        null=True,
    )

class SpecialAuthorization(models.Model):
    """Defines the Special Authorization criteria for specified URLs"""
    url = models.PositiveIntegerField()

    title = models.CharField(
        max_length=200,
        null=True,
    )

    link = models.CharField(
        max_length=50,
        null=True,
    )

class SubsBSRF(models.Model):
    """Formatting substitutions for Brand/Strength/Route/Formulation"""
    bsrf = models.CharField(
        max_length=250,
        unique=True,
    )

    brand_name = models.CharField(
        max_length=80,
    )

    strength = models.CharField(
        max_length=200,
        null=True
    )

    route = models.CharField(
        max_length=20,
        null=True
    )

    dosage_form = models.CharField(
        max_length=40,
        null=True
    )

class SubsGeneric(models.Model):
    """Formatting substitutions for generic names"""
    original = models.CharField(
        max_length=450,
        unique=True,
    )

    correction = models.CharField(
        max_length=450,
    )

class SubsManufacturer(models.Model):
    """Formatting substitutions for manufacturers"""
    original = models.CharField(
        max_length=120,
        unique=True,
    )

    correction = models.CharField(
        max_length=120,
    )

class SubsPTC(models.Model):
    """Substitutions for PTC"""
    original = models.CharField(
        max_length=120,
        unique=True,
    )

    correction = models.CharField(
        max_length=120,
    )

class SubsUnit(models.Model):
    """Substitutions for units"""
    original = models.CharField(
        max_length=120,
        unique=True,
    )

    correction = models.CharField(
        max_length=120,
    )

class PendBSRF(models.Model):
    """Pending substitutions for BSRF"""
    original = models.CharField(
        max_length=250,
        unique=True,
    )

    brand_name = models.CharField(
        max_length=80,
    )

    strength = models.CharField(
        max_length=200,
        null=True,
    )

    route = models.CharField(
        max_length=20,
        null=True,
    )

    dosage_form = models.CharField(
        max_length=40,
        null=True,
    )

class PendGeneric(models.Model):
    """Pending substitutions for Generic Names"""
    original = models.CharField(
        max_length=450,
        unique=True,
    )

    correction = models.CharField(
        max_length=450,
    )

class PendManufacturer(models.Model):
    """Pending substitutions for Manufacturers"""
    original = models.CharField(
        max_length=150,
        unique=True,
    )

    correction = models.CharField(
        max_length=150,
    )

class PendPTC(models.Model):
    """Pending substitutions for PTC"""
    original = models.CharField(
        max_length=150,
        unique=True,
    )

    correction = models.CharField(
        max_length=150,
    )

"""
    Planning for expanding the drug price calculator

    List of medications
    Trade name
    Brand Name
    Ingredients +/- strengths +/- dosage form (EPID?)
    ptcFK
    atcFK

    Price info
        medicationFK
        unit price
        unit of issue
        LCA
        MAC
        source
            ABC iDBL
            ABC DPL
            NIHB

    PTC List

    ATC List

    Coverage
        ABC coverage
            Plan coverage amounts
            ABC special auth
        NIHB coverage
            Prior approval
"""
