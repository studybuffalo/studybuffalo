"""Views for the Drug Price Calculator API."""
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from drug_price_calculator import models

from api.drug_price_calculator.serializers import iDBLDataSerializer


class UploadiDBLData(GenericAPIView):
    serializer = iDBLDataSerializer

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
        serializer = self.get_serializer(data=request, instance=drug)

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
