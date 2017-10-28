from django import forms
from .models import CalendarUser, ShiftCode

class CalendarSettingsForm(forms.ModelForm):
    full_day = forms.ChoiceField(
        choices=(
            ("False", "No"),
            ("True", "Yes"),
        ),
        help_text=(
            "Whether your schedule should display your shifts as "
            "full day events or not"
        ),
    )

    reminder = forms.IntegerField(
        help_text=(
            "How much time before the shift to display a calendar "
            "reminder (leave blank for no reminder)"
        ),
        max_value=60,
        min_value=0,
        required=False,
    )

    class Meta:
        model = CalendarUser
        fields = [
            "calendar_name",
            "full_day",
            "reminder",
        ]

class CalendarShiftCodeForm(forms.ModelForm):
    code = forms.CharField(
        help_text="The shift code used in the Excel schedule",
        max_length=20,
    )

    class Meta:
        model = ShiftCode
        fields = [
            "code",
            "monday_start",
            "monday_duration",
            "tuesday_start",
            "tuesday_duration",
            "wednesday_start",
            "wednesday_duration",
            "thursday_start",
            "thursday_duration",
            "friday_start",
            "friday_duration",
            "saturday_start",
            "saturday_duration",
            "sunday_start",
            "sunday_duration",
            "stat_start",
            "stat_duration",
        ]
        
class MissingCodeForm(forms.ModelForm):
    class Meta:
        model = ShiftCode
        fields = [
            "monday_start",
            "monday_duration",
            "tuesday_start",
            "tuesday_duration",
            "wednesday_start",
            "wednesday_duration",
            "thursday_start",
            "thursday_duration",
            "friday_start",
            "friday_duration",
            "saturday_start",
            "saturday_duration",
            "sunday_start",
            "sunday_duration",
            "stat_start",
            "stat_duration",
        ]