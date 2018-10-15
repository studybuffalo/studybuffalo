from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics

from rdrhc_calendar import models
from rdrhc_calendar.api import serializers


@api_view(['GET'])
@authentication_classes((SessionAuthentication, TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def api_root(request, format=None): # pylint: disable=redefined-builtin
    return Response({
        'users': reverse('rdrhc_calendar:api_v1:user_list', request=request, format=format),
    })

class UserList(generics.ListCreateAPIView):
    queryset = models.CalendarUser.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CalendarUser.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer
    lookup_field = 'id'

class UserShiftCodesList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ShiftCodesSerializer

    def get_queryset(self):
        # Get a reference to the main user model
        app_name, model_name = settings.AUTH_USER_MODEL.split('.')
        user_model = apps.get_model(app_label=app_name, model_name=model_name)
        user_id = self.kwargs.get('id', None)
        user = get_object_or_404(user_model, id=user_id)

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

class StatHolidaysList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        date_start = self.request.GET.get('date_start', datetime(2001, 1, 1))
        date_end = self.request.GET.get('date_end', datetime(2025, 12, 31))

        queryset = models.StatHoliday.objects.all().filter(
            Q(date__gte=date_start) & Q(date__lte=date_end)
        )

        return queryset
