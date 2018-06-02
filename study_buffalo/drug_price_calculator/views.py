import json

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.db.models import Q

from django.core.serializers.json import DjangoJSONEncoder
from .models import (
    ATC, Coverage, ExtraInformation, Price, PTC, SpecialAuthorization,
    ATCDescriptions, SubsBSRF, SubsGeneric, SubsManufacturer, SubsPTC,
    SubsUnit
)

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



def live_search(request):
    """Handles AJAX request to display drug name search results"""
    response = ""

    # If there is a GET request, search for results
    if request.GET:
        # Get the search value
        search_value = request.GET["q"]

        if search_value:
            search_results = Price.objects.filter(
                Q(generic_name__icontains=search_value) |
                Q(brand_name__icontains=search_value)).exclude(
                    unit_price__isnull=True).order_by("generic_name")

            if search_results:
                result_list = []
                first_entry = True

                for item in search_results:
                    # Assemble the title
                    description = []

                    if item.strength: description.append(item.strength)
                    if item.route: description.append(item.route)
                    if item.dosage_form: description.append(item.dosage_form)

                    if len(description):
                        title = "%s (%s)" % (
                            item.generic_name,
                            " ".join(description)
                        )
                    else:
                        title = item.generic_name

                    if first_entry:
                        temp_dict = {
                            "title": title,
                            "url": item.url,
                            "brand_name": item.brand_name,
                        }

                        result_list.append(temp_dict)

                        first_entry = False
                    else:
                        title_match = False

                        # Look for a title match
                        for list_index, list_item in enumerate(result_list):
                            if list_item["title"] == title:
                                result_list[list_index]["url"] = "%s,%s" % (result_list[list_index]["url"], item.url)
                                result_list[list_index]["brand_name"] = "{},{}".format(
                                    result_list[list_index]["brand_name"], item.brand_name
                                )

                                title_match = True

                                break

                        if not title_match:
                            temp_dict = {
                                "title": title,
                                "url": item.url,
                                "brand_name": item.brand_name,
                            }

                            result_list.append(temp_dict)

                li_elements = []

                for index, item in enumerate(result_list):
                    element = (
                        "<li><a id='Search-Result-%s' data-url='%s' "
                        "onclick='chooseResult(this)'><strong>%s</strong><br>"
                        "<em>also known as %s</em></a></li>") % (
                            index, item["url"], item["title"], item["brand_name"]
                        )

                    li_elements.append(element)

                response = "<ul>%s</ul>" % ("".join(li_elements))
            else:
                response = "<ul><li><a><strong>No medication found</strong></a></li></ul>"

    return HttpResponse(response, content_type="text/html")

def add_item(request):
    response = []

    selection = request.GET["q"].split(",")

    for url in selection:
        # Get all the required price, coverage data, and special_auth data
        price = Price.objects.get(url=url)
        coverage = Coverage.objects.get(url=url)
        special_auth = SpecialAuthorization.objects.filter(url=url)

        # Create a dictionary out of both querysets (if there is a unit price)
        if price.unit_price:
            combo = {
                "url": url,
                "brand_name": price.brand_name,
                "strength": price.strength,
                "route": price.route,
                "dosage_form": price.dosage_form,
                "generic_name": price.generic_name,
                "unit_price": price.unit_price,
                "lca": price.lca,
                "unit_issue": price.unit_issue,
                "criteria": coverage.criteria,
                "coverage": coverage.coverage,
                "criteria_sa": coverage.criteria_sa,
                "criteria_p": coverage.criteria_p,
                "group_1": coverage.group_1,
                "group_66": coverage.group_66,
                "group_66a": coverage.group_66a,
                "group_19823": coverage.group_19823,
                "group_19823a": coverage.group_19823a,
                "group_19824": coverage.group_19824,
                "group_20400": coverage.group_20400,
                "group_20403": coverage.group_20403,
                "group_20514": coverage.group_20514,
                "group_22128": coverage.group_22128,
                "group_23609": coverage.group_23609,
                "special_auth": [],
            }

            for item in special_auth:
                if item.title:
                    combo["special_auth"].append({
                        "title": item.title,
                        "link": item.link,
                    })

            response.append(combo)

    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")

