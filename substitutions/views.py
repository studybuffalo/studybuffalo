from django.apps import apps
from django.shortcuts import render

from .models import Apps, ModelFields

def dashboard(request):
    """Displays a dashboard of the monitored apps"""
    sub_data = {}

    # Get all the apps
    apps_list = Apps.objects.all()

    # For each app, get the number of substitutions
    for app in apps_list:
        model_pending = apps.get_model(app.app_name, app.model_pending)
        
        model_data = {
            "id": app.id,
            "pending": app.model_pending,
            "sub": app.model_sub,
            "count": model_pending.objects.all().count()
        }

        if app.app_name in sub_data:
            sub_data[app.app_name].append(model_data)
        else:
            sub_data[app.app_name] = [model_data]
        
    print(sub_data)
    return render(
        request,
        "substitutions/dashboard.html",
        {
            "sub_data": sub_data
        }
    )