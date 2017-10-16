from django.shortcuts import render
from .forms import CalendarSettingsForm

def calendar_index(request):
    """View for the tool page"""
    return render(
        request,
        "rdrhc_calendar/index.html",
        context={},
    )

def calendar_settings(request):
    form = CalendarSettingsForm()

    return render(
        request, 
        "rdrhc_calendar/calendar_settings.html", 
        {'form': form}
    )