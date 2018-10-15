from datetime import time

from django.db import models
from django.conf import settings

class CalendarUser(models.Model):
    sb_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='calendar_user',
    )

    name = models.CharField(
        help_text="The name of the user",
        max_length=25,
    )

    schedule_name = models.CharField(
        help_text="The name of the user on the Excel schedule",
        max_length=25,
    )

    calendar_name = models.CharField(
        help_text="The name of your calendar file",
        max_length=50,
        unique=True,
    )

    role = models.CharField(
        choices=(
            ("a", "Pharmacy Assistant"),
            ("p", "Pharmacist"),
            ("t", "Pharmacy Technician"),
        ),
        help_text="The role/profession of the user",
        max_length=1,
    )

    first_email_sent = models.BooleanField(
        default=False,
        help_text="Whether the welcome email has been sent or not",
    )

    full_day = models.BooleanField(
        default=False,
        help_text=(
            "Whether the .ics calender should show shifts as "
            "full day events or not"
        ),
    )

    reminder = models.IntegerField(
        help_text=(
            "How much time before the shift starts (in minutes) to "
            "provide a reminder (leave blank for no reminder)"
        ),
        blank=True,
        null=True
    )

    class Meta:
        permissions = (
            ("can_view", "Can view the RDRHC Calendar settings view"),
        )
        verbose_name = "RDRHC Calendar User"
        verbose_name_plural = "RDRHC Calendar Users"

    def __str__(self):
        return "{0} - {1}".format(self.role, self.name)

class StatHoliday(models.Model):
    date = models.DateField()

    class Meta:
        verbose_name = "Stat Holiday"
        verbose_name_plural = "Stat Holidays'"

    def __str__(self):
        return "{0}".format(self.date)

class ShiftCode(models.Model):
    code = models.CharField(
        help_text="The shift code used in the Excel schedule",
        max_length=20,
    )

    sb_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        help_text=(
            "Which user this shift code applies to (leave blank for "
            "a default entry)"
        ),
        null=True,
        on_delete=models.CASCADE,
    )

    role = models.CharField(
        choices=(
            ("a", "Pharmacy Assistant"),
            ("p", "Pharmacist"),
            ("t", "Pharmacy Technician"),
        ),
        help_text="The role/profession this code applies to",
        max_length=1,
    )

    monday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    monday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    tuesday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    tuesday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    wednesday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    wednesday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    thursday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    thursday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    friday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    friday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    saturday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    saturday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    sunday_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    sunday_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    stat_start = models.TimeField(
        blank=True,
        default=time(7, 0),
        help_text=(
            "The start time of the shift (leave blank if there should "
            "be no shift at this time)"
        ),
        null=True,
    )

    stat_duration = models.DecimalField(
        blank=True,
        decimal_places=2,
        default=15.00,
        help_text="The duration of the shift in hours (defaults to 15 hours)",
        max_digits=4,
        null=True,
    )

    class Meta:
        unique_together = ("code", "sb_user", "role",)
        verbose_name = "Shift Code"
        verbose_name_plural = "Shift Codes"

    def __str__(self):
        if self.sb_user:
            return "{0} - {1} - {2}".format(
                self.get_role_display(), self.sb_user, self.code
            )
        else:
            return "{0} - {1}".format(self.get_role_display(), self.code)

class Shift(models.Model):
    sb_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text="The user this shift applies to",
        on_delete=models.CASCADE,
    )

    date = models.DateField(
        help_text="The date of the shift",
    )

    shift_code = models.ForeignKey(
        ShiftCode,
        blank=True,
        help_text="The shift code for this shift",
        null=True,
        on_delete=models.CASCADE,
    )

    text_shift_code = models.CharField(
        help_text="Text representation of the shift code",
        max_length=20,
    )

    def __str__(self):
        return "{0} - {1}".format(self.date, self.shift_code)

class MissingShiftCode(models.Model):
    code = models.CharField(
        help_text="The shift code used in the Excel schedule",
        max_length=20,
    )

    role = models.CharField(
        choices=(
            ("a", "Pharmacy Assistant"),
            ("p", "Pharmacist"),
            ("t", "Pharmacy Technician"),
        ),
        help_text="The role/profession this code applies to",
        max_length=1,
    )

    def __str__(self):
        return "{0} - {1}".format(self.code, self.role)

    class Meta:
        permissions = (
            ("can_add_default_codes",
             "Can add new default codes to the ShiftCode database"),
        )
        unique_together = ["code", "role"]
