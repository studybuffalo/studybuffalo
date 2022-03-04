"""Views for the RDRHC Calendar app."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .forms import CalendarSettingsForm, CalendarShiftCodeForm, MissingCodeForm
from .models import CalendarUser, ShiftCode, MissingShiftCode


@login_required
@permission_required('rdrhc_calendar.can_view', raise_exception=True)
def calendar_index(request):
    """View for the tool page"""
    return render(
        request,
        'rdrhc_calendar/index.html',
        context={},
    )


@login_required
@permission_required('rdrhc_calendar.can_view', raise_exception=True)
def calendar_settings(request):
    """View for a user's calendar settings."""
    user_settings = get_object_or_404(CalendarUser, sb_user=request.user.id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Populate the form
        form = CalendarSettingsForm(request.POST, instance=user_settings)

        # Validate the form
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, 'Settings updated')
            return HttpResponseRedirect(reverse('rdrhc_calendar:settings'))

    # If this is a GET (or any other method) create the default form.
    else:
        # Set the default form fields
        form = CalendarSettingsForm(instance=user_settings)

    return render(
        request,
        'rdrhc_calendar/calendar_settings.html',
        {'form': form}
    )


class ShiftCodeList(PermissionRequiredMixin, generic.ListView):
    """List view for a user's Shift Codes."""
    permission_required = 'rdrhc_calendar.can_view'
    context_object_name = 'shift_code_list'
    template_name = 'rdrhd_calendar/shiftcode_list.html'

    def get_queryset(self):
        # Confirm user has a CalenderUser instance
        if CalendarUser.objects.filter(sb_user=self.request.user).exists():
            return ShiftCode.objects.filter(sb_user=self.request.user)

        raise Http404


@login_required
@permission_required('rdrhc_calendar.can_view', raise_exception=True)
def calendar_code_edit(request, code_id):
    """View to edit a user's shift code."""
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
            messages.success(request, 'Shift code updated')
            return HttpResponseRedirect(reverse('rdrhc_calendar:code_list'))

    # If this is a GET (or any other method) create the default form
    else:
        form = CalendarShiftCodeForm(instance=shift_code_instance)

    return render(
        request,
        'rdrhc_calendar/shiftcode_edit.html',
        {'form': form}
    )


@login_required
@permission_required('rdrhc_calendar.can_view', raise_exception=True)
def calendar_code_add(request):
    """View to add a calendar shift code for a user."""
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
            messages.success(request, 'Shift code added')
            return HttpResponseRedirect(reverse('rdrhc_calendar:code_list'))
    else:
        form = CalendarShiftCodeForm()

    return render(
        request,
        'rdrhc_calendar/shiftcode_add.html',
        {'form': form}
    )


@login_required
@permission_required('rdrhc_calendar.can_view', raise_exception=True)
def calendar_code_delete(request, code_id):
    """View to delete a user's calendar code."""
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(
        ShiftCode,
        id=code_id,
        sb_user=request.user
    )

    if request.method == 'POST':
        shift_code_instance.delete()

        # Redirect back to main list
        messages.warning(request, 'Shift code deleted')
        return HttpResponseRedirect(reverse('rdrhc_calendar:code_list'))

    return render(
        request,
        'rdrhc_calendar/shiftcode_delete.html',
        {'shift_code': shift_code_instance.code}
    )


class MissingShiftCodeList(PermissionRequiredMixin, generic.ListView):
    """List view for missing shift codes."""
    permission_required = 'rdrhc_calendar.can_add_default_codes'
    context_object_name = 'shift_code_list'
    template_name = 'missingshiftcode_list.html'

    def get_queryset(self):
        return MissingShiftCode.objects.all()


@login_required
@permission_required('rdrhc_calendar.can_add_default_codes', raise_exception=True)
def missing_code_edit(request, code_id):
    """View to edit a missing shift code for a user."""
    # Get the Shift Code instance for this user
    missing_code_instance = get_object_or_404(MissingShiftCode, id=code_id)

    if request.method == 'POST':
        form = MissingCodeForm(request.POST)

        if form.is_valid():
            shift_code = form.save(commit=False)
            shift_code.code = missing_code_instance.code
            shift_code.role = missing_code_instance.role

            try:
                shift_code.save()

                # If save successful, delete this MissingShiftCode
                missing_code_instance.delete()

                # redirect to a new URL
                messages.success(request, 'Shift code added')
                return HttpResponseRedirect(reverse('rdrhc_calendar:missing_code_list'))
            except IntegrityError:
                messages.error(request, 'Shift code already exists for role.')

    else:
        form = MissingCodeForm()

    return render(
        request,
        'rdrhc_calendar/missingshiftcode_edit.html',
        {
            'form': form,
            'shift_code': missing_code_instance.code,
            'role': missing_code_instance.role,
        }
    )


@login_required
@permission_required('rdrhc_calendar.can_add_default_codes', raise_exception=True)
def missing_code_delete(request, code_id):
    """View to delete a missing shift code for a user."""
    # Get the Shift Code instance for this user
    shift_code_instance = get_object_or_404(MissingShiftCode, id=code_id)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        shift_code_instance.delete()

        # Redirect back to main list
        messages.warning(request, 'Shift code deleted')
        return HttpResponseRedirect(reverse('rdrhc_calendar:missing_code_list'))

    return render(
        request,
        'rdrhc_calendar/missingshiftcode_delete.html',
        {'shift_code': shift_code_instance.code}
    )
