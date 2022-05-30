"""Views for the Drug Price Calculator API."""
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from api.hc_dpd import serializers, paginators, permissions
from hc_dpd import models


class UploadHCDPDData(GenericAPIView):
    """View to allow upload of new DPD data.

        Build to accept multiple entries at once to reduce # of requests.
    """
    serializer_class = serializers.UploadHCDPDDataSerializer
    permission_classes = [permissions.HasDPDEditAccess]

    def post(self, request):
        """Perform POST call to update HC DPD data."""
        # Get serializer and validate data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() is False:
            message = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }

            return Response(
                data=message, status=status.HTTP_400_BAD_REQUEST
            )

        # Process data and create/update model instances
        message, status_code = serializer.create(serializer.validated_data)

        return Response(data=message, status=status_code)


class ChecksumList(ListAPIView):
    """View to return a list of checksum values.

        Can be a GET request
        Need to intake a file name type and checksum range (start & stop)
        Need to return proper message on no match found
    """
    pagination_class = paginators.ChecksumPagination
    serializer_class = serializers.UploadHCDPDDataSerializer
    permission_classes = [
        permissions.HasDPDViewAccess|permissions.HasDPDEditAccess  # pylint: disable=unsupported-binary-operation
    ]

    def get_queryset(self):
        """Filters the queryset to the requested details"""
        # Confirm required query parameters are present.""""
        self._validate_parameters()

        return models.DPDChecksum.objects.filter(
            drug_code_step=self.request.query_params['step'],
            extract_source=self.request.query_params['source'],
        )

    def _validate_parameters(self):
        serializer = serializers.ChecksumListParameterSerializer(
            data=self.request.query_params,
        )
        serializer.is_valid(raise_exception=True)


class ChecksumTest(GenericAPIView):
    """View to test a client's checksum process."""
    serializer_class = serializers.ChecksumTestSerializer
    permission_classes = [
        permissions.HasDPDViewAccess|permissions.HasDPDEditAccess  # pylint: disable=unsupported-binary-operation
    ]

    def post(self, request):
        """Perform POST to validate a user's checksum."""
        # Get serializer and validate data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid() is False:
            message = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': serializer.errors
            }

            return Response(
                data=message, status=status.HTTP_400_BAD_REQUEST
            )

        message = self._test_checksum_string(serializer.validated_data)

        return Response(data=message, status=status.HTTP_200_OK)

    @staticmethod
    def _test_checksum_string(data):
        """Determines if user data matches app-generated checksum."""
        return {
            'user_string': '',
            'user_checksum': '',
            'app_checksum': '',
            'checksum_valid': True,
        }
