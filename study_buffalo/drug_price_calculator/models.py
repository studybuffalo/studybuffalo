"""Models for the Drug Price Calculator Application."""
from django.db import models


class Drug(models.Model):
    """Details of a single drug."""
    din = models.CharField(
        help_text='The drug\'s DIN/NPN/PIN',
        max_length=8,
        unique=True,
        verbose_name='DIN',
    )
    brand_name = models.CharField(
        blank=True,
        help_text='The brand name or trade name',
        max_length=80,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        help_text='The strength(s) of the medications',
        max_length=250,
        null=True,
    )
    route = models.CharField(
        blank=True,
        help_text='The route of administration',
        max_length=20,
        null=True,
    )
    dosage_form = models.CharField(
        blank=True,
        help_text='The dosage form',
        max_length=40,
        null=True,
    )
    generic_name = models.CharField(
        blank=True,
        help_text='The generic name',
        max_length=450,
        null=True,
    )
    manufacturer = models.CharField(
        blank=True,
        help_text='The drug manufacturer',
        max_length=150,
        null=True,
    )
    schedule = models.CharField(
        blank=True,
        help_text='The provincial drug schedule',
        max_length=10,
        null=True,
    )
    atc = models.ForeignKey(
        blank=True,
        help_text='The ATC code for this drug',
        null=True,
        on_delete=models.SET_NULL,
        related_name='drugs',
        to='drug_price_calculator.ATC',
        verbose_name='ATC',
    )
    ptc = models.ForeignKey(
        blank=True,
        help_text='The PTC code for this drug',
        null=True,
        on_delete=models.SET_NULL,
        related_name='drugs',
        to='drug_price_calculator.PTC',
        verbose_name='PTC',
    )
    generic_product = models.CharField(
        blank=True,
        help_text='A calculated name to identify similar drugs',
        max_length=750,
        null=True,
    )

    def __str__(self):
        if self.brand_name:
            return f'{self.brand_name} ({self.din})'

        return self.din


class ATC(models.Model):
    """Defines the ATC for each extracted URL"""
    id = models.CharField(
        max_length=7,
        primary_key=True,
        unique=True,
    )
    atc_1 = models.CharField(
        blank=True,
        max_length=7,
        null=True,
        verbose_name='ATC level 1 code',
    )
    atc_1_text = models.CharField(
        blank=True,
        max_length=200,
        null=True,
        verbose_name='ATC level 1 description',
    )
    atc_2 = models.CharField(
        blank=True,
        max_length=7,
        null=True,
        verbose_name='ATC level 2 code',
    )
    atc_2_text = models.CharField(
        blank=True,
        max_length=200,
        null=True,
        verbose_name='ATC level 2 description',
    )
    atc_3 = models.CharField(
        blank=True,
        max_length=7,
        null=True,
        verbose_name='ATC level 3 code',
    )
    atc_3_text = models.CharField(
        blank=True,
        max_length=200,
        null=True,
        verbose_name='ATC level 3 description',
    )
    atc_4 = models.CharField(
        blank=True,
        max_length=7,
        null=True,
        verbose_name='ATC level 4 code',
    )
    atc_4_text = models.CharField(
        blank=True,
        max_length=200,
        null=True,
        verbose_name='ATC level 4 description',
    )
    atc_5 = models.CharField(
        blank=True,
        max_length=7,
        null=True,
        verbose_name='ATC level 5 code',
    )
    atc_5_text = models.CharField(
        blank=True,
        max_length=200,
        null=True,
        verbose_name='ATC level 5 description',
    )

    class Meta:
        verbose_name = 'Anatomical Therapeutic Category'
        verbose_name_plural = 'Anatomical Therapeutic Categories'

    def __str__(self):
        if self.atc_5:
            return f'{self.atc_5} ({self.atc_5_text})'

        if self.atc_4:
            return f'{self.atc_4} ({self.atc_4_text})'

        if self.atc_3:
            return f'{self.atc_3} ({self.atc_3_text})'

        if self.atc_2:
            return f'{self.atc_2} ({self.atc_2_text})'

        if self.atc_1:
            return f'{self.atc_1} ({self.atc_1_text})'

        return str(self.id)


