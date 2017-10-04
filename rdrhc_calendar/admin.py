from django.contrib import admin
from .models import CalendarUser, StatHolidays, ShiftCode, Shift

admin.site.register(CalendarUser)
admin.site.register(ShiftCode)
admin.site.register(StatHolidays)

class CalendarUserAdmin(admin.ModelAdmin):
    model = CalendarUser
    list_display = (
        "name", "role", "schedule_name", "email", "first_email_sent"
    )

class ShiftCode(admin.ModelAdmin):
    model = ShiftCode
    list_display = ("code", "role", "user", "monday_start", "monday_duration")

class StatHolidayAdmin(admin.ModelAdmin):
    model = StatHolidays