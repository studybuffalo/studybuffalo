from rest_framework import serializers

from rdrhc_calendar.models import CalendarUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarUser
        fields = (
            'id', 'sb_user', 'name', 'schedule_name', 'calendar_name', 'role',
            'first_email_sent', 'full_day', 'reminder',
        )
