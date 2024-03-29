"""Serializers for the Drug Price Calculator API."""
from sentry_sdk import capture_message

from rest_framework import serializers

from drug_price_calculator import models

from api.drug_price_calculator import parse


class iDBLClientsSerializer(serializers.Serializer):
    """Serializer for the iDBL Clients."""
    group_1 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_66 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_19823 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_19823a = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_19824 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_20400 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_20403 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_20514 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_22128 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )
    group_23609 = serializers.BooleanField(
        allow_null=True,
        default=False,
        required=False,
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class iDBLSpecialAuthorizationSerializer(serializers.Serializer):
    """Serializer for Special Authorization details."""
    file_name = serializers.CharField(
        help_text='The name of the PDF file',
        max_length=15,
    )
    pdf_title = serializers.CharField(
        help_text='The tile of the PDF',
        max_length=200,
    )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class iDBLCoverageCriteriaSerializer(serializers.Serializer):
    """Serializer for Coverage Criteria."""
    header = serializers.CharField(
        allow_null=True,
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
        allow_null=True,
        default=None,
        help_text='The combined brand name, strength, route, and dosage form',
        max_length=390,
    )
    generic_name = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The generic name of the drug',
    )
    ptc = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The PTC for the drug',
        max_length=11,
    )
    date_listed = serializers.DateField(
        allow_null=True,
        default=None,
        help_text='The date listed or date updated',
    )
    unit_price = serializers.DecimalField(
        allow_null=True,
        decimal_places=4,
        default=None,
        help_text='The unit price (in CAD)',
        max_digits=10,
    )
    lca_price = serializers.DecimalField(
        allow_null=True,
        decimal_places=4,
        default=None,
        help_text='The Least Cost Alternative price (in CAD)',
        max_digits=10,
    )
    mac_price = serializers.DecimalField(
        allow_null=True,
        decimal_places=4,
        default=None,
        help_text='The Maximum Allowable Cost price (in CAD)',
        max_digits=10,
    )
    mac_text = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='Descriptions for the MAC pricing',
        max_length=150,
    )
    unit_issue = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The unit of issue for pricing',
        max_length=25,
    )
    manufacturer = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The drug manufacturer',
        max_length=150,
    )
    atc = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The ATC for the drug',
        max_length=7,
    )
    schedule = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The provincial drug schedule',
        max_length=10,
    )
    interchangeable = serializers.BooleanField(
        allow_null=True,
        default=False,
        help_text='Whether are interchangeable products or not',
    )
    coverage_status = serializers.CharField(
        allow_null=True,
        default=None,
        help_text='The coverage status of the drug',
        max_length=100,
    )
    clients = iDBLClientsSerializer(
        allow_null=True,
        required=False,
    )
    special_authorization = iDBLSpecialAuthorizationSerializer(
        allow_null=True,
        many=True,
        required=False,
    )
    coverage_criteria = iDBLCoverageCriteriaSerializer(
        allow_null=True,
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
        # If no values, can exit and return none
        if not self.validated_data['atc']:
            return None

        # See if this exact reference exists
        atc, created = models.ATC.objects.get_or_create(id=self.validated_data['atc'])

        # If this was created, add the level 5 code
        if created:
            atc.atc_5 = self.validated_data['atc']
            atc.save()

            # Try to fill in other details from another code
            atc_4 = models.ATC.objects.filter(
                atc_4=self.validated_data['atc'][:-2]  # type: ignore
            ).first()

            if atc_4:
                atc.atc_1 = atc_4.atc_1
                atc.atc_1_text = atc_4.atc_1_text
                atc.atc_2 = atc_4.atc_2
                atc.atc_2_text = atc_4.atc_2_text
                atc.atc_3 = atc_4.atc_3
                atc.atc_3_text = atc_4.atc_3_text
                atc.atc_4 = atc_4.atc_4
                atc.atc_4_text = atc_4.atc_4_text
                atc.save()
            else:
                # No matches for other ATC does send message
                message = (
                    f'No Matching ATC model for FK {self.validated_data["ptc"]} (DIN: {self.validated_data["din"]})'
                )
                capture_message(message=message, level=20)

        return atc

    def _get_ptc_instance(self):
        """Retrieves PTC model for validated PTC value."""
        # If no values, can exit and return none
        if not self.validated_data['ptc']:
            return None

        # Get reference
        ptc, created = models.PTC.objects.get_or_create(id=self.validated_data['ptc'])

        if created:
            # Send message to notify of missing PTC data
            message = (
                f'No Matching PTC model for FK {self.validated_data["ptc"]} (DIN: {self.validated_data["din"]})'
            )
            capture_message(message=message, level=20)

        return ptc

    def _update_drug(self, drug):
        """Updates the Drug instance."""
        data = self.validated_data

        # Parse the BSRF data
        bsrf = parse.parse_bsrf(data['bsrf'])

        # Parse the generic data
        generic_name = parse.parse_generic(data['generic_name'])

        # Assemble the generic_product name
        generic_product = parse.assemble_generic_product(bsrf, generic_name)

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
        drug.generic_product = generic_product
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
        unit_issue = parse.parse_unit_issue(data['unit_issue'])

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

        clients.group_1 = data['group_1']  # type: ignore
        clients.group_66 = data['group_66']  # type: ignore
        clients.group_19823 = data['group_19823']  # type: ignore
        clients.group_19823a = data['group_19823a']  # type: ignore
        clients.group_19824 = data['group_19824']  # type: ignore
        clients.group_20400 = data['group_20400']  # type: ignore
        clients.group_20403 = data['group_20403']  # type: ignore
        clients.group_20514 = data['group_20514']  # type: ignore
        clients.group_22128 = data['group_22128']  # type: ignore
        clients.group_23609 = data['group_23609']  # type: ignore
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


class DrugListSerializer(serializers.ModelSerializer):
    """Serializer to list drugs."""
    class Meta:
        model = models.Drug
        fields = (
            'id', 'brand_name', 'generic_name', 'strength', 'route',
            'dosage_form', 'generic_product',
        )


class ATCDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide ATC details."""
    class Meta:
        model = models.ATC
        fields = (
            'id', 'atc_1', 'atc_1_text', 'atc_2', 'atc_2_text',
            'atc_3', 'atc_3_text', 'atc_4', 'atc_4_text',
            'atc_5', 'atc_5_text',
        )


class PTCDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide PTC details."""
    class Meta:
        model = models.PTC
        fields = (
            'id', 'ptc_1', 'ptc_1_text', 'ptc_2', 'ptc_2_text',
            'ptc_3', 'ptc_3_text', 'ptc_4', 'ptc_4_text',
        )


class DrugDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide drug details."""
    atc = ATCDetailSerializer()
    ptc = PTCDetailSerializer()

    class Meta:
        model = models.Drug
        fields = (
            'id', 'din', 'brand_name', 'strength', 'route', 'dosage_form',
            'generic_name', 'manufacturer', 'schedule', 'atc', 'ptc',
            'generic_product'
        )


class ClientsDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide details on clients."""
    class Meta:
        model = models.Clients
        fields = (
            'id', 'group_1', 'group_66', 'group_19823', 'group_19823a',
            'group_19824', 'group_20400', 'group_20403', 'group_20514',
            'group_22128', 'group_23609',
        )


class SpecialAuthorizationDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide details on Special Authorization."""
    class Meta:
        model = models.SpecialAuthorization
        fields = ('file_name', 'pdf_title')


class CoverageCriteriaDetailSerializer(serializers.ModelSerializer):
    """Serializer to provide details on Coverage Criteria."""
    class Meta:
        model = models.CoverageCriteria
        fields = ('header', 'criteria')


class DrugPriceListSerializer(serializers.ModelSerializer):
    """Serializer to provide drug price list."""
    drug = DrugDetailSerializer()
    clients = ClientsDetailSerializer()
    special_authorizations = SpecialAuthorizationDetailSerializer(many=True)
    coverage_criteria = CoverageCriteriaDetailSerializer(many=True)

    class Meta:
        model = models.Price
        fields = (
            'id', 'drug', 'unit_price', 'lca_price', 'mac_price', 'mac_text',
            'unit_issue', 'coverage_status', 'special_authorizations',
            'clients', 'coverage_criteria',
        )