def comparison_search(request):
    """Returns a list of medications with matching generic name,
    brand name, ATC, or PTC"""
    # TOFIX: If a name match occurs and the ATC/PTC is not a 4th
    # level code, it will pull all children codes for that 1-3rd level code
    def bool_convert(txt):
        if txt == "true":
            return True
        else:
            return False

    def find_last_description(category, category_type):
        """Find the most specific classification"""
        if category_type == "ptc":
            if category.ptc_4_text:
                return category.ptc_4_text
            elif category.ptc_3_text:
                return category.ptc_3_text
            elif category.ptc_2_text:
                return category.ptc_2_text
            elif category.ptc_1_text:
                return category.ptc_1_text
        elif category_type == "atc":
            if category.atc_4_text:
                return category.atc_4_text
            elif category.atc_3_text:
                return category.atc_3_text
            elif category.atc_2_text:
                return category.atc_2_text
            elif category.atc_1_text:
                return category.atc_1_text

    def query_complete(urls, category_type):
        # Cycle through each URL and collect needed data
        output = []

        for url in urls:
            # Assemble dictionary from appropriate models
            if category_type == "atc":
                price = Price.objects.get(url=url)
                atc = ATC.objects.get(url=url)

                # Only include entries with a price
                if price.unit_price:
                    output.append({
                        "url": str(url),
                        "type": "atc",
                        "route": price.route,
                        "generic_name": price.generic_name,
                        "description": find_last_description(atc, "atc")
                    })
            elif category_type == "ptc":
                price = Price.objects.get(url=url)
                ptc = PTC.objects.get(url=url)

                # Only include entries with a price
                if price.unit_price:
                    output.append({
                        "url": str(url),
                        "type": "ptc",
                        "route": price.route,
                        "generic_name": price.generic_name,
                        "description": find_last_description(ptc, "ptc")
                    })

        return output

    def get_atc_url(search_string):
        """Searches for any match against all ATC records"""
        atc = ATC.objects.filter(
            Q(atc_1_text__icontains=search_string) |
            Q(atc_2_text__icontains=search_string) |
            Q(atc_3_text__icontains=search_string) |
            Q(atc_4_text__icontains=search_string)
        )

        urls = set()

        for item in atc:
            urls.add(item.url)

        return urls

    def get_ptc_url(search_string):
        """Searches for any match against all PTC records"""
        ptc = PTC.objects.filter(
            Q(ptc_1_text__icontains=search_string) |
            Q(ptc_2_text__icontains=search_string) |
            Q(ptc_3_text__icontains=search_string) |
            Q(ptc_4_text__icontains=search_string)
        )

        urls = set()

        for item in ptc:
            urls.add(item.url)

        return urls

    def get_name_url(search_string, category_type):
        """Retrieves any match against generic or brand name"""
        # Find any matching brand or generic name
        names = Price.objects.filter(
            Q(brand_name__icontains=search_string) |
            Q(generic_name__icontains=search_string)
        )

        description_list = set()
        urls = set()

        if category_type == "atc":
            # Use the URL of each match to find what the ATC code
            for item in names:
                atc = ATC.objects.get(url=item.url)
                description_list.add(find_last_description(atc, "atc"))
            # Use the collected ATC codes to find any matching URLs
            for desc in description_list:
                atc_urls = get_atc_url(desc)

                urls = urls.union(atc_urls)
        elif category_type == "ptc":
            # Use the URL of each match to find what the PTC code
            for item in names:
                ptc = PTC.objects.get(url=item.url)
                description_list.add(find_last_description(ptc, "ptc"))

            # Use the collected PTC codes to find any matching URLs
            for desc in description_list:
                ptc_urls = get_ptc_url(desc)

                urls = urls.union(ptc_urls)

        return urls

    def process_atc(search_string):
        """Searches and returns data matching search string (ATC & names)"""
        # Collects any matching ATC urls
        atc_urls = get_atc_url(search_string)

        # Collects any matching mediction name URLs
        name_urls = get_name_url(search_string, "atc")

        # Combine URL results
        urls = atc_urls.union(name_urls)

        # Use collected URLs to collect the full entry data
        if len(urls):
            return query_complete(urls, "atc")
        else:
            return []

    def process_ptc(search_string):
        """Searches and returns data matching search string (ATC & names)"""
        # Collects any matching ATC urls
        ptc_urls = get_ptc_url(search_string)

        # Collects any matching mediction name URLs
        name_urls = get_name_url(search_string, "ptc")

        # Combine URL results
        urls = ptc_urls.union(name_urls)

        # Use collected URLs to collect the full entry data
        if len(urls):
            return query_complete(urls, "ptc")
        else:
            return []

    response = ""

    search_string = request.GET["search"]
    method_atc = bool_convert(request.GET["methodATC"])
    method_ptc = bool_convert(request.GET["methodPTC"])

    # Only process request if there is a search string
    if search_string:
        result_list = []

        # Retrieve ATC results
        if method_atc:
            temp_list = process_atc(search_string)
            result_list = result_list + temp_list

        # Retrieve PTC results
        if method_ptc:
            temp_list = process_ptc(search_string)
            result_list = result_list + temp_list


    # Group retrieved items under common category descriptions
    first_item = True
    grouped_items = []

    for item in result_list:
        # Assemble a common title
        title = "%s (%s)" % (item["description"], item["type"].upper())

        if first_item:
            grouped_items.append({
                "title": title,
                "url": item["url"],
                "drugs": item["generic_name"]
            })
            first_item = False
        else:
            match = False

            for index, group in enumerate(grouped_items):
                if group["title"] == title:
                    # Append new URL
                    grouped_items[index]["url"] += ",%s" % item["url"]

                    # Append generic name (if unique)
                    # TODO: Fix bug where a partial name match (e.g.
                    # "lidocaine" in "lidocaine HCl" is not added
                    if item["generic_name"] not in grouped_items[index]["drugs"]:
                        grouped_items[index]["drugs"] += ", %s" % item["generic_name"]

                    match = True

                    break

            if match == False:
                grouped_items.append({
                    "title": title,
                    "url": item["url"],
                    "drugs": item["generic_name"]
                })

    # Takes the grouped items and converts to an HTML list
    if len(grouped_items):
        list_items = []

        for index, item in enumerate(grouped_items):
            list_items.append(
                "<li><a id='Comparison-Result-%s' data-url='%s' "
                "onclick='chooseComparison(this)'>"
                "<strong>%s</strong><br><em>Examples: %s</em></a>"
                "</li>" % (index, item["url"], item["title"], item["drugs"])
            )

        response = "<ul>%s</ul>" % "".join(list_items)
    else:
        # If no grouped items are available, provide appropriate user response
        if method_atc == False and method_ptc == False:
            response = ("<ul><li><a><strong>Please select a classification "
                        "system above</strong></a></li></ul>")
        else:
            response = ("<ul><li><a><strong>No results "
                        "found</strong></a></li></ul>")

    return HttpResponse(response, content_type="text/html")

