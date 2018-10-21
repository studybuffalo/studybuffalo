from datetime import datetime
import json

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import DataError
from django.db.models import Q
from django.shortcuts import get_object_or_404

from allauth.account.models import EmailAddress
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import generics, status

from rdrhc_calendar import models
from rdrhc_calendar.api import serializers
from rdrhc_calendar.api.permissions import HasAPIAccess


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, ))
@permission_classes((IsAuthenticated, HasAPIAccess, ))
def api_root(request, format=None): # pylint: disable=redefined-builtin
    return Response({
        'users': reverse('rdrhc_calendar:api_v1:user_list', request=request, format=format),
        'shifts': reverse('rdrhc_calendar:api_v1:shift_list', request=request, format=format),
    })

class UserList(generics.ListAPIView):
    queryset = models.CalendarUser.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CalendarUser.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

class UserEmailList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.EmailSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        user = get_user_model().objects.get(id=user_id)

        emails = EmailAddress.objects.filter(user=user)

        return emails

    def list(self, request, *args, **kwargs):
        return Response(self.get_queryset().values_list('email', flat=True))

class ShiftList(generics.ListAPIView):
    queryset = models.Shift.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.ShiftSerializer

class UserShiftCodesList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.ShiftCodesSerializer

    def get_queryset(self):
        # Get a reference to the main user model
        user_id = self.kwargs.get('user_id', None)
        user = get_user_model().objects.get(id=user_id)

        # Collect the user-specific codes
        user_codes = models.ShiftCode.objects.filter(sb_user=user)

        # Collect the default codes (i.e. no user)
        default_codes = models.ShiftCode.objects.filter(
            Q(role=user.calendar_user.role) & Q(sb_user__isnull=True)
        )

        # Add all the user_codes into the codes list
        codes = []

        for u_code in user_codes:
            codes.append(u_code)

        # Add any default codes that don't have a user code already
        for d_code in default_codes:
            if not any(d_code.code == code.code for code in codes):
                codes.append(d_code)

        return codes

class StatHolidaysList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.StatHolidaySerializer

    def get_queryset(self):
        date_start = self.request.GET.get('date_start', datetime(2001, 1, 1))
        date_end = self.request.GET.get('date_end', datetime(2025, 12, 31))

        queryset = models.StatHoliday.objects.all().filter(
            Q(date__gte=date_start) & Q(date__lte=date_end)
        )

        return queryset

    def list(self, request, *args, **kwargs):
        return Response(self.get_queryset().values_list('date', flat=True))

class UserScheduleList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )
    serializer_class = serializers.ShiftSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)

        queryset = models.Shift.objects.all().filter(
            sb_user=user_id
        ).order_by('date')

        return queryset

# TODO: See if this can be combined into the UserScheduleList
class UserScheduleDelete(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )

    def delete(self, request, user_id):
        shifts = models.Shift.objects.filter(sb_user=user_id)
        shifts.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class UserScheduleUpload(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )

    def post(self, request, user_id):
        try:
            schedule = serializers.ShiftSerializer(
                data=json.loads(request.POST.get('schedule')),
                many=True
            )
        except json.JSONDecodeError:
            return Response(
                data='Invalid JSON format received.',
                status=status.HTTP_400_BAD_REQUEST
            )

        if schedule.is_valid():
            schedule.save()

            response_message = (
                'Schedule successfully uploaded for user id = {}'.format(
                    user_id
                )
            )

            return Response(
                data={'message': response_message},
                status=status.HTTP_200_OK
            )

        return Response(
            data=schedule.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class UserEmailFirstSent(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )

    def post(self, request, user_id):
        calendar_user = get_object_or_404(models.CalendarUser, sb_user=user_id)
        calendar_user.first_email_sent = True
        calendar_user.save()

        return Response(status=status.HTTP_200_OK)

class MissingShiftCodesUpload(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, HasAPIAccess, )

    def post(self, request):
        try:
            codes = json.loads(request.POST.get('codes'))
        except json.JSONDecodeError:
            return Response(
                data='Invalid JSON format received.',
                status=status.HTTP_400_BAD_REQUEST
            )

        new_codes = []

        for code in codes:
            try:
                db_code, created = models.MissingShiftCode.objects.get_or_create(
                    code=code['code'], role=code['role']
                )

                if created:
                    new_codes.append(db_code.code)
            except (DataError, KeyError) as e:
                return Response(
                    data=str(e),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data=new_codes,
            status=status.HTTP_200_OK,
        )
