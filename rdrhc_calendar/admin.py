from django.contrib import admin
from .models import CalendarUser, StatHoliday, ShiftCode, Shift

@admin.register(CalendarUser)
class CalendarUserAdmin(admin.ModelAdmin):
    model = CalendarUser
    
    list_display = (
        "name", "role", "schedule_name", "email", "first_email_sent"
    )
    list_filter = ("role",)
    ordering = ("role", "name",)

@admin.register(ShiftCode)
class ShiftCode(admin.ModelAdmin):
    model = ShiftCode
    
    list_display = ("code", "role", "user", "monday_start", "monday_duration")
    list_filter = ("role",)
    ordering = ("role", "user", "code",)

@admin.register(StatHoliday)
class StatHolidayAdmin(admin.ModelAdmin):
    model = StatHoliday

    ordering = ("date",)