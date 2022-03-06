"""Core models to support the Health Canada Drug Product Database app."""
from django.db import models


class DPD(models.Model):
    """Holds the HC Drug Code as a foreign key and reference for all models."""
    drug_code = models.PositiveIntegerField(
        primary_key=True,
        help_text='The Health Canada Drug Code.'
    )

    def __str__(self):
        return str(self.drug_code)


class DPDChecksum(models.Model):
    """Holds checksum data of the original DPD data to identify changed data.

        Checksums are used to quickly identify when a record in the DPD
        extracts has changed. Checksums are calculated by:
            - Combining all DPD file types (e.g. marketed, cancelled) for an
              extract type (e.g. QRYM_BIOSIMILARS, QRYM_FORM);
            - Filtering to the desired range of items (typically 1000 items
              or fewer);
            - Converting all original data values to strings;
            - Concatenating all value for each item in the original order
              provided by the DPD;
            - Concatenating all these concatenated values in order of the
              smallest drug code to the largest; and then
            - Running the <TBD HASH> on the final concatenated product.
    """
    # Extract source file choices
    ACTIVE_INGREDIENTS = 'act'
    BIOSIMILARS = 'bio'
    COMPANIES = 'com'
    DRUG_PRODUCT = 'dru'
    FORM = 'for'
    INACTIVE_PRODUCTS = 'ina'
    PACKAGING = 'pac'
    PHARMACEUTICAL_STANDARD = 'pha'
    ROUTE = 'rou'
    SCHEDULE = 'sch'
    STATUS = 'sta'
    THERAPEUTIC_CLASS = 'the'
    VETERINARY_SPECIES = 'vet'
    EXTRACT_SOURCE_CHOICES = (
        (ACTIVE_INGREDIENTS, 'QRYM_ACTIVE_INGREDIENTS'),
        (BIOSIMILARS, 'QRYM_BIOSIMILARS'),
        (COMPANIES, 'QRYM_COMPANIES'),
        (DRUG_PRODUCT, 'QRYM_DRUG_PRODUCT'),
        (FORM, 'QRYM_FORM'),
        (INACTIVE_PRODUCTS, 'QRYM_INACTIVE_PRODUCTS'),
        (PACKAGING, 'QRYM_PACKAGING'),
        (PHARMACEUTICAL_STANDARD, 'QRYM_PHARMACEUTICAL_STD'),
        (ROUTE, 'QRYM_ROUTE'),
        (SCHEDULE, 'QRYM_SCHEDULE'),
        (STATUS, 'QRYM_STATUS'),
        (THERAPEUTIC_CLASS, 'QRYM_THERAPEUTIC_CLASS'),
        (VETERINARY_SPECIES, 'QRYM_VETERINARY_SPECIES'),
    )

    drug_code_start = models.PositiveIntegerField(
        help_text='The starting Health Canada Drug code for this checksum.',
    )
    drug_code_end = models.PositiveIntegerField(
        help_text='The final Health Canada Drug code for this checksum.',
    )
    extract_source = models.CharField(
        choices=EXTRACT_SOURCE_CHOICES,
        help_text='The extract source data for this checksum',
        max_length=3,
    )
    checksum = models.CharField(
        help_text='The checksum value for the specified items.',
        max_length=128,
    )
    checksum_date = models.DateField(
        auto_now=True,
        help_text='The date this checksum was created or updated.'
    )
