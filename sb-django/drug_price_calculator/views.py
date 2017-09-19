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
from django.db.models import Q
from django.core import serializers

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
                Q(brand_name__icontains=search_value)).order_by("generic_name")

            if search_results:
                result_list = []
                first_entry = True

                for item in search_results:
                    title = item.generic_name
                    
                    """
                    $tempText = $item['generic_name'] . " (" . $item['strength'] . " " . 
						    $item['route'] . " " . $item['dosage_form'] . ")";
						
			        //Cleans up the tempText in case an item was missing
			        $tempText = str_replace("  ", " ", $tempText);
			        $tempText = str_replace("  ", " ", $tempText);
			        $tempText = str_replace("( ", "(", $tempText);
			        $tempText = str_replace(" )", ")", $tempText);
			        $tempText = str_replace(" ()", "", $tempText);
                    """

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
                                result_list[list_index]["brand_name"] = "%s,%s" % (result_list[list_index]["brand_name"], item.brand_name)
                                
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

import json

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
                "unit_price": str(price.unit_price),
                "lca": str(price.lca),
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

    return HttpResponse(json.dumps(response), content_type="application/json")

def comparison_search(request):
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
        # Remove duplicate URLs
        urls = list(set(urls))

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

        urls = []

        for item in atc:
            urls.append(item.url)

        return urls

    def get_ptc_url(search_string):
        """Searches for any match against all PTC records"""
        atc = ATC.objects.filter(
            Q(ptc_1_text__icontains=search_string) |
            Q(ptc_2_text__icontains=search_string) |
            Q(ptc_3_text__icontains=search_string) |
            Q(ptc_4_text__icontains=search_string)
        )

        urls = []

        for item in atc:
            urls.append(item.url)

        return urls

    def get_name_url(search_string, category_type):
        """Retrieves any match against generic or brand name"""
        # Find any matching brand or generic name
        names = Price.objects.filter(
            Q(brand_name__icontains=search_string) |
            Q(generic_name__icontains=search_string)
        )
        
        description_list = []
        urls = []

        if category_type == "atc":
            # Use the URL of each match to find what the ATC code
            for item in names:
                atc = ATC.objects.get(url=item.url)
                description_list.append(find_last_description(atc, "atc"))

            # Use the collected ATC codes to find any matching URLs
            for desc in description_list:
                atc_urls = get_atc_url(desc)

                urls = urls + atc_urls
        elif category_type == "ptc":
            # Use the URL of each match to find what the PTC code
            for item in names:
                ptc = PTC.objects.get(url=item.url)
                description_list.append(find_last_description(ptc, "ptc"))
            
            # Use the collected PTC codes to find any matching URLs
            for desc in description_list:
                atc = PTC.objects.filter(get_ptc_url(desc))

                urls.append(ptc.url)
      
        return urls

    def process_atc(search_string):
        """Searches and returns data matching search string (ATC & names)"""
        # Collects any matching ATC urls
        atc_urls = get_atc_url(search_string)

        # Collects any matching mediction name URLs
        name_urls = get_name_url(search_string, "atc")

        # Combine URL results
        urls = atc_urls + name_urls

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
        urls = ptc_urls + name_urls

        # Use collected URLs to collect the full entry data
        if len(urls):
            return query_complete(urls, "ptc")
        else:
            return []

    response = ""
    htmlList = []

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
                    grouped_items[index]["url"] += ",%s" % group["url"]

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
    """
        <?php

        require_once '../../../../config/db_config.php';

        $resultArray = array();
        $urlArray = array();
        $outputList = array();
        $q = explode(",", $_GET["q"]);

        // Establish database connection
        $db = db_connect('sb', 'abc_vw');

        // Sending prepared statement to server
        $params = implode(",", array_fill(0, count($q), "?"));
        $query = "SELECT DISTINCT t1.url, t1.strength, t1.generic_name, " .
		         "t1.unit_price, t1.lca, t2.coverage, t2.criteria_sa, " .
		         "t2.criteria_p, t2.group_1, t2.group_66, t2.group_66a, " .
		         "t2.group_19823, t2.group_19823a, t2.group_19824, " .
		         "t2.group_20400, t2.group_20403, t2.group_20514, " .
		         "t2.group_22128, t2.group_23609 " .
		         "FROM abc_price t1 " .
		         "JOIN abc_coverage t2 " .
		         "ON t1.url = t2.url " .
		         "WHERE t1.url IN ($params) AND t1.unit_price IS NOT NULL";

        $statement = $db->prepare($query);
        $statement->execute($q);

        // Copy server results to array
        while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
	        // Creates special auth entry in results
	        $temp['special_auth'] = array();

	        // Adds results to array
	        array_push($resultArray, $temp);

	        // Collects all URLs for special auth query
	        array_push($urlArray, $temp['url']);
        }

        // Collects retrieved URLs and retrieves special auth information
        $params = implode(",", array_fill(0, count($urlArray), "?"));
        $query = "SELECT url, title, link " .
		         "FROM abc_special_authorization " .
		         "WHERE url IN ($params) AND title IS NOT NULL";

        $statement = $db->prepare($query);
        $statement->execute($urlArray);

        // Matches the special auth data to the appropriate $resultArray entries
        while ($temp = $statement->fetch(PDO::FETCH_ASSOC)) {
	        for ($i = 0; $i < count($resultArray); $i++) {
		        if ($resultArray[$i]['url'] === $temp['url']) {
			        array_push($resultArray[$i]['special_auth'], $temp);
		        }
	        }
        }

        /*
	        Group each drug by generic name
	        Create drop downs for each available strength
	        Each strength linked to the LCA
        */

        // Format results into an array for html processing
        if (count($resultArray) > 0) {
	        foreach ($resultArray as $key => $item) {
		        // Groups each entry by generic name and strength
		        if ($key == 0) {
			        $outputArray[0] = array('generic_name' => $item['generic_name'],
									        'strength' => array());
			        $outputArray[0]['strength'][0]['strength'] = $item['strength'];
			        $outputArray[0]['strength'][0]['unit_price'] = $item['unit_price'];
			        $outputArray[0]['strength'][0]['lca'] = $item['lca'];
			        $outputArray[0]['strength'][0]['coverage'] = $item['coverage'];
			        $outputArray[0]['strength'][0]['criteria_sa'] = $item['criteria_sa'];
			        $outputArray[0]['strength'][0]['criteria_p'] = $item['criteria_p'];
			        $outputArray[0]['strength'][0]['group_1'] = $item['group_1'];
			        $outputArray[0]['strength'][0]['group_66'] = $item['group_66'];
			        $outputArray[0]['strength'][0]['group_66a'] = $item['group_66a'];
			        $outputArray[0]['strength'][0]['group_19823'] = $item['group_19823'];
			        $outputArray[0]['strength'][0]['group_19823a'] = $item['group_19823a'];
			        $outputArray[0]['strength'][0]['group_19824'] = $item['group_19824'];
			        $outputArray[0]['strength'][0]['group_20400'] = $item['group_20400'];
			        $outputArray[0]['strength'][0]['group_20403'] = $item['group_20403'];
			        $outputArray[0]['strength'][0]['group_20514'] = $item['group_20514'];
			        $outputArray[0]['strength'][0]['group_22128'] = $item['group_22128'];
			        $outputArray[0]['strength'][0]['group_23609'] = $item['group_23609'];
			        $outputArray[0]['strength'][0]['special_auth'] = $item['special_auth'];
		        } else {
			        $genericMatch = FALSE;
			        $strengthMatch = FALSE;

			        // Checks for matching generic name
			        for ($i = 0; $i < count($outputArray); $i++) {
				        if ($outputArray[$i]['generic_name'] == $item['generic_name']) {
					        $genericMatch = TRUE;

					        // Then checks for matching strength
					        for ($j = 0; $j < count($outputArray[$i]['strength']); $j++) {
						        if ($outputArray[$i]['strength'][$j]['strength'] == $item['strength']) {
							        $strengthMatch = TRUE;

							        // If unit price is lower, replaces the array contents
							        if ($item['unit_price'] < $outputArray[$i]['strength'][$j]['unit_price']) {
								        $outputArray[$i]['strength'][$j]['unit_price'] = $item['unit_price'];
								        $outputArray[$i]['strength'][$j]['lca'] = $item['lca'];
								        $outputArray[$i]['strength'][$j]['coverage'] = $item['coverage'];
								        $outputArray[$i]['strength'][$j]['criteria_sa'] = $item['criteria_sa'];
								        $outputArray[$i]['strength'][$j]['criteria_p'] = $item['criteria_p'];
								        $outputArray[$i]['strength'][$j]['group_1'] = $item['group_1'];
								        $outputArray[$i]['strength'][$j]['group_66'] = $item['group_66'];
								        $outputArray[$i]['strength'][$j]['group_66a'] = $item['group_66a'];
								        $outputArray[$i]['strength'][$j]['group_19823'] = $item['group_19823'];
								        $outputArray[$i]['strength'][$j]['group_19823a'] = $item['group_19823a'];
								        $outputArray[$i]['strength'][$j]['group_19824'] = $item['group_19824'];
								        $outputArray[$i]['strength'][$j]['group_20400'] = $item['group_20400'];
								        $outputArray[$i]['strength'][$j]['group_20403'] = $item['group_20403'];
								        $outputArray[$i]['strength'][$j]['group_20514'] = $item['group_20514'];
								        $outputArray[$i]['strength'][$j]['group_22128'] = $item['group_22128'];
								        $outputArray[$i]['strength'][$j]['group_23609'] = $item['group_23609'];
								        $outputArray[$i]['strength'][$j]['special_auth'] = $item['special_auth'];
							        }

							        break;
						        }
					        }

					        // If no strength match was found, adds it to this generic entry
					        if ($strengthMatch === FALSE) {
						        $index = count($outputArray[$i]['strength']);
						        $outputArray[$i]['strength'][$index] = array(
								        'strength' => $item['strength'],
								        'unit_price' => $item['unit_price'],
								        'lca' => $item['lca'],
								        'coverage' => $item['coverage'],
								        'criteria_sa' => $item['criteria_sa'],
								        'criteria_p' => $item['criteria_p'],
								        'group_1' => $item['group_1'],
								        'group_66' => $item['group_66'],
								        'group_66a' => $item['group_66a'],
								        'group_19823' => $item['group_19823'],
								        'group_19823a' => $item['group_19823a'],
								        'group_19824' => $item['group_19824'],
								        'group_20400' => $item['group_20400'],
								        'group_20403' => $item['group_20403'],
								        'group_20514' => $item['group_20514'],
								        'group_22128' => $item['group_22128'],
								        'group_23609' => $item['group_23609'],
								        'special_auth' => $item['special_auth']);
					        }

					        break;
				        }
			        }

			        // If no generic match was found, adds it to the array
			        if ($genericMatch == FALSE) {
				        $index = count($outputArray);
				        $outputArray[$index] = array('generic_name' => $item['generic_name'],
											         'strength' => array());
				        $outputArray[$index]['strength'][0]['strength'] = $item['strength'];
				        $outputArray[$index]['strength'][0]['unit_price'] = $item['unit_price'];
				        $outputArray[$index]['strength'][0]['lca'] = $item['lca'];
				        $outputArray[$index]['strength'][0]['coverage'] = $item['coverage'];
				        $outputArray[$index]['strength'][0]['criteria_sa'] = $item['criteria_sa'];
				        $outputArray[$index]['strength'][0]['criteria_p'] = $item['criteria_p'];
				        $outputArray[$index]['strength'][0]['group_1'] = $item['group_1'];
				        $outputArray[$index]['strength'][0]['group_66'] = $item['group_66'];
				        $outputArray[$index]['strength'][0]['group_66a'] = $item['group_66a'];
				        $outputArray[$index]['strength'][0]['group_19823'] = $item['group_19823'];
				        $outputArray[$index]['strength'][0]['group_19823a'] = $item['group_19823a'];
				        $outputArray[$index]['strength'][0]['group_19824'] = $item['group_19824'];
				        $outputArray[$index]['strength'][0]['group_20400'] = $item['group_20400'];
				        $outputArray[$index]['strength'][0]['group_20403'] = $item['group_20403'];
				        $outputArray[$index]['strength'][0]['group_20514'] = $item['group_20514'];
				        $outputArray[$index]['strength'][0]['group_22128'] = $item['group_22128'];
				        $outputArray[$index]['strength'][0]['group_23609'] = $item['group_23609'];
				        $outputArray[$index]['strength'][0]['special_auth'] = $item['special_auth'];
			        }
		        }
	        }
        }

        // Sorts the strength items from lowest to highest
        if (count($outputArray) > 0) {
	        function sortFunction($a, $b) {
		        $pattern = '/([\d|\.]+\b)/';

		        if (preg_match($pattern, $a['strength'], $matches)) {
			        $a = $matches[1];
		        } else {
			        $a = $a['strength'];
		        }

		        if (preg_match($pattern, $b['strength'], $matches)) {
			        $b = $matches[1];
		        } else {
			        $b = $b['strength'];
		        }

		        if ($a == $b) {
			        return 0;
		        } else if ($a < $b) {
			        return -1;
		        } else {
			        return 1;
		        }
	        }

	        for ($i = 0; $i < count($outputArray); $i++) {
		        usort($outputArray[$i]['strength'], 'sortFunction');
	        }
        }

        echo json_encode($outputArray);
        ?>
    """