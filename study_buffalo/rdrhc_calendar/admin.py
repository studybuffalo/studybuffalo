"""Admin settings for the RDRHC Calendar app."""
from django.contrib import admin

from .models import CalendarUser, StatHoliday, ShiftCode, Shift


@admin.register(CalendarUser)
class CalendarUserAdmin(admin.ModelAdmin):
    """Admin for the Calendar User model."""
    model = CalendarUser

    list_display = (
        'name', 'role', 'schedule_name', 'first_email_sent'
    )
    list_filter = ('role',)
    ordering = ('role', 'name',)

@admin.register(ShiftCode)
class ShiftCodeAdmin(admin.ModelAdmin):
    """Admin for the Shift Code model."""
    model = ShiftCode

    list_display = ('code', 'role', 'sb_user', 'monday_start', 'monday_duration')
    list_filter = ('role',)
    ordering = ('role', 'sb_user', 'code',)

@admin.register(StatHoliday)
class StatHolidayAdmin(admin.ModelAdmin):
    """Admin for the Stat Holiday model."""
    model = StatHoliday

    ordering = ('date',)

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    """Admin for the Shift model."""
    model = Shift

    list_display = ('sb_user', 'date', 'text_shift_code')
    ordering = ('sb_user', 'date')
