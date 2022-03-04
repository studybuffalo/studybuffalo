"""Views for the Substitutions app."""
from bisect import bisect_left
import json
import re

from django.apps import apps
from django.contrib.auth.decorators import permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from dictionary.models import Word, ExcludedWord
from .models import Apps, ModelFields


def binary_search(search_list, word):
    """Completes a binary search to detect if word is present in search list."""
    # Look for match
    i = bisect_left(search_list, word)

    # If match found, return the corresponding object
    if i != len(search_list) and search_list[i] == word:
        return True

    return None


def setup_dictionary():
    """Retrieves all words from dictionary app & returns sorted list"""
    dictionary = set()
    dictionary.update(Word.objects.values_list('word', flat=True))
    dictionary.update(ExcludedWord.objects.values_list('word', flat=True))
    dictionary = list(dictionary)
    dictionary.sort()

    return dictionary


def dictionary_check(dictionary, words):
    """Checks for presence of words within dictionary and manages accordingly."""
    return_text = ''
    start_index = 0

    # Cycle through each individual word
    for word in re.finditer(r'[\w\']+', words):
        # Set word indices
        word_start = word.start()
        word_end = word.end()

        # If needed, add any text before the matched word
        if word_start > start_index:
            return_text = f'{return_text}{words[start_index:word_start]}'

        # Search for the matched word in the dictionary
        regular_search = binary_search(dictionary, word.group())
        lower_case_search = binary_search(
            dictionary,
            f'{word.group()[:1].lower()}{word.group()[1:]}'
        )

        # Check if word was found in either search
        if regular_search or lower_case_search:
            # Word found, can add matched word normally
            return_text = f'{return_text}{words[word_start:word_end]}'
        else:
            # Word not found, mark as missing
            return_text = f'{return_text}<span class="missing">{words[word_start:word_end]}</span>'

        # Reset the start_index for the next loop
        start_index = word_end

    # Add any remaining text from the original string
    return_text = f'{return_text}{words[start_index:]}'

    return return_text


@permission_required('substitutions.can_view', login_url='/accounts/login/')
def dashboard(request):
    """Displays a dashboard of the monitored apps"""
    sub_data = {}

    # Get all the apps
    apps_list = Apps.objects.all()

    # For each app, get the number of substitutions
    for app in apps_list:
        # Get a reference to the monitored pending sub model
        model_pending = apps.get_model(app.app_name, app.model_pending)

        # Get the verbose name (if available) or default name
        try:
            pending_name = model_pending._meta.verbose_name
        except AttributeError:
            pending_name = app.model_pending

        model_data = {
            'id': app.id,
            'pending': pending_name,
            'sub': app.model_sub,
            'count': model_pending.objects.all().count()
        }

        if app.app_name in sub_data:
            sub_data[app.app_name]['data'].append(model_data)
        else:
            # Create a new dictionary entry for this new app
            # Get the App Verbose name (if available)
            try:
                app_name = apps.get_app_config(app.app_name).verbose_name
            except AttributeError:
                app_name = app.app_name

            sub_data[app.app_name] = {
                'app_name': app_name,
                'data': [model_data]
            }

    return render(
        request,
        'substitutions/dashboard.html',
        {
            'sub_data': sub_data
        }
    )


@permission_required('substitutions.can_view', login_url='/accounts/login/')
def review(request, app_id):
    """Generates a page to review pending substitutions"""
    # Get the Apps reference for the provided ID
    app = Apps.objects.get(id=app_id)

    # Assemble required data to pass to template
    app_data = {
        'id': app_id,
        'app_name': app.app_name,
        'pending': app.model_pending,
        'sub': app.model_sub,
    }

    return render(
        request,
        'substitutions/review.html',
        {
            'app_data': app_data,
        }
    )


def retrieve_pending_entries(app_id, last_id, req_num):
    """Utility to collect required pending entries."""
    # Collect the required models
    app = Apps.objects.get(id=app_id)
    orig_fields = ModelFields.objects.filter(
        Q(app_id=app_id) & Q(field_type='o')
    )
    sub_fields = ModelFields.objects.filter(
        Q(app_id=app_id) & Q(field_type='s')
    )

    # Get the monitored application
    model = None

    if app:
        model = apps.get_model(app.app_name, app.model_pending)

    # Get all the entries in the monitored application
    if model and len(orig_fields) and len(sub_fields):
        entries = model.objects.filter(id__gt=int(last_id))[:int(req_num)]

    # Download a copy of the dictionary words to perform a dictionary check
    dictionary = setup_dictionary()

    # Cycle through all the entries and format into dictionary
    response = []

    for entry in entries:
        # Basic details of each entry
        entry_response = {
            'id': getattr(entry, 'id'),
            'orig': [],
            'subs': []
        }

        # Add all the values for the original fields
        for o_field in orig_fields:
            value = getattr(entry, o_field.field_name)

            if o_field.dictionary_check:
                value = dictionary_check(dictionary, value)

            entry_response['orig'].append({
                'field_name': o_field.field_name,
                'value': value,
                'google': o_field.google_check
            })

        # Add all the values for the substitution fields
        for s_field in sub_fields:
            value = getattr(entry, s_field.field_name)

            if s_field.dictionary_check:
                value = dictionary_check(dictionary, value)

            entry_response['subs'].append({
                'field_name': s_field.field_name,
                'value': value,
                'google': s_field.google_check
            })

        response.append(entry_response)

    # Return the final response
    return response


