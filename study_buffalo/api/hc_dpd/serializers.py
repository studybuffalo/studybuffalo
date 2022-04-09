"""Serializers for the Drug Price Calculator API."""
from django.core.exceptions import ValidationError

from rest_framework import serializers, status

from hc_dpd import models, utils


class ActiveIngredientSerializer(serializers.ModelSerializer):
    """Serializer representing data from the QRYM_ACTIVE_INGREDIENTS file."""
    drug_code = serializers.IntegerField(
        help_text='The DRUG_CODE entry for this item.',
        min_value=1,
        required=True,
    )

    class Meta:
        # Get fields from field_order and remove drug code
        serializer_fields = models.OriginalActiveIngredient.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalBiosimilar.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalCompany.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalDrugProduct.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalForm.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalInactiveProduct.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalPackaging.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalPharmaceuticalStandard.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalRoute.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalSchedule.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalStatus.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalTherapeuticClass.field_order
        serializer_fields.remove('drug_code')

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
        serializer_fields = models.OriginalVeterinarySpecies.field_order
        serializer_fields.remove('drug_code')

        model = models.OriginalVeterinarySpecies
        fields = serializer_fields


class UploadHCDPDDataSerializer(serializers.Serializer):
    """Serializer to manage requests to update HC DPD data."""
    active_ingredients = ActiveIngredientSerializer(
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

    def create(self, validated_data):  # pylint: disable=too-many-locals
        """Create or update new database entries when needed."""
        message = []
        status_check = {'201': False, '400': False}
        status_code = None

        for file_type, file_data in validated_data.items():
            # Group drug codes together to allow updates to occur together
            grouped_data = self._group_upload_data(file_data)

            # Iterate through grouped data and make required updates
            for drug_code, items in grouped_data.items():
                # Get or create the DPD model instance
                dpd_instance, _ = models.DPD.objects.get_or_create(pk=drug_code)

                # Get relevant model for this file type
                model = utils.standard_to_original_model()[file_type]

                # Delete any existing model intance(s)
                model.objects.filter(drug_code=dpd_instance).delete()

                # Create the required model instance for each item
                for item in items:
                    # Remove the drug_code entry as it is not needed
                    item.pop('drug_code')

                    try:
                        model_instance = model.objects.create(
                            drug_code=dpd_instance,
                            defaults=item,
                        )

                        message.append({
                            'status_code': status.HTTP_201_CREATED,
                            'file_type': file_type,
                            'id': model_instance.id,
                            'drug_code': drug_code,
                        })
                        status_check['201'] = True
                    except ValidationError as e:
                        message.append({
                            'status_code': status.HTTP_400_BAD_REQUEST,
                            'errors': [f'Could not create entry ({item}): {e}']
                        })
                        status_check['400'] = True

                # Update the modified time for this file type
                dpd_instance.update_modified(file_type)

        # Determine final status code based on model creation
        if status_check['201'] and status_check['400']:
            status_code = status.HTTP_207_MULTI_STATUS
        elif status_check['201']:
            status_code = status.HTTP_201_CREATED
        elif status_check['400']:
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            message.append({
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': ['No data submitted for upload.']
            })

        return message, status_code

    def update(self, instance, validated_data):
        """Abstract method that is not required."""
        # https://docs.python.org/3/library/exceptions.html#NotImplementedError
        return None

    @staticmethod
    def _group_upload_data(data):
        """Groups upload data in a dictionary with drug_code as the key."""
        grouped_data = {}

        for item in data:
            if item['drug_code'] in grouped_data:
                grouped_data[item['drug_code']].append(item)
            else:
                grouped_data[item['drug_code']] = [item]

        return grouped_data


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