class PTC(models.Model):
    """Defines the PTC for the specified URL"""
    id = models.CharField(
        max_length=11,
        primary_key=True,
        unique=True,
    )
    ptc_1 = models.CharField(
        blank=True,
        max_length=11,
        null=True,
        verbose_name='PTC level 1 code',
    )
    ptc_1_text = models.CharField(
        blank=True,
        max_length=100,
        null=True,
        verbose_name='PTC level 1 description',
    )
    ptc_2 = models.CharField(
        blank=True,
        max_length=11,
        null=True,
        verbose_name='PTC level 2 code',
    )
    ptc_2_text = models.CharField(
        blank=True,
        max_length=100,
        null=True,
        verbose_name='PTC level 2 description',
    )
    ptc_3 = models.CharField(
        blank=True,
        max_length=11,
        null=True,
        verbose_name='PTC level 3 code',
    )
    ptc_3_text = models.CharField(
        blank=True,
        max_length=100,
        null=True,
        verbose_name='PTC level 3 description',
    )
    ptc_4 = models.CharField(
        blank=True,
        max_length=11,
        null=True,
        verbose_name='PTC level 4 code',
    )
    ptc_4_text = models.CharField(
        blank=True,
        max_length=100,
        null=True,
        verbose_name='PTC level 4 description',
    )

    class Meta:
        verbose_name = 'Pharmacologic-Therapeutic Classification'
        verbose_name_plural = 'Pharmacologic-Therapeutic Classifications'

    def __str__(self):
        if self.ptc_4:
            return f'{self.ptc_4} ({self.ptc_4_text})'

        if self.ptc_3:
            return f'{self.ptc_3} ({self.ptc_3_text})'

        if self.ptc_2:
            return f'{self.ptc_2} ({self.ptc_2_text})'

        if self.ptc_1:
            return f'{self.ptc_1} ({self.ptc_1_text})'

        return str(self.id)


class Price(models.Model):
    """Pricing details for a single drug."""
    drug = models.ForeignKey(
        help_text='The drug this price applies to',
        on_delete=models.CASCADE,
        related_name='prices',
        to=Drug,
    )
    abc_id = models.PositiveIntegerField(
        help_text='The Alberta Blue Cross iDBL ID number',
        verbose_name='ABC ID',
    )
    date_listed = models.DateField(
        blank=True,
        help_text='The date listed or date updated',
        null=True,
    )
    unit_price = models.DecimalField(
        blank=True,
        decimal_places=4,
        help_text='The unit price (in CAD)',
        max_digits=10,
        null=True,
    )
    lca_price = models.DecimalField(
        blank=True,
        decimal_places=4,
        help_text='The Least Cost Alternative price (in CAD)',
        max_digits=10,
        null=True,
        verbose_name='LCA price',
    )
    mac_price = models.DecimalField(
        blank=True,
        decimal_places=4,
        help_text='The Maximum Allowable Cost price (in CAD)',
        max_digits=10,
        null=True,
        verbose_name='MAC price',
    )
    mac_text = models.CharField(
        blank=True,
        help_text='Descriptions for the MAC pricing',
        max_length=150,
        null=True,
        verbose_name='MAC text',
    )
    unit_issue = models.CharField(
        blank=True,
        help_text='The unit of issue for pricing',
        max_length=25,
        null=True,
        verbose_name='unit of issue',
    )
    interchangeable = models.BooleanField(
        default=False,
        help_text='Whether are interchangeable products or not',
    )
    coverage_status = models.CharField(
        blank=True,
        help_text='The coverage status of the drug',
        max_length=100,
        null=True,
    )
    special_authorizations = models.ManyToManyField(
        help_text='Special Authorization forms that apply to this drug',
        related_name='drugs',
        to='drug_price_calculator.SpecialAuthorization',
    )
    date_added = models.DateTimeField(
        auto_now=True,
        help_text='The date and time this price was added',
    )

    def __str__(self):
        if self.drug.brand_name:
            return f'{self.drug.brand_name} price ({self.abc_id})'

        return f'{self.drug.din} price ({self.abc_id})'


