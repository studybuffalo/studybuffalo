from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CalendarSettingsForm, CalendarShiftCodeForm, MissingCodeForm
from .models import CalendarUser, ShiftCode, MissingShiftCode

@login_required
@permission_required("rdrhc_calendar.can_view", raise_exception=True)
def calendar_index(request):
    """View for the tool page"""
    return render(
        request,
        "rdrhc_calendar/index.html",
        context={},
    )

@login_required
@permission_required("rdrhc_calendar.can_view", raise_exception=True)
def calendar_settings(request):
    user_settings = get_object_or_404(CalendarUser, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Populate the form
        form = CalendarSettingsForm(request.POST, instance=user_settings)

        # Validate the form
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Settings updated")
            return HttpResponseRedirect(reverse('rdrhc_calendar:settings'))

    # If this is a GET (or any other method) create the default form.
    else:
        # Set the default form fields
        form = CalendarSettingsForm(instance=user_settings)

    return render(
        request,
        "rdrhc_calendar/calendar_settings.html",
        {'form': form}
    )

class ShiftCodeList(PermissionRequiredMixin, generic.ListView):
    permission_required = "rdrhc_calendar.can_view"
    context_object_name = "shift_code_list"
    template_name = "rdrhd_calendar/shiftcode_list.html"

    def get_queryset(self):
        # Confirm user has a CalenderUser instance
        if CalendarUser.objects.filter(sb_user=self.request.user).exists():
            return ShiftCode.objects.filter(sb_user=self.request.user)

        raise Http404

@login_required
@permission_required("rdrhc_calendar.can_view", raise_exception=True)
def calendar_code_edit(request, code_id):
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(
        ShiftCode,
        id=code_id,
        sb_user=request.user.id
    )

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create the form
        form = CalendarShiftCodeForm(request.POST, instance=shift_code_instance)

        # Check if the form is valid:
        if form.is_valid():
            shift_code_instance.save()

            # redirect to a new URL:
            messages.success(request, "Shift code updated")
            return HttpResponseRedirect(reverse('rdrhc_calendar:code_list'))

    # If this is a GET (or any other method) create the default form
    else:
        form = CalendarShiftCodeForm(instance=shift_code_instance)

    return render(
        request,
        "rdrhc_calendar/shiftcode_edit.html",
        {'form': form}
    )

@login_required
@permission_required("rdrhc_calendar.can_view", raise_exception=True)
def calendar_code_add(request):
    # Collect the user data
    sb_user = request.user
    calendar_user = get_object_or_404(CalendarUser, sb_user=sb_user)

    if request.method == 'POST':
        # Populate form
        form = CalendarShiftCodeForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Save partial form and add required fields
            shift_code = form.save(commit=False)
            shift_code.sb_user = sb_user
            shift_code.role = calendar_user.role
            shift_code.save()

            # redirect to a new URL:
            messages.success(request, "Shift code added")
            return HttpResponseRedirect(reverse("rdrhc_calendar:code_list"))
    else:
        form = CalendarShiftCodeForm()

    return render(
        request,
        "rdrhc_calendar/shiftcode_add.html",
        {'form': form}
    )

@login_required
@permission_required("rdrhc_calendar.can_view", raise_exception=True)
def calendar_code_delete(request, code):
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(ShiftCode, code=code, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        shift_code_instance.delete()

        # Redirect back to main list
        messages.warning(request, "Shift code deleted")
        return HttpResponseRedirect(reverse('rdrhc_calendar:code_list'))

    return render(
        request,
        "rdrhc_calendar/shiftcode_delete.html",
        {"shift_code": code}
    )

class MissingShiftCodeList(PermissionRequiredMixin, generic.ListView):
    permission_required = "rdrhc_calendar.can_add_default_codes"
    context_object_name = "shift_code_list"
    template_name = "missingshiftcode_list.html"

    def get_queryset(self):
        return MissingShiftCode.objects.all()

@login_required
@permission_required("rdrhc_calendar.can_add_default_codes", raise_exception=True)
def missing_code_add(request, code_id):
    # Get the Shift Code instance for this user
    missing_code_instance = get_object_or_404(MissingShiftCode, id=id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = MissingCodeForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
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
            shift_code = missing_code_instance.code
            role = missing_code_instance.role

            if ShiftCode.objects.filter(sb_user=None, role=role, code=shift_code):
                messages.error(request, "This shift code already exists")
            else:
                # Add the new default code
                new_code = ShiftCode(
                    code=shift_code,
                    role=role,
                    monday_start=monday_start,
                    monday_duration=monday_duration,
                    tuesday_start=tuesday_start,
                    tuesday_duration=tuesday_duration,
                    wednesday_start=wednesday_start,
                    wednesday_duration=wednesday_duration,
                    thursday_start=thursday_start,
                    thursday_duration=thursday_duration,
                    friday_start=friday_start,
                    friday_duration=friday_duration,
                    saturday_start=saturday_start,
                    saturday_duration=saturday_duration,
                    sunday_start=sunday_start,
                    sunday_duration=sunday_duration,
                    stat_start=stat_start,
                    stat_duration=stat_duration
                )

                new_code.save()

                # If save succeed, delete this MissingShiftCode
                missing_code_instance.delete()

                # redirect to a new URL
                messages.success(request, "Shift code added")
                return HttpResponseRedirect(reverse('calendar_missing_code_list'))

    # If this is a GET (or any other method) create the default form
    else:
        # Create form that populates with default values
        form = MissingCodeForm(initial={})

    return render(
        request,
        "rdrhc_calendar/missingshiftcode_add.html",
        {
            "form": form,
            "shift_code": missing_code_instance.code,
            "role": missing_code_instance.role,
        }
    )

@login_required
@permission_required("rdrhc_calendar.can_add_default_codes", raise_exception=True)
def missing_code_delete(request, codeid):
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(MissingShiftCode, id=id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        shift_code_instance.delete()

        # Redirect back to main list
        messages.warning(request, "Shift code deleted")
        return HttpResponseRedirect(reverse('calendar_missing_code_list'))

    return render(
        request,
        "rdrhc_calendar/missingshiftcode_delete.html",
        {"shift_code": shift_code_instance.code}
    )
