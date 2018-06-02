from django.shortcuts import render

def index(request):
    return render(
        request,
        "flash_cards/index.html",
        context={},
    )
