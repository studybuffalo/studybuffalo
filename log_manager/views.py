from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic

from .models import AppData, LogEntry
from .forms import AppDataForm

# Create your views here.
class AppList(PermissionRequiredMixin, generic.ListView):
    model = AppData

    permission_required = "log_manager.can_view"
    context_object_name = "app_list"
    template_name = "log_manager/app_list.html"

class LogEntries(PermissionRequiredMixin, generic.ListView):
    permission_required = "log_manager.can_view"
    context_object_name = "log_entries"
    template_name = "log_manager/log_entries.html"
    paginate_by = 200

    def get_queryset(self):
        queryset = LogEntry.objects.filter(level_no__gte=30).order_by("-asc_time")

        return queryset

@permission_required("log_manager.can_view", login_url="/accounts/login/")
def update_entries(request):
    # Return query data as JSON
    if request.method == "GET":
        entries = LogEntry.object.all()

    response = [{"things": "otherthings"}]
 
    return HttpResponse(response, content_type="text/html")
@permission_required("log_manager.can_view", login_url="/accounts/login/")
def app_add(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        app_data = AppData()

        # Create a form instance and populate it with data from the request (binding):
        form = AppDataForm(request.POST, instance=app_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            log_location = form.cleaned_data["log_location"]
            file_name = form.cleaned_data["file_name"]
            flag_start = form.cleaned_data["flag_start"]
            flag_end = form.cleaned_data["flag_end"]
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
            app_data.flag_start = flag_start
            app_data.flag_end = flag_end
            app_instance.asc_time_format = asc_time_format
            app_instance.log_timezone = log_timezone
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
            flag_start = form.cleaned_data["flag_start"]
            flag_end = form.cleaned_data["flag_end"]
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
            app_instance.flag_start = flag_start
            app_instance.flag_end = flag_end
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
        flag_start = app_instance.flag_start
        flag_end = app_instance.flag_end
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
            "flag_start": flag_start,
            "flag_end": flag_end,
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