@permission_required('substitutions.can_view', login_url='/accounts/login/')
def retrieve_entries(request):
    """View to request pending entries."""
    response = []

    # Return query data as JSON
    if request.POST:
        # Organize the post variables
        app_id = request.POST.get('app_id', None)
        last_id = request.POST.get('last_id', None)
        request_num = request.POST.get('request_num', None)

        if app_id and last_id and request_num:
            response = retrieve_pending_entries(app_id, last_id, request_num)

    return JsonResponse(response, DjangoJSONEncoder)


def add_new_substitutions(app_id, pend_id, orig, subs):
    """Function to add new substitutions."""
    # Get the model to insert the substitution into
    app = Apps.objects.get(id=app_id)
    model_sub = apps.get_model(app.app_name, app.model_sub)

    # Convert the JSON strings to dictionaries
    orig = json.loads(orig)
    subs = json.loads(subs)

    if model_sub:
        model = model_sub()

        for field in orig:
            setattr(model, field['field_name'], field['field_value'])

        for field in subs:
            setattr(model, field['field_name'], field['field_value'])

        try:
            model.save()

            return {
                'id': pend_id,
                'success': True,
                'message': f'New substitution added ({apps.get_app_config(app.app_name).verbose_name})',
            }
        except ValueError as e:
            return {
                'id': pend_id,
                'success': False,
                'message': f'Unable to save new substitution: {e}'
            }
    else:
        return {
                'id': pend_id,
                'success': False,
                'message': f'Unable to locate model: {app.model_sub}'
            }


@permission_required('substitutions.can_view', login_url='/accounts/login/')
def verify(request):
    """View to add new substitutions."""
    response = {}

    if request.POST:
        app_id = request.POST.get('app_id', None)
        pend_id = request.POST.get('pend_id', None)
        orig = request.POST.get('orig')
        subs = request.POST.get('subs')

        if app_id and pend_id and orig and subs:
            response = add_new_substitutions(app_id, pend_id, orig, subs)
        else:
            # Compile list of the missing arguments
            missing_args = []

            if app_id:
                missing_args.append('application ID')
            if pend_id:
                missing_args.append('pending entry ID')
            if orig:
                missing_args.append('original field data')
            if subs:
                missing_args.append('substitutions field data')

            response = {
                'success': False,
                'message': f'POST request missing arguments: {", ".join(missing_args)}',
            }
    else:
        response = {
            'success': False,
            'message': 'No data received on POST request',
        }

    return JsonResponse(response, DjangoJSONEncoder)


def delete_entry(app_id, pend_id):
    """Function to delete entries."""
    # Get the model to insert the substitution into
    app = Apps.objects.get(id=app_id)
    model_pend = apps.get_model(app.app_name, app.model_pending)

    # Variable to hold the response message
    response = {}

    if model_pend:
        model = model_pend.objects.get(id=pend_id)

        try:
            model.delete()

            response = {
                'id': pend_id,
                'success': True,
                'message': f'Pending entry (id = {pend_id}) successfully deleted',
            }
        except ValueError as e:
            response = {
                'id': pend_id,
                'success': True,
                'message': f'Unable to delete pending entry: {e}'
            }
    else:
        response = {
            'id': pend_id,
            'success': True,
            'message': f'Unable to locate model: {app.model_pend}'
        }

    return response


@permission_required('substitutions.can_view', login_url='/accounts/login/')
def delete_pend(request):
    """View to delete pending entries."""
    response = {}

    if request.POST:
        app_id = request.POST.get('app_id', None)
        pend_id = request.POST.get('pend_id', None)

        if app_id and pend_id:
            response = delete_entry(app_id, pend_id)
        else:
            # Compile list of the missing arguments
            missing_args = []

            if app_id:
                missing_args.append('application ID')
            if pend_id:
                missing_args.append('pending entry ID')

            response = {
               'id': pend_id,
               'success': False,
               'message': f'POST request missing arguments: {", ".join(missing_args)}',
            }
    else:
        response = {
            'id': pend_id,
            'success': False,
            'message': 'No data received on POST request'
        }

    return JsonResponse(response, DjangoJSONEncoder)
