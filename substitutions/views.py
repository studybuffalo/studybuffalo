from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.shortcuts import render, HttpResponse

from .models import Apps, ModelFields

import json

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

def review(request, id):
    """Generates a page to review pending substitutions"""
    # Get the Apps reference for the provided ID
    app = Apps.objects.get(id=id)

    # Assemble required data to pass to template
    app_data = {
        "id": id,
        "app_name": app.app_name,
        "pending": app.model_pending,
        "sub": app.model_sub,
    }

    return render(
        request,
        "substitutions/review.html",
        {
            "app_data": app_data,
        }
    )

def retrieve_pending_entries(app_id, last_id, req_num):
    # Get the Substitution App reference and the fields
    app = Apps.objects.get(id=app_id)
    original_fields = ModelFields.objects.filter(
        Q(app_id=app_id) & Q(field_type="o")
    )
    sub_fields = ModelFields.objects.filter(
        Q(app_id=app_id) & Q(field_type="s")
    )
    # Get the monitored application and the required response
    model = None

    if app:
        model = apps.get_model(app.app_name, app.model_pending)

    if model and len(fields):
        print("test")
        entries = model.objects.filter(id__gt=int(last_id))[:int(req_num)]

    response = []

    for entry in entries:
        entry_response = {
            "orig": [],
            "subs": []
        }

        for o_field in original_fields:
            entry_response["orig"].append({
                field.field_name: getattr(entry, o_field.field_name),
                "dictionary": o_field.dictionary_check,
                "google": o_field.google_check
            })
        for s_field in sub_fields:
            entry_response["orig"].append({
                field.field_name: getattr(entry, o_field.field_name),
                "dictionary": o_field.dictionary_check,
                "google": o_field.google_check
            })

        response.append(entry_response)

    return response

def retrieve_entries(request):
    response = []

    # Return query data as JSON
    if request.GET:
        # Organize the post variables
        app_id = request.GET["app_id"] if request.GET["app_id"] else None
        last_id = request.GET["last_id"] if request.GET["last_id"] else 0
        request_num = (
            request.GET["request_num"] if request.GET["request_num"] else None
        )

        if app_id and last_id and request_num:
            response = retrieve_pending_entries(app_id, last_id, request_num)

    return HttpResponse(
        json.dumps(response, cls=DjangoJSONEncoder), 
        content_type="application/json",
    )