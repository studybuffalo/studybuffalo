from django.apps import apps
from django.contrib.auth.decorators import permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, HttpResponse

from .models import WordPending

import json

def get_application_name(application_name):
    """Returns a verbose name for the application, if available"""
    try:
        return apps.get_app_config(application_name).verbose_name
    except Exception:
        # Unable to get a name, just return the application_name
        return object_name

def get_model_name(application_name, model_name):
    """Returns a verbose name for the model, if available"""
    try:
        return apps.get_model(application_name, model_name)._meta.verbose_name
    except AttributeError:
        # No verbose name, try to get the str name
        return str(apps.get_model(application_name, model_name))
    except Exception:
        # Unable to get a name, just return the provided model_name
        return model_name

def index(request):
    """Displays a page for users to download dictionaries"""
    return render(
        request,
        "dictionary/index.html",
        {},
    )

@permission_required("dictionary.can_view", login_url="/accounts/login/")
def review(request):
    """Displays a dashboard of the pending Word entries"""
    return render(
        request,
        "dictionary/review.html",
        {},
    )

@permission_required("dictionary.can_view", login_url="/accounts/login/")
def retrieve_entries(request):
    response = []

    # Return query data as JSON
    if request.POST:
        # Organize the post variables
        last_id = request.POST.get("last_id", None)
        request_num = request.POST.get("request_num", None)

        if last_id and request_num:
            response = retrieve_pending_entries(last_id, request_num)

    return HttpResponse(
        json.dumps(response, cls=DjangoJSONEncoder), 
        content_type="application/json",
    )

def retrieve_pending_entries(last_id, req_num):
    # Get the requested entries
    entries = WordPending.objects.filter(id__gt=int(last_id))[:int(req_num)]

    # Cycle through all the entries and format into dictionary
    response = []

    for entry in entries:
        # Basic details of each entry
        response.append({
            "id": getattr(entry, "id"),
            "word": entry.word,
            "type": entry.dictionary_type.id,
            "language": entry.language.id,
        })

    # Return the final response
    return response