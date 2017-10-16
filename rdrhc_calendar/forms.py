from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CalendarSettingsForm(forms.Form):
    calendar_name = forms.CharField(
        help_text="The name of your calendar",
        max_length="256",
    )

    full_day = forms.BooleanField(
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
    )