"""Core models to support the Health Canada Drug Product Database app."""
from zlib import crc32

from django.db import models
from django.utils import timezone

from hc_dpd import utils
from hc_dpd.validators import validate_checksum_start


class DPD(models.Model):
    """Holds the HC Drug Code as a foreign key and reference for all models."""
    drug_code = models.PositiveIntegerField(
        primary_key=True,
        help_text='The Health Canada Drug Code.'
    )
    original_active_ingredient_modified = models.DateTimeField(
        blank=True,
        help_text='When the original active ingredient instances were last modified.',
        null=True,
    )
    original_biosimilar_modified = models.DateTimeField(
        blank=True,
        help_text='When the original biosimilar instances were last modified.',
        null=True,
    )
    original_company_modified = models.DateTimeField(
        blank=True,
        help_text='When the original company instances were last modified.',
        null=True,
    )
    original_drug_product_modified = models.DateTimeField(
        blank=True,
        help_text='When the original drug product instances were last modified.',
        null=True,
    )
    original_form_modified = models.DateTimeField(
        blank=True,
        help_text='When the original form instances were last modified.',
        null=True,
    )
    original_inactive_product_modified = models.DateTimeField(
        blank=True,
        help_text='When the original inactive product instances were last modified.',
        null=True,
    )
    original_packaging_modified = models.DateTimeField(
        blank=True,
        help_text='When the original packaging instances were last modified.',
        null=True,
    )
    original_pharmaceutical_standard_modified = models.DateTimeField(
        blank=True,
        help_text='When the original pharmaceutical standard instances were last modified.',
        null=True,
    )
    original_route_modified = models.DateTimeField(
        blank=True,
        help_text='When the original route instances were last modified.',
        null=True,
    )
    original_schedule_modified = models.DateTimeField(
        blank=True,
        help_text='When the original schedule instances were last modified.',
        null=True,
    )
    original_status_modified = models.DateTimeField(
        blank=True,
        help_text='When the original status instances were last modified.',
        null=True,
    )
    original_therapeutic_class_modified = models.DateTimeField(
        blank=True,
        help_text='When the original therapeutic_class instances were last modified.',
        null=True,
    )
    original_veterinary_species_modified = models.DateTimeField(
        blank=True,
        help_text='When the original veterinary species instances were last modified.',
        null=True,
    )

    def __str__(self):
        """Returns string representation of model."""
        return str(self.drug_code)

    def update_modified(self, field):
        """Updates the modified datetime for the specified field.

            :param field str: The field to update the modified
                datetime for.
        """
        # Mapping of string names to model fields
        field_mapping = {
            utils.ACTIVE_INGREDIENT: 'original_active_ingredient_modified',
            utils.BIOSIMILAR: 'original_biosimilar_modified',
            utils.COMPANY: 'original_company_modified',
            utils.DRUG_PRODUCT: 'original_drug_product_modified',
            utils.FORM: 'original_form_modified',
            utils.INACTIVE_PRODUCT: 'original_inactive_product_modified',
            utils.PACKAGING: 'original_packaging_modified',
            utils.PHARMACEUTICAL_STANDARD: 'original_pharmaceutical_standard_modified',
            utils.ROUTE: 'original_route_modified',
            utils.SCHEDULE: 'original_schedule_modified',
            utils.STATUS: 'original_status_modified',
            utils.THERAPUETIC_CLASS: 'original_therapeutic_class_modified',
            utils.VETERINARY_SPECIES: 'original_veterinary_species_modified',
        }

        # Update the modified time and save model
        setattr(self, field_mapping[field], timezone.now())
        self.save()

    class Meta:
        verbose_name = 'DPD code'
        verbose_name_plural = 'DPD codes'
        permissions = (
            ('api_view', 'Can view DPD data via the API'),
            ('api_edit', 'Can edit DPD data via the API'),
            ('web_view', 'Can view DPD data via the web views'),
        )