def generate_comparison(request):
    # Collect pricing information for the selected urls
    results = []

    urls = request.GET["q"].split(",")

    for url in urls:
        # Get data from required objects
        price = Price.objects.get(url=url)
        coverage = Coverage.objects.get(url=url)
        special_auth = SpecialAuthorization.objects.filter(url=url)

        # Add results to results list if price is not null
        if price.unit_price:
            result = {
                "url": url,
                "strength": price.strength,
                "generic_name": price.generic_name,
                "unit_price": price.unit_price,
                "lca": price.lca,
                "unit_issue": price.unit_issue,
                "criteria": coverage.criteria,
                "coverage": coverage.coverage,
                "criteria_sa": coverage.criteria_sa,
                "criteria_p": coverage.criteria_p,
                "group_1": coverage.group_1,
                "group_66": coverage.group_66,
                "group_66a": coverage.group_66a,
                "group_19823": coverage.group_19823,
                "group_19823a": coverage.group_19823a,
                "group_19824": coverage.group_19824,
                "group_20400": coverage.group_20400,
                "group_20403": coverage.group_20403,
                "group_20514": coverage.group_20514,
                "group_22128": coverage.group_22128,
                "group_23609": coverage.group_23609,
                "special_auth": [],
            }

            # Add any special auth links
            for item in special_auth:
                if item.title:
                    result["special_auth"].append({
                        "title": item.title,
                        "link": item.link,
                    })

            results.append(result)

    # Combines the results list into single generic names
    combined_list = []
    first_item = True

    for result in results:
        # Group by generic Name
        if first_item:
            combined_list.append({
                "generic_name": result["generic_name"],
                "strength": [{
                    "strength": result["strength"],
                    "unit_price": result["unit_price"],
                    "lca": result["lca"],
                    "criteria": result["criteria"],
                    "coverage": result["coverage"],
                    "criteria_sa": result["criteria_sa"],
                    "criteria_p": result["criteria_p"],
                    "group_1": result["group_1"],
                    "group_66": result["group_66"],
                    "group_66a": result["group_66a"],
                    "group_19823": result["group_19823"],
                    "group_19823a": result["group_19823a"],
                    "group_19824": result["group_19824"],
                    "group_20400": result["group_20400"],
                    "group_20403": result["group_20403"],
                    "group_20514": result["group_20514"],
                    "group_22128": result["group_22128"],
                    "group_23609": result["group_23609"],
                    "special_auth": result["special_auth"],
                }],
            })

            first_item = False
        else:
            generic_match = False
            strength_match = False

            # Check for a matching generic name
            for g, generic_item in enumerate(combined_list):
                if result["generic_name"] == generic_item["generic_name"]:
                    generic_match = True

                    # Check for matching strength
                    for s, strength_item in enumerate(generic_item["strength"]):
                        if result["strength"] == strength_item["strength"]:
                            strength_match = True

                            # If unit price is lower, replace the contents
                            if result["unit_price"] < strength_item["unit_price"]:
                                combined_list[g]["strength"][s]["unit_price"] = result["unit_price"]
                                combined_list[g]["strength"][s]["lca"] = result["lca"],
                                combined_list[g]["strength"][s]["criteria"] = result["criteria"],
                                combined_list[g]["strength"][s]["coverage"] = result["coverage"],
                                combined_list[g]["strength"][s]["criteria_sa"] = result["criteria_sa"],
                                combined_list[g]["strength"][s]["criteria_p"] = result["criteria_p"],
                                combined_list[g]["strength"][s]["group_1"] = result["group_1"],
                                combined_list[g]["strength"][s]["group_66"] = result["group_66"],
                                combined_list[g]["strength"][s]["group_66a"] = result["group_66a"],
                                combined_list[g]["strength"][s]["group_19823"] = result["group_19823"],
                                combined_list[g]["strength"][s]["group_19823a"] = result["group_19823a"],
                                combined_list[g]["strength"][s]["group_19824"] = result["group_19824"],
                                combined_list[g]["strength"][s]["group_20400"] = result["group_20400"],
                                combined_list[g]["strength"][s]["group_20403"] = result["group_20403"],
                                combined_list[g]["strength"][s]["group_20514"] = result["group_20514"],
                                combined_list[g]["strength"][s]["group_22128"] = result["group_22128"],
                                combined_list[g]["strength"][s]["group_23609"] = result["group_23609"],
                                combined_list[g]["strength"][s]["special_auth"] = result["special_auth"],

                            break

                    # If no strength match found, create a new entry
                    if strength_match == False:
                        combined_list[g]["strength"].append({
                            "strength": result["strength"],
                            "unit_price": result["unit_price"],
                            "lca": result["lca"],
                            "criteria": result["criteria"],
                            "coverage": result["coverage"],
                            "criteria_sa": result["criteria_sa"],
                            "criteria_p": result["criteria_p"],
                            "group_1": result["group_1"],
                            "group_66": result["group_66"],
                            "group_66a": result["group_66a"],
                            "group_19823": result["group_19823"],
                            "group_19823a": result["group_19823a"],
                            "group_19824": result["group_19824"],
                            "group_20400": result["group_20400"],
                            "group_20403": result["group_20403"],
                            "group_20514": result["group_20514"],
                            "group_22128": result["group_22128"],
                            "group_23609": result["group_23609"],
                            "special_auth": result["special_auth"],
                        })

                    break

            # If not generic match found, create a new entry
            if generic_match == False:
                combined_list.append({
                    "generic_name": result["generic_name"],
                    "strength": [{
                        "strength": result["strength"],
                        "unit_price": result["unit_price"],
                        "lca": result["lca"],
                        "criteria": result["criteria"],
                        "coverage": result["coverage"],
                        "criteria_sa": result["criteria_sa"],
                        "criteria_p": result["criteria_p"],
                        "group_1": result["group_1"],
                        "group_66": result["group_66"],
                        "group_66a": result["group_66a"],
                        "group_19823": result["group_19823"],
                        "group_19823a": result["group_19823a"],
                        "group_19824": result["group_19824"],
                        "group_20400": result["group_20400"],
                        "group_20403": result["group_20403"],
                        "group_20514": result["group_20514"],
                        "group_22128": result["group_22128"],
                        "group_23609": result["group_23609"],
                        "special_auth": result["special_auth"],
                    }],
                })

    # Sorts the combined_list so generic names appear in alphabetical order
    combined_list = sorted(combined_list, key=lambda x: x["generic_name"])

    # Sorts the combined_list so strengths appear form lowest to highest
    import re

    for index, combo in enumerate(combined_list):
        def sort_by_strength(strength):
            """Returns the numerical value of the "strength" key"""
            regex = r"([\d|\.]+\b)"

            strength_regex = re.search(regex, strength["strength"])

            if strength_regex:
                return float(strength_regex.group(1))
            else:
                return strength["strength"]

        combined_list[index]["strength"] = sorted(
            combo["strength"], key=sort_by_strength
        )


    return HttpResponse(
        json.dumps(combined_list, cls=DjangoJSONEncoder),
        content_type="application/json"
    )
