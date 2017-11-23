from django.apps import apps
from django.contrib.auth.decorators import permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, HttpResponse

from .models import WordPending, Word, ExcludedWord, Language, DictionaryType

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
    pending_count = WordPending.objects.all().count()

    return render(
        request,
        "dictionary/review.html",
        {"count": pending_count,},
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
            "dictionary_type": entry.dictionary_type.id,
            "language": entry.language.id,
        })

    # Return the final response
    return response

@permission_required("dictionary.can_view", login_url="/accounts/login/")
def add_new_word(request):
    response = {}

    if request.POST:
        pending_id = request.POST.get("pending_id", None)
        model_name = request.POST.get("model_name")
        word = request.POST.get("word")
        language = request.POST.get("language")
        dictionary_type = request.POST.get("dictionary_type")

        if pending_id and model_name and word and language and dictionary_type:
            response = process_new_word(
                model_name, word, language, dictionary_type
            )

            response["id"] = pending_id
        else:
            # Compile list of the missing arguments
            missing_args = []

            None if pending_id else missing_args.append("pending ID")
            None if model_name else missing_args.append("model name")
            None if word else missing_args.append("sord")
            None if language else missing_args.append("language")
            None if dictionary_type else missing_args.append("dictionary_type")
            
            response = {
                "success": False,
                "message": "POST request missing arguments: {}".format(
                    ", ".join(missing_args)
                )
            }
    else:
        response = {
            "success": False,
            "message": "No data received on POST request",
        }

    return HttpResponse(
        json.dumps(response, cls=DjangoJSONEncoder), 
        content_type="application/json",
    )

def process_new_word(model_name, word, language, dictionary_type):
    # Get the proper model reference
    model_reference = Word if model_name == "word" else ExcludedWord

    new_word = model_reference(
        language=Language.objects.get(id=language),
        dictionary_type=DictionaryType.objects.get(id=dictionary_type),
        word=word,
    )
    
    model_message = ""

    if model_name == "word":
        model_message = "Word dictionary"
    else:
        model_message = "Excluded Word dictionary"

    try:
        new_word.save()

        message = "{} added to the {}".format(word, model_message)
        
        return {
            "success":True,
            "message": message,
        }
    except Exception as e:
        message = "Unable to save {} to the {}: {}".format(
            word, model_message, e
        )
        return {
            "success": False,
            "message": message
        }

@permission_required("dictionary.can_view", login_url="/accounts/login/")
def delete_pending_word(request):
    response = {}

    if request.POST:
        pending_id = request.POST.get("pending_id", None)

        if pending_id:
            response = process_pending_word_deletion(pending_id)
        else:
            response = {
               "success": False,
               "message": "POST request missing pending ID",
            }
    else:
        response = {
            "success": False,
            "message": "No data received on POST request"
        }

    return HttpResponse(
        json.dumps(response, cls=DjangoJSONEncoder), 
        content_type="application/json",
    )

def process_pending_word_deletion(pending_id):
    pending_word = WordPending.objects.get(id=pending_id)
       
    try:
        pending_word.delete()

        return {
            "id": pending_id,
            "success": True,
            "message": (
                "Pending word (id = {}) successfully "
                "deleted".format(pending_id)
            )
        }
    except Exception as e:
        log.warn("Error deleting pending word", exc_info=True)

        return {
            "id": pending_id,
            "success": True,
            "message": "Unable to delete pending word (id = {}): {}".format(
                pending_id, e
            )
        }