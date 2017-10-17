from django import forms
from .models import CalendarUser

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