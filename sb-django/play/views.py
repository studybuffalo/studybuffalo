from django.shortcuts import render

def index(request):
    """The study buffalo home page"""

    return render(
        request,
        "play/index.html",
        context={}
    )