class DPDChecksum(models.Model):
    """Holds checksum data of the original DPD data to identify changed data.

        Checksums are used to quickly identify when a record in the DPD
        extracts has changed. Checksums are calculated by:
            - Combining all DPD file types (e.g. marketed, cancelled) for an
              extract type (e.g. QRYM_BIOSIMILARS, QRYM_FORM);
            - Filtering to the desired range of items;
            - Converting all original data values to strings;
            - Concatenating all value for each item in the original order
              provided by the DPD;
            - Concatenating all these concatenated values in order of the
              smallest drug code to the largest; and then
            - Running the <TBD HASH> on the final concatenated product.
    """
    # Extract source file choices
    EXTRACT_SOURCE_CHOICES = (
        (utils.ACTIVE_INGREDIENT, 'QRYM_ACTIVE_INGREDIENTS'),
        (utils.BIOSIMILAR, 'QRYM_BIOSIMILARS'),
        (utils.COMPANY, 'QRYM_COMPANIES'),
        (utils.DRUG_PRODUCT, 'QRYM_DRUG_PRODUCT'),
        (utils.FORM, 'QRYM_FORM'),
        (utils.INACTIVE_PRODUCT, 'QRYM_INACTIVE_PRODUCTS'),
        (utils.PACKAGING, 'QRYM_PACKAGING'),
        (utils.PHARMACEUTICAL_STANDARD, 'QRYM_PHARMACEUTICAL_STD'),
        (utils.ROUTE, 'QRYM_ROUTE'),
        (utils.SCHEDULE, 'QRYM_SCHEDULE'),
        (utils.STATUS, 'QRYM_STATUS'),
        (utils.THERAPUETIC_CLASS, 'QRYM_THERAPEUTIC_CLASS'),
        (utils.VETERINARY_SPECIES, 'QRYM_VETERINARY_SPECIES'),
    )

    # Drug code step choices
    STEP_CHOICES = (
        (1, 1),
        (10, 10),
        (100, 100),
        (1000, 1000),
        (10000, 10000),
        (100000, 100000),
    )

    drug_code_start = models.PositiveIntegerField(
        help_text='The starting Health Canada Drug code for this checksum.',
    )
    drug_code_step = models.PositiveIntegerField(
        choices=STEP_CHOICES,
        help_text='The interval of drug codes for this checksum.',
    )
    extract_source = models.CharField(
        choices=EXTRACT_SOURCE_CHOICES,
        help_text='The extract source data for this checksum',
        max_length=32,
    )
    checksum = models.CharField(
        blank=True,
        help_text='The checksum value for the specified items.',
        max_length=10,
    )
    checksum_date = models.DateField(
        auto_now=True,
        help_text='The date this checksum was created or updated.'
    )

    def clean(self):
        """Method to allow additional validation steps.

            :raises ValidationError: if start value is not a multiple
                of the step
        """
        # Confirm a valid start and step are entered
        validate_checksum_start(self.drug_code_start, self.drug_code_step)

    def save(self, *args, **kwargs):
        """Extend save method to calculate a checksum."""
        # Run basic validation
        self.full_clean()

        # Once fields are confirmed as valid, run checksum method
        self.create_checksum()

        # Run normal save method
        super().save(*args, **kwargs)

    def create_checksum(self):
        """Uses instance information to create a checksum."""
        # Get the model for this extract source
        extract_model = utils.standard_to_original_model()[self.extract_source]

        # Calculate ending drug code for filter
        drug_code_end = self.drug_code_start + self.drug_code_step

        # Get a query for the proper drug code values
        query = extract_model.objects.filter(
            drug_code__pk__gte=self.drug_code_start,
            pk__lte=drug_code_end,
        )

        # Get the checksum string for this extract
        checksum_string = self._compile_checksum_string(
            query, extract_model.dpd_field_order()
        )

        # Calculate checksum for string
        checksum = self.calculate_checksum(checksum_string)

        # Update this DPDChecksum instance with the calculated checksum
        self.checksum = checksum

    @staticmethod
    def calculate_checksum(string):
        """Calculates checksum for a provided string.

            Uses the CRC32 algorithm, as this is expect to be fast enough
            for the API needs and the size of strings to create checksums
            are unlikely to result in meaningful collisions.

            :param str string: The string to calculate checksum for
            :return: The calculated checksum
            :rtype: str
        """
        # Convert string to bytes
        b_string = string.encode('utf-8')

        return crc32(b_string)

    @staticmethod
    def _compile_checksum_string(query, field_order):
        """Concatenates provided fields in query for checksum calculation.

            :param obj query: A Django queryset object.
            :param list[str] field_order: A list outlining order of fields.
            :return: The concatenated query data
            :rtype: str
        """
        checksum_string = ''

        for row in query:
            for field in field_order:
                checksum_string += str(getattr(row, field))

        return checksum_string

    class Meta:
        verbose_name = 'DPD checksum'
        verbose_name_plural = 'DPD checksums'
