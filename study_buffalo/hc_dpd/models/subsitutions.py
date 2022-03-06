"""Models to support formatting substitutions."""
from django.db import models


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
