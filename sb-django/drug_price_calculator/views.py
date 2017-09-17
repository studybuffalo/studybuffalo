from django.shortcuts import render
from django.views import generic
from .models import (ATC, Coverage, ExtraInformation, Price, PTC, 
                     SpecialAuthorization, ATCDescriptions, SubsBSRF, 
                     SubsGeneric, SubsManufacturer, SubsPTC, SubsUnit)

def index(request):
    """View for the main drug price calculator page"""
    return render(
        request,
        "drug_price_calculator/index.html",
        context={},
    )


class ATCList(generic.ListView):
    model = ATC

    context_object_name = "atc_list"

class CoverageList(generic.ListView):
    model = Coverage

    context_object_name = "coverage_list"

class ExtraInformationList(generic.ListView):
    model = ExtraInformation

    context_object_name = "extra_information_list"

class PriceList(generic.ListView):
    model = Price

    context_object_name = "price_list"

class PTCList(generic.ListView):
    model = PTC

    context_object_name = "ptc_list"

class SpecialAuthorizationList(generic.ListView):
    model = SpecialAuthorization

    context_object_name = "special_authorization_list"

class SubsATCList(generic.ListView):
    model = ATCDescriptions

    context_object_name = "subs_atc_list"

class SubsBSRFList(generic.ListView):
    model = SubsBSRF

    context_object_name = "subs_bsrf_list"

class SubsGenericList(generic.ListView):
    model = SubsGeneric

    context_object_name = "subs_generic_list"

class SubsManufacturerList(generic.ListView):
    model = SubsManufacturer

    context_object_name = "subs_manufacturer_list"

class SubsPTCList(generic.ListView):
    model = SubsPTC
    
    context_object_name = "subs_ptc_list"

class SubsUnitList(generic.ListView):
    model = SubsUnit

    context_object_name = "subs_unit_list"


from django.http import HttpResponse
import json

def live_search(request):
    print("test")
    if request.GET:
        get_value = request.body
        data = {"result": "test",}
        return HttpResponse(json.dumps(data), content_type="application/json")