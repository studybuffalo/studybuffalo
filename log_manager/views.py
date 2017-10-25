from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.utils import timezone
from django.views import generic

from .models import AppData, LogEntry
from .forms import AppDataForm

from datetime import datetime, timedelta
import json
import pytz

# Create your views here.
class AppList(PermissionRequiredMixin, generic.ListView):
    model = AppData

    permission_required = "log_manager.can_view"
    context_object_name = "app_list"
    template_name = "log_manager/app_list.html"
    
class AllLogEntries(PermissionRequiredMixin, generic.ListView):
    model = LogEntry
    
    permission_required = "log_manager.can_view"
    context_object_name = "log_entries"
    template_name = "log_manager/log_entries_all.html"


@permission_required("log_manager.can_view", login_url="/accounts/login/")
def log_entries(request):
    # Retrieve list of all the application names
    apps_data = AppData.objects.all()

    # Assemble each app into a dictionary with an ID and name
    app_list = []

    for app in apps_data:
        app_list.append({
            "id": app.id,
            "name": app.name
        })

    # Get datetimes for default time display
    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now()

    return render(
        request, 
        "log_manager/log_entries.html", 
        {
            "applications": app_list,
            "start_date": start_date,
            "end_date": end_date
        }
    )

@permission_required("log_manager.can_view", login_url="/accounts/login/")
def update_entries(request):
    # Return query data as JSON
    if request.GET:
        # Assemble the app name list
        if request.GET["app_names"]:
            app_names_strings = request.GET["app_names"].split(",")

            # Convert the app name codes into integers
            app_names = []

            for app in app_names_strings:
                app_names.append(int(app))
        else:
            app_names = []
        
        
        # Assemble the log level list
        if request.GET["log_levels"]:
            log_levels_string = request.GET["log_levels"].split(",")

            # Conver the log levels into integers
            log_levels = []

            for level in log_levels_string:
                log_levels.append(int(level))
        else:
            log_levels = []

        # Format the datetime values
        if request.GET["start_date"]:
            start_date_string = request.GET["start_date"]

            # Try to format it into a datetime object, otherwise use default
            try:
                start_date_naive = datetime.strptime(
                    start_date_string,
                    "%Y-%m-%d %H:%M:%S"
                )

                start_date = pytz.timezone("UTC").localize(start_date_naive)
            except Exception:
                start_date = timezone.now() - timedelta(months=144)
        else:
            start_date = timezone.now() - timedelta(months=144)

        if request.GET["start_date"]:
            end_date_string = request.GET["end_date"]

            # Try to format it into a datetime object, otherwise use default
            try:
                end_date_naive = datetime.strptime(
                    end_date_string,
                    "%Y-%m-%d %H:%M:%S"
                )

                end_date = pytz.timezone("UTC").localize(end_date_naive)
            except Exception:
                end_date = timezone.now()
        else:
            end_date = timezone.now()
        
    # Create a queryset object that matches all the required criteria
    log_entries = LogEntry.objects.filter(
        app_name__in=app_names
    ).filter(
        level_no__in=log_levels
    ).filter(
        asc_time__gte=start_date
    ).filter(
        asc_time__lte=end_date
    ).order_by(
        "-asc_time"
    )

    # Format the log_entries as a json dictionary
    response = []

    for entry in log_entries:
        response.append({
            "entry_id": entry.id,
            "asc_time": entry.asc_time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "app_name": entry.app_name.name,
            "func_name": entry.func_name,
            "message": entry.message,
            "level_no": entry.level_no
        })

    return HttpResponse(
        json.dumps(response, cls=DjangoJSONEncoder), 
        content_type="application/json"
    )

