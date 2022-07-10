"""Serializers for the Drug Price Calculator API."""
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import DataError
from rest_framework import serializers, status

from hc_dpd import models, utils
from api.hc_dpd.validators import AscendingDrugCode


class ActiveIngredientSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_ACTIVE_INGREDIENTS file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order
        serializer_fields = models.OriginalActiveIngredient.dpd_field_order()

        # Meta declarations
        model = models.OriginalActiveIngredient
        fields = serializer_fields


class BiosimilarSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_BIOSIMILARS file.

        Default create implementation raises TypeError if something
        goes wrong - will need to catch that.

        Either need to override create entirely to handle drug_code
        relationship, or look at injecting that data into the validated
        data.
    """
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalBiosimilar.dpd_field_order()

        model = models.OriginalBiosimilar
        fields = serializer_fields


class CompanySerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_COMPANIES file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalCompany.dpd_field_order()

        model = models.OriginalCompany
        fields = serializer_fields


class DrugProductSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_DRUG_PRODUCT file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalDrugProduct.dpd_field_order()

        model = models.OriginalDrugProduct
        fields = serializer_fields


class FormSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_FORM file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalForm.dpd_field_order()

        model = models.OriginalForm
        fields = serializer_fields


class InactiveProductSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_INACTIVE_PRODUCTS file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalInactiveProduct.dpd_field_order()

        model = models.OriginalInactiveProduct
        fields = serializer_fields


class PackagingSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_Packaging file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalPackaging.dpd_field_order()

        model = models.OriginalPackaging
        fields = serializer_fields


class PharmaceuticalStandardSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_PHARMACEUTICAL_STD file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalPharmaceuticalStandard.dpd_field_order()

        model = models.OriginalPharmaceuticalStandard
        fields = serializer_fields


class RouteSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_ROUTE file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalRoute.dpd_field_order()

        model = models.OriginalRoute
        fields = serializer_fields


class ScheduleSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_SCHEDULE file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalSchedule.dpd_field_order()

        model = models.OriginalSchedule
        fields = serializer_fields


class StatusSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_STATUS file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalStatus.dpd_field_order()

        model = models.OriginalStatus
        fields = serializer_fields


class TherapeuticClassSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_THERAPEUTIC_CLASS file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalTherapeuticClass.dpd_field_order()

        model = models.OriginalTherapeuticClass
        fields = serializer_fields


class VeterinarySpeciesSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_VETERINARY_SPECIES file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalVeterinarySpecies.dpd_field_order()

        model = models.OriginalVeterinarySpecies
        fields = serializer_fields


class UploadDPDExtractsSerializer(serializers.Serializer):
    """Serializer for the extract data to upload."""
    active_ingredient = ActiveIngredientSerializer(
        help_text='Data from the QRYM_ACTIVE_INGREDIENTS file.',
        many=True,
        required=False,
    )
    biosimilar = BiosimilarSerializer(
        help_text='Data from the QRYM_BIOSIMILARS file.',
        many=True,
        required=False,
    )
    company = CompanySerializer(
        help_text='Data from the QRYM_COMPANIES file.',
        many=True,
        required=False,
    )
    drug_product = DrugProductSerializer(
        help_text='Data from the QRYM_DRUG_PRODUCT file.',
        many=True,
        required=False,
    )
    form = FormSerializer(
        help_text='Data from the QRYM_FORM file.',
        many=True,
        required=False,
    )
    inactive_product = InactiveProductSerializer(
        help_text='Data from the QRYM_INACTIVE_PRODUCTS file.',
        many=True,
        required=False,
    )
    packaging = PackagingSerializer(
        help_text='Data from the QRYM_Packaging file.',
        many=True,
        required=False,
    )
    pharmaceutical_standard = PharmaceuticalStandardSerializer(
        help_text='Data from the QRYM_PHARMACEUTICAL_STD file.',
        many=True,
        required=False,
    )
    route = RouteSerializer(
        help_text='Data from the QRYM_ROUTE file.',
        many=True,
        required=False,
    )
    schedule = ScheduleSerializer(
        help_text='Data from the QRYM_SCHEDULE file.',
        many=True,
        required=False,
    )
    status = StatusSerializer(
        help_text='Data from the QRYM_STATUS file.',
        many=True,
        required=False,
    )
    therapeutic_class = TherapeuticClassSerializer(
        help_text='Data from the QRYM_THERAPEUTIC_CLASS file.',
        many=True,
        required=False,
    )
    veterinary_species = VeterinarySpeciesSerializer(
        help_text='Data from the QRYM_VETERINARY_SPECIES file.',
        many=True,
        required=False,
    )

    def create(self, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None


class UploadDPDAndExtractsSerializer(serializers.Serializer):
    """Groups together drug code field and related field serializer."""
    drug_code = serializers.IntegerField(
        help_text='The drug code for the upload data.',
        min_value=1,
        required=True,
    )
    extract_data = UploadDPDExtractsSerializer(
        help_text='The extract data to upload with this drug code.',
        required=True,
    )

    def create(self, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None


class UploadHCDPDDataSerializer(serializers.Serializer):
    """Serializer to manage requests to update HC DPD data."""
    data = UploadDPDAndExtractsSerializer(
        help_text='The data to upload.',
        many=True,
        required=True,
    )

    def create(self, validated_data):  # pylint: disable=too-many-locals
        """Create or update new database entries when needed."""
        message_list = []
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        # Setup a dictionary to organize bulk data
        bulk_data = {
            'active_ingredient': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'biosimilar': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'company': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'drug_product': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'form': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'inactive_product': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'packaging': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'pharmaceutical_standard': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'route': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'schedule': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'status': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'therapeutic_class': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
            'veterinary_species': {
                'drug_codes': [],
                'dpd_instances': [],
                'extract_data': [],
                'model': None,
            },
        }

        # Add model to bulk data for easier reference
        original_model_mapping = utils.standard_to_original_model()
        for extract_type, data in bulk_data.items():
            data['model'] = original_model_mapping[extract_type]

        # Get the modified field mapping for easier reference
        dpd_modified_mapping = models.DPD.original_modified_field_mapping()

        # Iterate through each collection of drug codes & extract data
        for post_data in validated_data['data']:
            # Get or create the DPD model instance
            drug_code = post_data['drug_code']
            dpd_instance, _ = models.DPD.objects.get_or_create(pk=drug_code)

            # Loop through all the extract type fields
            for extract_type, extract_data in post_data['extract_data'].items():
                # Collect all drug codes for this extract data
                bulk_data[extract_type]['drug_codes'].append(drug_code)
                bulk_data[extract_type]['dpd_instances'].append(dpd_instance)

                # Get relevant model for this file type
                model = bulk_data[extract_type]['model']

                for item in extract_data:
                    # Add the drug code reference to this item
                    item['drug_code'] = dpd_instance

                    # Create a model object for future bulk upload
                    bulk_data[extract_type]['extract_data'].append(model(**item))

        # Loop through all the organized bulk data
        for extract_type, data in bulk_data.items():
            # Skip processing if no data present
            if len(data['extract_data']) == 0:
                continue

            # Bulk delete any existing extract data with updates
            data['model'].objects.filter(drug_code__in=data['drug_codes']).delete()

            # Complete the bulk creation
            try:
                data['model'].objects.bulk_create(data['extract_data'])
            except (ValidationError, DataError) as e:
                error_message = f'Could not complete upload: {e}'
                status_code = status.HTTP_400_BAD_REQUEST

                # DB error has occurred - need to break because this
                # atomic transaction will prevent all future queries
                break

            # Bulk create successful - add to message list
            message_list.append({
                'file_type': extract_type,
                'drug_codes': data['drug_codes'],
            })
            status_code = status.HTTP_201_CREATED

            # Update the appropriate DPD instnace modified time field
            for instance in data['dpd_instances']:
                instance.update_modified(extract_type, bulk=True)

            models.DPD.objects.bulk_update(
                data['dpd_instances'], (dpd_modified_mapping[extract_type],)
            )

        # Handles situations when no data was submitted
        if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            # Revert transaction to prevent DPD instances from being saved
            transaction.set_rollback(True)
            error_message = 'No data submitted for upload.'

        # Format the final message based on status code
        if status_code == status.HTTP_201_CREATED:
            message = {
                'status_code': status_code,
                'message': message_list,
            }
        else:
            message = {
                'status_code': status_code,
                'errors': {
                    'non_field': [error_message],
                    'field': {},
                },
            }

        return message, status_code

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None


class ChecksumSerializer(serializers.ModelSerializer):
    """Serializer for DPDChecksum model data."""
    class Meta:
        model = models.DPDChecksum
        fields = [
            'drug_code_start',
            'drug_code_step',
            'extract_source',
            'checksum',
            'checksum_date',
        ]


class ChecksumListParameterSerializer(serializers.Serializer):
    """Serializer to validate URL parameters for ChecksumList view."""
    step = serializers.ChoiceField(
        choices=models.DPDChecksum.STEP_CHOICES,
        help_text='The interval of drug codes for this checksum.',
    )
    source = serializers.ChoiceField(
        choices=models.DPDChecksum.EXTRACT_SOURCE_CHOICES,
        help_text='The extract source data for this checksum',
    )

    def create(self, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None


class ChecksumTestSerializer(serializers.Serializer):
    """Serializer to validate POST data for testing Checksums."""
    active_ingredient = ActiveIngredientSerializer(
        help_text='Data from the QRYM_ACTIVE_INGREDIENTS file.',
        many=True,
        required=False,
    )
    biosimilar = BiosimilarSerializer(
        help_text='Data from the QRYM_BIOSIMILARS file.',
        many=True,
        required=False,
    )
    company = CompanySerializer(
        help_text='Data from the QRYM_COMPANIES file.',
        many=True,
        required=False,
    )
    drug_product = DrugProductSerializer(
        help_text='Data from the QRYM_DRUG_PRODUCT file.',
        many=True,
        required=False,
    )
    form = FormSerializer(
        help_text='Data from the QRYM_FORM file.',
        many=True,
        required=False,
    )
    inactive_product = InactiveProductSerializer(
        help_text='Data from the QRYM_INACTIVE_PRODUCTS file.',
        many=True,
        required=False,
    )
    packaging = PackagingSerializer(
        help_text='Data from the QRYM_Packaging file.',
        many=True,
        required=False,
    )
    pharmaceutical_standard = PharmaceuticalStandardSerializer(
        help_text='Data from the QRYM_PHARMACEUTICAL_STD file.',
        many=True,
        required=False,
    )
    route = RouteSerializer(
        help_text='Data from the QRYM_ROUTE file.',
        many=True,
        required=False,
    )
    schedule = ScheduleSerializer(
        help_text='Data from the QRYM_SCHEDULE file.',
        many=True,
        required=False,
    )
    status = StatusSerializer(
        help_text='Data from the QRYM_STATUS file.',
        many=True,
        required=False,
    )
    therapeutic_class = TherapeuticClassSerializer(
        help_text='Data from the QRYM_THERAPEUTIC_CLASS file.',
        many=True,
        required=False,
    )
    veterinary_species = VeterinarySpeciesSerializer(
        help_text='Data from the QRYM_VETERINARY_SPECIES file.',
        many=True,
        required=False,
    )

    def create(self, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    def test_checksum(self):
        """Calculates checksum & checksum string to validate client process."""
        checksums = {}

        # Loops through each batch of submitted data to calculate checksums
        for source_file, source_data in self.validated_data.items():
            # Get the field order for this extract source
            field_order = utils.standard_to_original_model()[source_file].dpd_field_order()

            # Compiles string from the submitted data
            checksum_string = self.compile_checksum_string(source_data, field_order)

            # Calculate checksum for string
            calculated_checksum = models.DPDChecksum.calculate_checksum(checksum_string)

            # Update checksum data
            checksums[source_file] = {
                'server_checksum_string': checksum_string,
                'server_checksum': calculated_checksum,
            }

        return checksums

    @staticmethod
    def compile_checksum_string(data, field_order):
        """Concatenates provided fields in data for checksum calculation.

            :param list[dict] data: a list of dictionaries containing data.
            :param list[str] field_order: A list outlining order of fields.
            :return: The concatenated query data
            :rtype: str
        """
        checksum_string = ''

        for row in data:
            row_dict = dict(row)

            for field in field_order:
                checksum_string += str(row_dict.get(field, ''))

        return checksum_string

    class Meta:
        validators = [AscendingDrugCode()]
