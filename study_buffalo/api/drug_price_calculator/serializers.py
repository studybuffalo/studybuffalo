"""Serializers for the Drug Price Calculator API."""
from sentry_sdk import capture_message

from rest_framework import serializers

from drug_price_calculator import models

from api.drug_price_calculator import parse


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
        default=None,
        help_text='The combined brand name, strength, route, and dosage form',
    )
    generic_name = serializers.CharField(
        default=None,
        help_text='The generic name of the drug',
    )
    ptc = serializers.CharField(
        default=None,
        help_text='The PTC for the drug',
        max_length=11,
    )
    date_listed = serializers.DateField(
        default=None,
        help_text='The date listed or date updated',
    )
    unit_price = serializers.DecimalField(
        decimal_places=4,
        default=None,
        help_text='The unit price (in CAD)',
        max_digits=10,
    )
    lca_price = serializers.DecimalField(
        decimal_places=4,
        default=None,
        help_text='The Least Cost Alternative price (in CAD)',
        max_digits=10,
    )
    mac_price = serializers.DecimalField(
        decimal_places=4,
        default=None,
        help_text='The Maximum Allowable Cost price (in CAD)',
        max_digits=10,
    )
    mac_text = serializers.CharField(
        default=None,
        help_text='Descriptions for the MAC pricing',
        max_length=150,
    )
    unit_issue = serializers.CharField(
        default=None,
        help_text='The unit of issue for pricing',
        max_length=25,
    )
    manufacturer = serializers.CharField(
        default=None,
        help_text='The drug manufacturer',
        max_length=75,
    )
    atc = serializers.CharField(
        default=None,
        help_text='The ATC for the drug',
        max_length=7,
    )
    schedule = serializers.CharField(
        default=None,
        help_text='The provincial drug schedule',
        max_length=10,
    )
    interchangeable = serializers.BooleanField(
        default=False,
        help_text='Whether are interchangeable products or not',
    )
    coverage_status = serializers.CharField(
        default=None,
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
        # Update the Drug instance
        drug = self._update_drug(instance)

        # Update the Price instance
        price = self._update_price(drug)

        # Update the Clients instance
        self._update_clients(price)

        # Update the SpecialAuthoriztions instances
        self._update_special_authorization(price)

        # Update the CoverageCriteria instances
        self._update_coverage_criteria(price)

        return instance

    def _get_atc_instance(self):
        """Retrieves ATC model for validated ATC value."""
        try:
            atc = models.ATC.objects.get(id=self.validated_data['atc'])
        except models.ATC.DoesNotExist:
            atc = None
            message = 'No matching ATC model for FK {} (DIN: {})'.format(
                self.validated_data['atc'], self.validated_data['din']
            )
            capture_message(message=message, level=30)

        return atc

    def _get_ptc_instance(self):
        """Retrieves PTC model for validated PTC value."""
        try:
            ptc = models.PTC.objects.get(id=self.validated_data['ptc'])
        except models.PTC.DoesNotExist:
            ptc = None
            message = 'No Matching PTC model for FK {} (DIN: {})'.format(
                self.validated_data['ptc'], self.validated_data['din']
            )
            capture_message(message=message, level=30)

        return ptc

    def _update_drug(self, drug):
        """Updates the Drug instance."""
        data = self.validated_data

        # Parse the BSRF data
        bsrf = parse.parse_bsrf(data['bsrf'])

        # Parse the generic data
        generic_name = parse.parse_generic(data['generic_name'])

        # Parse the manufacturer data
        manufacturer = parse.parse_manufacturer(data['manufacturer'])

        # Get ATC instance
        atc = self._get_atc_instance()

        # Get PTC instance
        ptc = self._get_ptc_instance()

        # Update the Drug instance
        drug.brand_name = bsrf['brand_name']
        drug.strength = bsrf['strength']
        drug.route = bsrf['route']
        drug.dosage_form = bsrf['dosage_form']
        drug.generic_name = generic_name
        drug.manufacturer = manufacturer
        drug.schedule = data['schedule']
        drug.atc = atc
        drug.ptc = ptc
        drug.save()

        return drug

    def _update_price(self, drug):
        """Updates the Price instance for this drug."""
        data = self.validated_data

        # Create or retrieve the Price model instance
        price, _ = models.Price.objects.get_or_create(
            drug=drug, abc_id=data['abc_id'],
        )

        # Parse the unit of issue
        unit_issue = parse.parse_unit_of_issue(data['unit_issue'])

        # Update the price model
        price.date_listed = data['date_listed']
        price.unit_price = data['unit_price']
        price.lca_price = data['lca_price']
        price.mac_price = data['mac_price']
        price.mac_text = data['mac_text']
        price.unit_issue = unit_issue
        price.interchangeable = data['interchangeable']
        price.coverage_status = data['coverage_status']
        price.save()

        # Remove any old price models
        old_prices = models.Price.objects.filter(drug=drug).exclude(id=price.id)
        old_prices.delete()

        return price

    def _update_clients(self, price):
        """Updates the Clients instance for provided price."""
        try:
            data = self.validated_data['clients']
        except KeyError:
            return None

        # Update Clients
        clients, _ = models.Clients.objects.get_or_create(price=price)

        clients.group_1 = data['group_1']
        clients.group_66 = data['group_66']
        clients.group_19823 = data['group_19823']
        clients.group_19823a = data['group_19823a']
        clients.group_19824 = data['group_19824']
        clients.group_20400 = data['group_20400']
        clients.group_20403 = data['group_20403']
        clients.group_20514 = data['group_20514']
        clients.group_22128 = data['group_22128']
        clients.group_23609 = data['group_23609']
        clients.save()

        # Remove old Clients models
        old_clients = models.Clients.objects.filter(
            price=price
        ).exclude(
            id=clients.id
        )
        old_clients.delete()

        return clients

    def _update_special_authorization(self, price):
        """Update SpecialAuthorization instances for provided price."""
        try:
            data = self.validated_data['special_authorization']
        except KeyError:
            return None

        # Collect model instances of Special Authorizations
        special_authorizations = []

        for special in data:
            special_instance, _ = models.SpecialAuthorization.objects.get_or_create(
                file_name=special['file_name'],
                pdf_title=special['pdf_title'],
            )
            special_authorizations.append(special_instance)

        # Replace the new SpecialAuthorization references
        price.special_authorizations.set(special_authorizations)

        return special_authorizations

    def _update_coverage_criteria(self, price):
        """Update CoverageCriteria instances for provided price."""
        try:
            data = self.validated_data['coverage_criteria']
        except KeyError:
            return None

        # Remove old CoverageCriteria models
        old_criteria = price.coverage_criteria.all()
        old_criteria.delete()

        # Update Coverage Criteria
        for criteria in data:
            models.CoverageCriteria.objects.get_or_create(
                price=price,
                header=criteria['header'],
                criteria=criteria['criteria'],
            )

        # No return value, so returns True
        return True
