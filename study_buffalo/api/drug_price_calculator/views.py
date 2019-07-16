"""Views for the Drug Price Calculator API."""
from django.db.models import Q

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from drug_price_calculator import models

from api.drug_price_calculator import serializers


class UploadiDBLData(GenericAPIView):
    serializer_class = serializers.iDBLDataSerializer

    def post(self, request, din):
        # Confirm DIN is in valid format
        if len(din) != 8:
            message = {
                'error': 'invalid_din',
                'error_description': 'DIN/NPN/PIN format is invalid.',
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create model instance
        drug, _ = models.Drug.objects.get_or_create(din=din)

        # Serializer and validate data
        serializer = self.get_serializer(data=request.data, instance=drug)

        if serializer.is_valid() is False:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the serializer data
        serializer.save()

        # Format response message
        message = {
            'message': 'Drug and price file successfully created',
            'drug_id': drug.id,
        }

        return Response(data=message, status=status.HTTP_201_CREATED)

class DrugListPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_query_param = 'page'

class DrugList(ListAPIView):
    """List of Drugs based on query filters."""
    serializer_class = serializers.DrugListSerializer
    permission_classes = []
    pagination_class = DrugListPagination

    def get_queryset(self):
        """Override to apply search filters."""
        q_string = self.request.GET.get('q', '')

        queryset = models.Drug.objects.filter(
            Q(generic_name__icontains=q_string) | Q(brand_name__icontains=q_string)
        ).exclude(
            prices__unit_price__isnull=True
        ).order_by(
            'generic_product'
        )

        return queryset

class DrugPriceList(ListAPIView):
    """List of drugs and prices based on requested products."""
    serializer_class = serializers.DrugPriceListSerializer
    permission_classes = []

    def get_queryset(self):
        """Overriding to apply filters."""
        try:
            drug_ids = self.request.GET['ids'].split(',')
        except KeyError:
            raise NotFound('No IDs provided in query')

        queryset = models.Price.objects.filter(
            drug__id__in=drug_ids
        )

        return queryset
