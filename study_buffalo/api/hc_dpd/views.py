"""Views for the Drug Price Calculator API."""
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from api.hc_dpd import serializers, paginators, permissions
from api.utils import convert_serializer_errors
from hc_dpd import models


class UploadHCDPDData(GenericAPIView):
    """View to allow upload of new DPD data."""
    serializer_class = serializers.UploadHCDPDDataSerializer
    permission_classes = [permissions.HasDPDEditAccess]

    def post(self, request):
        """Perform POST call to update HC DPD data."""
        # Get serializer and validate data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() is False:
            # Convert serializer errors into a list
            message = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': convert_serializer_errors(serializer.errors),
            }

            return Response(
                data=message, status=status.HTTP_400_BAD_REQUEST
            )

        # Process data and create/update model instances
        message, status_code = serializer.create(serializer.validated_data)

        return Response(data=message, status=status_code)


class ChecksumList(ListAPIView):
    """View to return a list of checksum values."""
    pagination_class = paginators.ChecksumPagination
    serializer_class = serializers.ChecksumSerializer
    permission_classes = [
        permissions.HasDPDViewAccess | permissions.HasDPDEditAccess  # pylint: disable=unsupported-binary-operation
    ]

    def get_queryset(self):
        """Filters the queryset to the requested details"""
        # Confirm required query parameters are present.""""
        parameters = self._get_validated_parameters()

        return models.DPDChecksum.objects.filter(
            drug_code_step=parameters['step'],
            extract_source=parameters['source'],
        ).order_by('drug_code_start', 'pk')

    def _get_validated_parameters(self):
        serializer = serializers.ChecksumListParameterSerializer(
            data=self.request.query_params,
        )
        serializer.is_valid(raise_exception=True)

        return serializer.validated_data


class ChecksumTest(GenericAPIView):
    """View to test a client's checksum process."""
    serializer_class = serializers.ChecksumTestSerializer
    permission_classes = [
        permissions.HasDPDViewAccess | permissions.HasDPDEditAccess  # pylint: disable=unsupported-binary-operation
    ]

    def post(self, request):
        """Perform POST to validate a user's checksum."""
        # Get serializer and validate data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() is False:
            message = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': convert_serializer_errors(serializer.errors),
            }

            return Response(
                data=message, status=status.HTTP_400_BAD_REQUEST
            )

        message = serializer.test_checksum()

        # Return error if no data returned (i.e. no data submitted)
        if not message:
            message = {
                'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'errors': {
                    'non_field': ['No data submitted for testing.'],
                    'field': {},
                },
            }

            return Response(
                data=message, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        return Response(data=message, status=status.HTTP_200_OK)
