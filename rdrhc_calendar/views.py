from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
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

class ShiftCodeList(PermissionRequiredMixin, generic.ListView):
    permission_required = "rdrhc_calendar.can_view"
    context_object_name = "shift_code_list"
    template_name = "shiftcode_list.html"

    def get_queryset(self):
        return ShiftCode.objects.filter(sb_user=self.request.user)

@permission_required("rdrhc_calendar.can_view", login_url="/accounts/login/")
def calendar_code_edit(request, code):
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(ShiftCode, code=code, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CalendarShiftCodeForm(request.POST, instance=shift_code_instance)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            shift_code = form.cleaned_data["code"]
            monday_start = form.cleaned_data["monday_start"]
            monday_duration = form.cleaned_data["monday_duration"]
            tuesday_start = form.cleaned_data["tuesday_start"]
            tuesday_duration = form.cleaned_data["tuesday_duration"]
            wednesday_start = form.cleaned_data["wednesday_start"]
            wednesday_duration = form.cleaned_data["wednesday_duration"]
            thursday_start = form.cleaned_data["thursday_start"]
            thursday_duration = form.cleaned_data["thursday_duration"]
            friday_start = form.cleaned_data["friday_start"]
            friday_duration = form.cleaned_data["friday_duration"]
            saturday_start = form.cleaned_data["saturday_start"]
            saturday_duration = form.cleaned_data["saturday_duration"]
            sunday_start = form.cleaned_data["sunday_start"]
            sunday_duration = form.cleaned_data["sunday_duration"]
            stat_start = form.cleaned_data["stat_start"]
            stat_duration = form.cleaned_data["stat_duration"]

            # Check if this is a unique entry
            sb_user = request.user.id
            role = shift_code_instance.role

            if ShiftCode.objects.filter(sb_user=sb_user, role=role, code=shift_code):
                messages.error(request, "This shift code already exists")
            else:
                # Upate the user settings
                shift_code_instance.code = shift_code
                shift_code_instance.monday_start = monday_start
                shift_code_instance.monday_duration = monday_duration
                shift_code_instance.tuesday_start = tuesday_start
                shift_code_instance.tuesday_duration = tuesday_duration
                shift_code_instance.wednesday_start = wednesday_start
                shift_code_instance.wednesday_duration = wednesday_duration
                shift_code_instance.thursday_start = thursday_start
                shift_code_instance.thursday_duration = thursday_duration
                shift_code_instance.friday_start = friday_start
                shift_code_instance.friday_duration = friday_duration
                shift_code_instance.saturday_start = saturday_start
                shift_code_instance.saturday_duration = saturday_duration
                shift_code_instance.sunday_start = sunday_start
                shift_code_instance.sunday_duration = sunday_duration
                shift_code_instance.stat_start = stat_start
                shift_code_instance.stat_duration = stat_duration

                shift_code_instance.save()

                # redirect to a new URL:
                messages.success(request, "Shift code updated")
                return HttpResponseRedirect(reverse('calendar_code_list'))

    # If this is a GET (or any other method) create the default form
    else:
        # Set the default form values
        shift_code = shift_code_instance.code
        monday_start = shift_code_instance.monday_start
        monday_duration = shift_code_instance.monday_duration
        tuesday_start = shift_code_instance.tuesday_start
        tuesday_duration = shift_code_instance.tuesday_duration
        wednesday_start = shift_code_instance.wednesday_start
        wednesday_duration = shift_code_instance.wednesday_duration
        thursday_start = shift_code_instance.thursday_start
        thursday_duration = shift_code_instance.thursday_duration
        friday_start = shift_code_instance.friday_start
        friday_duration = shift_code_instance.friday_duration
        saturday_start = shift_code_instance.saturday_start
        saturday_duration = shift_code_instance.saturday_duration
        sunday_start = shift_code_instance.sunday_start
        sunday_duration = shift_code_instance.sunday_duration
        stat_start = shift_code_instance.stat_start
        stat_duration = shift_code_instance.stat_duration
        
        form = CalendarShiftCodeForm(initial={
            "code": shift_code,
            "monday_start": monday_start,
            "monday_duration": monday_duration,
            "tuesday_start": tuesday_start,
            "tuesday_duration": tuesday_duration,
            "wednesday_start": wednesday_start,
            "wednesday_duration": wednesday_duration,
            "thursday_start": thursday_start,
            "thursday_duration": thursday_duration,
            "friday_start": friday_start,
            "friday_duration": friday_duration,
            "saturday_start": saturday_start,
            "saturday_duration": saturday_duration,
            "sunday_start": sunday_start,
            "sunday_duration": sunday_duration,
            "stat_start": stat_start,
            "stat_duration": stat_duration,
        })

    return render(
        request, 
        "rdrhc_calendar/shiftcode_edit.html", 
        {'form': form}
    )

@permission_required("rdrhc_calendar.can_view", login_url="/accounts/login/")
def calendar_code_add(request):
    if request.method == 'POST':
        shift_code_instance = ShiftCode()

        # Create a form instance and populate it with data from the request (binding):
        form = CalendarShiftCodeForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the user data
            sb_user = request.user
            role = CalendarUser.objects.filter(
                sb_user=sb_user).values_list("role", flat=True)[0]

            # Collect the form fields
            shift_code = form.cleaned_data["code"]
            monday_start = form.cleaned_data["monday_start"]
            monday_duration = form.cleaned_data["monday_duration"]
            tuesday_start = form.cleaned_data["tuesday_start"]
            tuesday_duration = form.cleaned_data["tuesday_duration"]
            wednesday_start = form.cleaned_data["wednesday_start"]
            wednesday_duration = form.cleaned_data["wednesday_duration"]
            thursday_start = form.cleaned_data["thursday_start"]
            thursday_duration = form.cleaned_data["thursday_duration"]
            friday_start = form.cleaned_data["friday_start"]
            friday_duration = form.cleaned_data["friday_duration"]
            saturday_start = form.cleaned_data["saturday_start"]
            saturday_duration = form.cleaned_data["saturday_duration"]
            sunday_start = form.cleaned_data["sunday_start"]
            sunday_duration = form.cleaned_data["sunday_duration"]
            stat_start = form.cleaned_data["stat_start"]
            stat_duration = form.cleaned_data["stat_duration"]
            
            # Check if this is a unique entry
            if ShiftCode.objects.filter(sb_user=sb_user, role=role, code=shift_code):
                messages.error(request, "This shift code already exists")
            else:
                # Upate the user settings
                shift_code_instance.sb_user = sb_user
                shift_code_instance.role = role
                shift_code_instance.code = shift_code
                shift_code_instance.monday_start = monday_start
                shift_code_instance.monday_duration = monday_duration
                shift_code_instance.tuesday_start = tuesday_start
                shift_code_instance.tuesday_duration = tuesday_duration
                shift_code_instance.wednesday_start = wednesday_start
                shift_code_instance.wednesday_duration = wednesday_duration
                shift_code_instance.thursday_start = thursday_start
                shift_code_instance.thursday_duration = thursday_duration
                shift_code_instance.friday_start = friday_start
                shift_code_instance.friday_duration = friday_duration
                shift_code_instance.saturday_start = saturday_start
                shift_code_instance.saturday_duration = saturday_duration
                shift_code_instance.sunday_start = sunday_start
                shift_code_instance.sunday_duration = sunday_duration
                shift_code_instance.stat_start = stat_start
                shift_code_instance.stat_duration = stat_duration

                shift_code_instance.save()

                # redirect to a new URL:
                messages.success(request, "Shift code added")
                return HttpResponseRedirect(reverse("calendar_code_list"))

    else:
        form = CalendarShiftCodeForm()

    return render(
        request, 
        "rdrhc_calendar/shiftcode_add.html", 
        {'form': form}
    )

@permission_required("rdrhc_calendar.can_view", login_url="/accounts/login/")
def calendar_code_delete(request, code):
     # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(ShiftCode, code=code, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        shift_code_instance.delete()
       
        # Redirect back to main list
        messages.warning(request, "Shift code deleted")
        return HttpResponseRedirect(reverse('calendar_code_list'))
  
    return render(
        request, 
        "rdrhc_calendar/shiftcode_delete.html", 
        {"shift_code": code}
    )