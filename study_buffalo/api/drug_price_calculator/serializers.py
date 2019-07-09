"""Serializers for the Drug Price Calculator API."""
from sentry_sdk import capture_message

from rest_framework import serializers

from drug_price_calculator import models


class iDBLClientsSerializer(serializers.Serializer):
    group_1 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_66 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_19823 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_19823a = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_19824 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_20400 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_20403 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_20514 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_22128 = serializers.BooleanField(
        default=False,
        required=False,
    )
    group_23609 = serializers.BooleanField(
        default=False,
        required=False,
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class iDBLSpecialAuthorizationSerializer(serializers.Serializer):
    file_name = serializers.CharField(
        help_text='The name of the PDF file',
        max_length=15,
    )
    pdf_title = serializers.CharField(
        help_text='The tile of the PDF',
        max_length=100,
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class iDBLCoverageCriteriaSerializer(serializers.Serializer):
    header = serializers.CharField(
        help_text='Any header for this criteria',
        max_length=200,
        required=False,
    )
    criteria = serializers.CharField(
        help_text='The coverage criteria',
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class iDBLDataSerializer(serializers.Serializer):
    """Serializer for extracted iDBL data."""
    abc_id = serializers.IntegerField(
        help_text='The Alberta Blue Cross iDBL ID number',
    )
    din = serializers.CharField(
        help_text='The drug DIN/NPN/PIN',
        max_length=8,
    )
    bsrf = serializers.CharField(
        help_text='The combined brand name, strength, route, and dosage form',
        required=False,
    )
    generic_name = serializers.CharField(
        help_text='The generic name of the drug',
        required=False,
    )
    ptc = serializers.CharField(
        help_text='The PTC for the drug',
        max_length=11,
        required=False,
    )
    date_listed = serializers.DateField(
        help_text='The date listed or date updated',
        required=False,
    )
    unit_price = serializers.DecimalField(
        decimal_places=4,
        help_text='The unit price (in CAD)',
        max_digits=10,
        required=False,
    )
    lca_price = serializers.DecimalField(
        decimal_places=4,
        help_text='The Least Cost Alternative price (in CAD)',
        max_digits=10,
        required=False,
    )
    mac_price = serializers.DecimalField(
        decimal_places=4,
        help_text='The Maximum Allowable Cost price (in CAD)',
        max_digits=10,
        required=False,
    )
    mac_text = serializers.CharField(
        help_text='Descriptions for the MAC pricing',
        max_length=150,
        required=False,
    )
    unit_of_issue = serializers.CharField(
        help_text='The unit of issue for pricing',
        max_length=25,
        required=False,
    )
    manufacturer = serializers.CharField(
        help_text='The drug manufacturer',
        max_length=75,
        required=False,
    )
    atc = serializers.CharField(
        help_text='The ATC for the drug',
        max_length=7,
    )
    schedule = serializers.CharField(
        help_text='The provincial drug schedule',
        max_length=10,
        required=False,
    )
    interchangeable = serializers.BooleanField(
        default=False,
        help_text='Whether are interchangeable products or not',
        required=False,
    )
    coverage_status = serializers.CharField(
        required=False,
        help_text='The coverage status of the drug',
        max_length=100,
    )
    clients = iDBLClientsSerializer(
        required=False,
    )
    special_authorization = iDBLSpecialAuthorizationSerializer(
        many=True,
        required=False,
    )
    coverage_criteria = iDBLCoverageCriteriaSerializer(
        many=True,
        required=False,
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        """Overriding update method."""
        # Parse the BSRF data
        brand_name, strength, route, dosage_form = parse.parse_bsrf(
            validated_data['bsrf']
        )

        # Parse the generic data
        generic_name = parse.parse_generic(validated_data['generic_name'])

        # Parse the manufacturer data
        manufacturer = parse.manufacturer(validated_data['manufacturer'])

        # Get ATC instance
        atc = self._get_atc_instance()

        # get PTC instance
        ptc = self._get_ptc_instance()

        # Update the instance
        instance.brand_name = brand_name
        instance.strength = strength
        instance.route = route
        instance.dosage_form = dosage_form
        instance.generic_name = generic_name
        instance.manufacturer = manufacturer
        instance.schedule = validated_data['schedule']
        instance.atc = atc
        instance.ptc = ptc
        instance.save()

        # Create or retrieve the Price model instance
        price, _ = models.Price.objects.get_or_create(drug=instance)

        # Update the price model
        price.abc_id = validated_data['abc_id']
        price.date_listed = validated_data['date_listed']


    def _get_atc_instance(self):
        """Retrieves ATC model for validated ATC value."""
        try:
            atc = models.ATC.objects.get(id=self.validated_data['atc'])
        except models.ATC.objects.DoesNotExist:
            atc = None
            message = 'Matching ATC model not found for FK {} (DIN: {})'.format(
                self.validated_data['atc'], self.validated_data['din']
            )
            capture_message(message=message, level=30)

        return atc

    def _get_ptc_instance(self):
        """Retrieves PTC model for validated PTC value."""
        try:
            ptc = models.PTC.objects.get(id=self.validated_data['ptc'])
        except models.PTC.objects.DoesNotExist:
            ptc = None
            message = 'Matching PTC model not found for FK {} (DIN: {})'.format(
                self.validated_data['ptc'], self.validated_data['din']
            )
            capture_message(message=message, level=30)

        return ptc
