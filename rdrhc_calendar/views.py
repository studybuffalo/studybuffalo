from django.shortcuts import render

def calendar_index(request):
    """View for the tool page"""
    return render(
        request,
        "rdrhc_calendar/index.html",
        context={},
    )