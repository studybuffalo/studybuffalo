from django import forms
from django.core.exceptions import ValidationError

from .models import AppData

class AppDataForm(forms.ModelForm):
    class Meta:
        model = AppData

        fields = [
            "name",
            "log_location",
            "file_name",
            "flag_start",
            "flag_end",
            "review_minute",
            "review_hour",
            "review_day",
            "review_month",
            "review_weekday",
            "next_review",
        ]