class Clients(models.Model):
    """Holds details regarding which clients are covered."""
    price = models.OneToOneField(
        blank=True,
        help_text='The price details these clients apply to',
        null=True,
        on_delete=models.SET_NULL,
        to='drug_price_calculator.Price',
    )
    group_1 = models.BooleanField(
        default=False,
    )
    group_66 = models.BooleanField(
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

    class Meta:
        verbose_name_plural = 'clients'

    def __str__(self):
        return f'{str(self.price)} clients'


class CoverageCriteria(models.Model):
    """Details on any coverage criteria."""
    price = models.ForeignKey(
        help_text='The drug price this criteria applies to',
        on_delete=models.CASCADE,
        related_name='coverage_criteria',
        to=Price,
    )
    header = models.CharField(
        blank=True,
        help_text='Any header for this criteria',
        max_length=200,
        null=True,
    )
    criteria = models.TextField(
        help_text='The coverage criteria',
    )

    class Meta:
        verbose_name_plural = 'coverage criteria'

    def __str__(self):
        return f'{str(self.price)} coverage criteria'


class SpecialAuthorization(models.Model):
    """Details on special authorization forms."""
    file_name = models.CharField(
        help_text='The name of the PDF file',
        max_length=15,
    )
    pdf_title = models.CharField(
        help_text='The tile of the PDF',
        max_length=200,
    )

    def __str__(self):
        return self.pdf_title


class SubsBSRF(models.Model):
    """Formatting substitutions for Brand/Strength/Route/Formulation"""
    original = models.CharField(
        max_length=400,
        unique=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=80,
        null=True
    )
    strength = models.CharField(
        blank=True,
        max_length=250,
        null=True
    )
    route = models.CharField(
        blank=True,
        max_length=20,
        null=True
    )
    dosage_form = models.CharField(
        blank=True,
        max_length=40,
        null=True
    )

    class Meta:
        verbose_name = 'Substitution - BSRF'
        verbose_name_plural = 'Substitutions - BSRF'


class SubsGeneric(models.Model):
    """Formatting substitutions for generic names"""
    original = models.CharField(
        max_length=450,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=450,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Generic'
        verbose_name_plural = 'Substitutions - Generic'


class SubsManufacturer(models.Model):
    """Formatting substitutions for manufacturers"""
    original = models.CharField(
        max_length=150,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=150,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Manufacturer'
        verbose_name_plural = 'Substitutions - Manufacturer'


class SubsUnit(models.Model):
    """Substitutions for units"""
    original = models.CharField(
        max_length=120,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=120,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Unit'
        verbose_name_plural = 'Substitutions - Unit'


class PendBSRF(models.Model):
    """Pending substitutions for BSRF"""
    original = models.CharField(
        max_length=400,
        unique=True,
    )
    brand_name = models.CharField(
        blank=True,
        max_length=80,
        null=True,
    )
    strength = models.CharField(
        blank=True,
        max_length=250,
        null=True,
    )
    route = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    dosage_form = models.CharField(
        blank=True,
        max_length=40,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - BSRF (Pending)'
        verbose_name_plural = 'Substitutions - BSRF (Pending)'


class PendGeneric(models.Model):
    """Pending substitutions for Generic Names"""
    original = models.CharField(
        max_length=450,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=450,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Generic (Pending)'
        verbose_name_plural = 'Substitutions - Generic (Pending)'


class PendManufacturer(models.Model):
    """Pending substitutions for Manufacturers"""
    original = models.CharField(
        max_length=150,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=150,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Manufactuer (Pending)'
        verbose_name_plural = 'Substitutions - Manufactuer (Pending)'


class PendUnit(models.Model):
    """Pending substitutions for Units"""
    original = models.CharField(
        max_length=120,
        unique=True,
    )
    correction = models.CharField(
        blank=True,
        max_length=120,
        null=True,
    )

    class Meta:
        verbose_name = 'Substitution - Unit (Pending)'
        verbose_name_plural = 'Substitutions - Unit (Pending)'
