from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CalendarSettingsForm, CalendarShiftCodeForm
from .models import CalendarUser, ShiftCode

# from .models import CalendarUser

def calendar_index(request):
    """View for the tool page"""
    return render(
        request,
        "rdrhc_calendar/index.html",
        context={},
    )

@permission_required("rdrhc_calendar.can_view", login_url="/accounts/login/")
def calendar_settings(request):
    user_settings = get_object_or_404(CalendarUser, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CalendarSettingsForm(request.POST, instance=user_settings)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            calendar_name = form.cleaned_data['calendar_name']
            full_day = form.cleaned_data['full_day']
            reminder = form.cleaned_data['reminder']

            # Upate the user settings
            user_settings.calendar_name = calendar_name
            user_settings.full_day = full_day
            user_settings.reminder = reminder

            user_settings.save()

            # redirect to a new URL:
            messages.success(request, "Settings updated")
            return HttpResponseRedirect(reverse('calendar_settings'))

    # If this is a GET (or any other method) create the default form.
    else:
        # Set the default form fields
        calendar_name = user_settings.calendar_name
        full_day = user_settings.full_day
        reminder = user_settings.reminder

        form = CalendarSettingsForm(initial={
            "calendar_name": calendar_name,
            "full_day": full_day,
            "reminder": reminder,
        })

    return render(
        request, 
        "rdrhc_calendar/calendar_settings.html", 
        {'form': form}
    )

class ShiftCodeList(generic.ListView):
    context_object_name = "shift_code_list"
    template_name = "shiftcode_list.html"

    def get_queryset(self):
        return ShiftCode.objects.filter(user=self.request.sb_user)

@permission_required("rdrhc_calendar.can_view", login_url="/accounts/login/")
def calendar_shift_code(request):
    shift = get_object_or_404(Shift, pk=request.shift.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CalendarShiftCodeForm(request.POST, instance=shift)

        # Check if the form is valid:
        """
        if form.is_valid():
            # Collect the form fields
            calendar_name = form.cleaned_data['calendar_name']
            full_day = form.cleaned_data['full_day']
            reminder = form.cleaned_data['reminder']

            # Upate the user settings
            user_settings.calendar_name = calendar_name
            user_settings.full_day = full_day
            user_settings.reminder = reminder

            user_settings.save()

            # redirect to a new URL:
            messages.success(request, "Settings updated")
            return HttpResponseRedirect(reverse('calendar_settings'))
        """

    # If this is a GET (or any other method) create the default form.
    else:
        # Set the default form fields
        form = CalendarShiftCodeForm(
        )

    return render(
        request, 
        "rdrhc_calendar/calendar_shift.html", 
        {'form': form}
    )