@permission_required("log_manager.can_view", login_url="/accounts/login/")
def app_add(request):
    # If this is a POST request then process the Form data
    if request.method == "POST":
        app_data = AppData()

        # Create a form instance and populate it with data from the request (binding):
        form = AppDataForm(request.POST, instance=app_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            log_location = form.cleaned_data["log_location"]
            file_name = form.cleaned_data["file_name"]
            monitor_start = form.cleaned_data["monitor_start"]
            asc_time_format = form.cleaned_data["asc_time_format"]
            log_timezone = form.cleaned_data["log_timezone"]
            review_minute = form.cleaned_data["review_minute"]
            review_hour = form.cleaned_data["review_hour"]
            review_day = form.cleaned_data["review_day"]
            review_month = form.cleaned_data["review_month"]
            review_weekday = form.cleaned_data["review_weekday"]
            
            # Upate the user settings
            app_data.name = name
            app_data.log_location = log_location
            app_data.file_name = file_name
            app_data.monitor_start = monitor_start
            app_data.asc_time_format = asc_time_format
            app_data.log_timezone = log_timezone
            app_data.review_minute = review_minute
            app_data.review_hour = review_hour
            app_data.review_day = review_day
            app_data.review_month = review_month
            app_data.review_weekday = review_weekday

            app_data.save()

            # redirect to a new URL:
            messages.success(request, "Application successfully added")
            return HttpResponseRedirect(reverse('app_list'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = AppDataForm(initial={})

    return render(
        request, 
        "log_manager/app_add.html", 
        {'form': form}
    )

@permission_required("log_manager.can_view", login_url="/accounts/login/")
def app_edit(request, id):
    # Get the Shift Code instance for this user
    app_instance = get_object_or_404(AppData, id=id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = AppDataForm(request.POST, instance=app_instance)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            log_location = form.cleaned_data["log_location"]
            file_name = form.cleaned_data["file_name"]
            monitor_start = form.cleaned_data["monitor_start"]
            asc_time_format = form.cleaned_data["asc_time_format"]
            log_timezone = form.cleaned_data["log_timezone"]
            review_minute = form.cleaned_data["review_minute"]
            review_hour = form.cleaned_data["review_hour"]
            review_day = form.cleaned_data["review_day"]
            review_month = form.cleaned_data["review_month"]
            review_weekday = form.cleaned_data["review_weekday"]
            next_review = form.cleaned_data["next_review"]

            # Upate the user settings
            app_instance.name = name
            app_instance.log_location = log_location
            app_instance.file_name = file_name
            app_instance.monitor_start = monitor_start
            app_instance.asc_time_format = asc_time_format
            app_instance.log_timezone = log_timezone
            app_instance.review_minute = review_minute
            app_instance.review_hour = review_hour
            app_instance.review_day = review_day
            app_instance.review_month = review_month
            app_instance.review_weekday = review_weekday
            app_instance.next_review = next_review

            app_instance.save()

            # redirect to a new URL:
            messages.success(request, "Application details updated")
            return HttpResponseRedirect(reverse('app_list'))

    # If this is a GET (or any other method) create the default form
    else:
        # Set the default form values
        name = app_instance.name
        log_location = app_instance.log_location
        file_name = app_instance.file_name
        monitor_start = app_instance.monitor_start
        asc_time_format = app_instance.asc_time_format
        log_timezone = app_instance.log_timezone
        review_minute = app_instance.review_minute
        review_hour = app_instance.review_hour
        review_day = app_instance.review_day
        review_month = app_instance.review_month
        review_weekday = app_instance.review_weekday
        next_review  = app_instance.next_review
        
        form = AppDataForm(initial={
            "name": name,
            "log_location": log_location,
            "file_name": file_name,
            "monitor_start": monitor_start,
            "asc_time_format": asc_time_format,
            "log_timezone": log_timezone,
            "review_minute": review_minute,
            "review_hour": review_hour,
            "review_day": review_day,
            "review_month": review_month,
            "review_weekday": review_weekday,
            "next_review": next_review
        })

    return render(
        request, 
        "log_manager/app_edit.html", 
        {"form": form, "id": id}
    )

@permission_required("log_manager.can_view", login_url="/accounts/login/")
def app_delete(request, id):
     # Get the Shift Code instance for this user
    app_instance = get_object_or_404(AppData, id=id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        app_instance.delete()
       
        # Redirect back to main list
        messages.success(request, "Application deleted")
        return HttpResponseRedirect(reverse('app_list'))
  
    return render(
        request, 
        "log_manager/app_delete.html", 
        {"app": app_instance.name}
    )