"""Views for the Dictionary app."""
from django.contrib.auth.decorators import permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    WordPending, Word, ExcludedWord, Language, DictionaryType, DictionaryClass
)


def index(request):
    """Displays a page for users to download dictionaries"""
    return render(
        request,
        'dictionary/index.html',
        {},
    )


@permission_required('dictionary.can_view', login_url='/accounts/login/')
def retrieve_select_data(request):
    """Returns data to generate the HTML select elements."""
    response = generate_select_data()

    return JsonResponse(response, DjangoJSONEncoder)


def generate_select_data():
    """Generates html select inputs for the review page."""
    selects = {
        'language': '',
        'dict_type': '',
        'dict_class': '',
    }

    # Generate the Language select
    languages = Language.objects.all()
    language_options = []

    for language in languages:
        language_options.append(
            f'<option value="{language.id}">{language.language}</option>'
        )

    selects['language'] = f'<select class="language">language_options{"".join(language_options)}</select>'

    # Generate the Dictionary Type Select
    dict_types = DictionaryType.objects.all()
    dict_type_options = []

    for dict_type in dict_types:
        dict_type_options.append(
            f'<option value="{dict_type.id}">{dict_type.dictionary_name}</option>'
        )

    selects['dict_type'] = (
        f'<select class="dictionary-type">{"".join(dict_type_options)}</select>'
    )

    # Generate the Dictionary Class Select
    dict_classes = DictionaryClass.objects.all()
    dict_class_options = []

    for dict_class in dict_classes:
        dict_class_options.append(
            f'<option value="{dict_class.id}">{dict_class.class_name}</option>'
        )

    selects['dict_class'] = (
        f'<select class="dictionary-class">{"".join(dict_class_options)}</select>'
    )

    return selects


@permission_required('dictionary.can_view', login_url='/accounts/login/')
def review(request):
    """Displays a dashboard of the pending Word entries"""
    pending_count = WordPending.objects.all().count()

    return render(
        request,
        'dictionary/review.html',
        {'count': pending_count},
    )


@permission_required('dictionary.can_view', login_url='/accounts/login/')
def retrieve_entries(request):
    """Retrieves requested dictionary entries."""
    response = []

    # Return query data as JSON
    if request.POST:
        # Organize the post variables
        last_id = request.POST.get('last_id', None)
        request_num = request.POST.get('request_num', None)

        if last_id and request_num:
            response = retrieve_pending_entries(last_id, request_num)

    return JsonResponse(response, DjangoJSONEncoder)


def retrieve_pending_entries(last_id, req_num):
    """Retrieves requested pending dicionary entries."""
    # Get the requested entries
    entries = WordPending.objects.filter(id__gt=int(last_id))[:int(req_num)]

    # Cycle through all the entries and format into dictionary
    response = []

    for entry in entries:
        # Basic details of each entry
        response.append({
            'id': getattr(entry, 'id'),
            'word': entry.word,
            'original': entry.original_words,
            'language': entry.language.id,
            'dictionary_type': entry.dictionary_type.id,
            'dictionary_class': entry.dictionary_class.id,
        })

    # Return the final response
    return response


@permission_required('dictionary.can_view', login_url='/accounts/login/')
def add_new_word(request):
    """View to add new word to dictionary."""
    response = {}

    if request.POST:
        pending_id = request.POST.get('pending_id', None)
        model_name = request.POST.get('model_name')
        word = request.POST.get('word')
        language = request.POST.get('language')
        dictionary_type = request.POST.get('dictionary_type')
        dictionary_class = request.POST.get('dictionary_class')

        if all([pending_id, model_name, word, language, dictionary_type, dictionary_class]):
            # Add the new word and get a response base
            response = process_new_word(
                model_name, word, language, dictionary_type, dictionary_class
            )

            response['id'] = pending_id
        else:
            # Compile list of the missing arguments
            missing_args = []

            if pending_id is None:
                missing_args.append('pending ID')

            if model_name is None:
                missing_args.append('model name')

            if word is None:
                missing_args.append('word')

            if language is None:
                missing_args.append('language')

            if dictionary_type is None:
                missing_args.append('dictionary_type')

            if dictionary_class is None:
                missing_args.append('dictionary_class')

            response = {
                'success': False,
                'message': f'POST request missing arguments: {", ".join(missing_args)}'
            }
    else:
        response = {
            'success': False,
            'message': 'No data received on POST request',
        }

    return JsonResponse(response, DjangoJSONEncoder)


def process_new_word(model_name, word, language, dictionary_type, dictionary_class):
    """View to process a new word for the dictionary."""
    # Get the proper model reference
    model_reference = Word if model_name == 'word' else ExcludedWord

    new_word = model_reference(
        language=Language.objects.get(id=language),
        dictionary_type=DictionaryType.objects.get(id=dictionary_type),
        dictionary_class=DictionaryClass.objects.get(id=dictionary_class),
        word=word,
    )

    model_message = ''

    if model_name == 'word':
        model_message = 'Word dictionary'
    else:
        model_message = 'Excluded Word dictionary'

    new_word.save()

    message = f'{word} added to the {model_message}'

    return {
        'success': True,
        'message': message,
    }


def process_pending_word_deletion(pending_id):
    """View to delete pending word."""
    pending_word = WordPending.objects.get(id=pending_id)
    pending_word.delete()

    return {
        'id': pending_id,
        'success': True,
        'message': (
            f'Pending word (id = {pending_id}) successfully deleted'
        )
    }


@permission_required('dictionary.can_view', login_url='/accounts/login/')
def delete_pending_word(request):
    """View to delte a pending word."""
    response = {}

    if request.POST:
        pending_id = request.POST.get('pending_id', None)

        if pending_id:
            response = process_pending_word_deletion(pending_id)
        else:
            response = {
                'success': False,
                'message': 'POST request missing pending ID',
            }
    else:
        response = {
            'success': False,
            'message': 'No data received on POST request'
        }

    return JsonResponse(response, DjangoJSONEncoder)
