from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
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
    model = LogEntry
    
    permission_required = "log_manager.can_view"
    context_object_name = "log_entries"
    template_name = "log_manager/log_entries.html"

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
