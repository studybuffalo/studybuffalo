"""Serializers for the RDRHC Calendar API."""
from allauth.account.models import EmailAddress
from rest_framework import serializers

from rdrhc_calendar import models


class UserSerializer(serializers.ModelSerializer):
    """Seralizer for RDRHC Calendar users."""
    class Meta:
        model = models.CalendarUser
        fields = (
            'id', 'sb_user', 'name', 'schedule_name', 'calendar_name', 'role',
            'first_email_sent', 'full_day', 'reminder',
        )

class EmailSerializer(serializers.ModelSerializer):
    """Serializer for RDRHC Calendar user email."""
    class Meta:
        model = EmailAddress
        fields = ('email',)

class ShiftCodesSerializer(serializers.ModelSerializer):
    """Serializer for RDRHC Calendar shift code."""
    class Meta:
        model = models.ShiftCode
        fields = (
            'id', 'code', 'sb_user', 'role',
            'monday_start', 'monday_duration',
            'tuesday_start', 'tuesday_duration',
            'wednesday_start', 'wednesday_duration',
            'thursday_start', 'thursday_duration',
            'friday_start', 'friday_duration',
            'saturday_start', 'saturday_duration',
            'sunday_start', 'sunday_duration',
            'stat_start', 'stat_duration',
        )

class StatHolidaySerializer(serializers.ModelSerializer):
    """Serializer for RDRHC Calendar statutory holidays."""
    class Meta:
        model = models.StatHoliday
        fields = ('date',)

class ShiftSerializer(serializers.ModelSerializer):
    """Serializer for RDRHC Calendar shift."""
    class Meta:
        model = models.Shift
        fields = ('id', 'sb_user', 'date', 'shift_code', 'text_shift_code',)

class MissingShiftCodeSerializer(serializers.ModelSerializer):
    """Serializer for RDRHC Calendar missing shift."""
    class Meta:
        model = models.MissingShiftCode
        fields = ('id', 'code', 'role',)
