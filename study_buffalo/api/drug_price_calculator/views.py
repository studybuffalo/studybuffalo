"""Views for the Drug Price Calculator API."""
from django.db.models import Q

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from drug_price_calculator import models

from api.drug_price_calculator import serializers


class UploadiDBLData(GenericAPIView):
    serializer_class = serializers.iDBLDataSerializer

    def post(self, request, din):
        # Confirm DIN is in valid format
        if len(din) != 8:
            message = {
                'error': 'invalid_din',
                'error_description': 'DIN/NPN/PIN format is invalid.',
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create model instance
        drug, _ = models.Drug.objects.get_or_create(din=din)

        # Serializer and validate data
        serializer = self.get_serializer(data=request.data, instance=drug)

        if serializer.is_valid() is False:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        # Save the serializer data
        serializer.save()

        # Format response message
        message = {
            'message': 'Drug and price file successfully created.',
            'drug_id': drug.id,
        }

        return Response(data=message, status=status.HTTP_201_CREATED)

class DrugListPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_query_param = 'page'

class DrugList(ListAPIView):
    """List of Drugs based on query filters."""
    serializer_class = serializers.DrugListSerializer
    permission_classes = []
    pagination_class = DrugListPagination

    def get_queryset(self):
        """Override to apply search filters."""
        q_string = self.request.GET.get('q', '')

        queryset = models.Drug.objects.filter(
            Q(generic_name__icontains=q_string) | Q(brand_name__icontains=q_string)
        ).exclude(
            prices__unit_price__isnull=True
        ).order_by(
            'generic_product'
        )

        return queryset

class DrugPriceList(ListAPIView):
    """List of drugs and prices based on requested products."""
    serializer_class = serializers.DrugPriceListSerializer
    permission_classes = []

    def get_queryset(self):
        """Overriding to apply filters."""
        drug_ids_string = self.request.GET.get('ids', None)

        if not drug_ids_string:
            raise NotFound('No IDs provided in query.')

        drug_ids = drug_ids_string.split(',')

        try:
            queryset = models.Price.objects.filter(
                drug__id__in=drug_ids
            )
        except ValueError:
            raise NotFound('Invalid ID format provided.')

        return queryset

class ComparisonList(ListAPIView):
    """List of drug class comparisons based on query parameters."""
    serializer_class = serializers.ComparisonListSerializer
    permission_classes = []
    pagination_class = DrugListPagination

    def get_queryset(self):
        """Override to apply search filters."""
        # Will need to develop system to:
        #   1) Search against the text descriptions
        #   2) Provide list of ATC/PTC records that match that description
        #   3) When selected by user, use the specific ATC/PTC record
        #      to retrieve drug price records
        #
        # Issues:
        #   1) ATC is now matched to a single drug; need way to move one level down
        q_string = self.request.GET.get('q')
        system = self.request.GET.get('system', 'atc')

        if system == 'atc':
            return Response(self._search_atc(q_string), status=status.HTTP_200_OK)

        if system == 'ptc':
            return Response(self._search_ptc(q_string), status=status.HTTP_200_OK)

        # Invalid system provided
        message = {
            'error': 'invalid_system',
            'error_description': 'Invalid classification system provided.',
        }
        return Response(message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def _search_atc(q_string):
        """Searches and returns data matching search string (ATC & names)"""
        # Collects any matching ATC urls
        atc = models.ATC.objects.filter(
            Q(atc_1_text__icontains=q_string) |
            Q(atc_2_text__icontains=q_string) |
            Q(atc_3_text__icontains=q_string) |
            Q(atc_4_text__icontains=q_string) |
            Q(atc_5_text__icontains=q_string) |
            Q(atc__drugs_generic_name__icontains=q_string) |
            Q(atc__drugs_brand_name__icontains=q_string)
        ).unique()

        return atc

    @staticmethod
    def _search_ptc(q_string):
        """Searches and returns data matching search string (ATC & names)"""
        ptc = models.PTC.objects.filter(
            Q(ptc_1_text__icontains=q_string) |
            Q(ptc_2_text__icontains=q_string) |
            Q(ptc_3_text__icontains=q_string) |
            Q(ptc_4_text__icontains=q_string) |
            Q(ptc__drugs_generic_name__icontains=q_string) |
            Q(ptc__drugs_brand_name__icontains=q_string)
        )

        return ptc

class ComparisonPriceList(ListAPIView):
    """Returns list of Drug Prices for comparison category."""
    def get_queryset(self):
        # Collect pricing information for the selected urls

        # urls = request.GET["q"].split(",")

        # for url in urls:
        #     # Get data from required objects
        #     price = Price.objects.get(url=url)
        #     coverage = Coverage.objects.get(url=url)
        #     special_auth = SpecialAuthorization.objects.filter(url=url)

        #     # Add results to results list if price is not null
        #     if price.unit_price:
        #         result = {
        #             "url": url,
        #             "strength": price.strength,
        #             "generic_name": price.generic_name,
        #             "unit_price": price.unit_price,
        #             "lca": price.lca,
        #             "unit_issue": price.unit_issue,
        #             "criteria": coverage.criteria,
        #             "coverage": coverage.coverage,
        #             "criteria_sa": coverage.criteria_sa,
        #             "criteria_p": coverage.criteria_p,
        #             "group_1": coverage.group_1,
        #             "group_66": coverage.group_66,
        #             "group_66a": coverage.group_66a,
        #             "group_19823": coverage.group_19823,
        #             "group_19823a": coverage.group_19823a,
        #             "group_19824": coverage.group_19824,
        #             "group_20400": coverage.group_20400,
        #             "group_20403": coverage.group_20403,
        #             "group_20514": coverage.group_20514,
        #             "group_22128": coverage.group_22128,
        #             "group_23609": coverage.group_23609,
        #             "special_auth": [],
        #         }

        #         # Add any special auth links
        #         for item in special_auth:
        #             if item.title:
        #                 result["special_auth"].append({
        #                     "title": item.title,
        #                     "link": item.link,
        #                 })

        #         results.append(result)

        # # Combines the results list into single generic names
        # combined_list = []
        # first_item = True

        # for result in results:
        #     # Group by generic Name
        #     if first_item:
        #         combined_list.append({
        #             "generic_name": result["generic_name"],
        #             "strength": [{
        #                 "strength": result["strength"],
        #                 "unit_price": result["unit_price"],
        #                 "lca": result["lca"],
        #                 "criteria": result["criteria"],
        #                 "coverage": result["coverage"],
        #                 "criteria_sa": result["criteria_sa"],
        #                 "criteria_p": result["criteria_p"],
        #                 "group_1": result["group_1"],
        #                 "group_66": result["group_66"],
        #                 "group_66a": result["group_66a"],
        #                 "group_19823": result["group_19823"],
        #                 "group_19823a": result["group_19823a"],
        #                 "group_19824": result["group_19824"],
        #                 "group_20400": result["group_20400"],
        #                 "group_20403": result["group_20403"],
        #                 "group_20514": result["group_20514"],
        #                 "group_22128": result["group_22128"],
        #                 "group_23609": result["group_23609"],
        #                 "special_auth": result["special_auth"],
        #             }],
        #         })

        #         first_item = False
        #     else:
        #         generic_match = False
        #         strength_match = False

        #         # Check for a matching generic name
        #         for g, generic_item in enumerate(combined_list):
        #             if result["generic_name"] == generic_item["generic_name"]:
        #                 generic_match = True

        #                 # Check for matching strength
        #                 for s, strength_item in enumerate(generic_item["strength"]):
        #                     if result["strength"] == strength_item["strength"]:
        #                         strength_match = True

        #                         # If unit price is lower, replace the contents
        #                         if result["unit_price"] < strength_item["unit_price"]:
        #                             combined_list[g]["strength"][s]["unit_price"] = result["unit_price"]
        #                             combined_list[g]["strength"][s]["lca"] = result["lca"],
        #                             combined_list[g]["strength"][s]["criteria"] = result["criteria"],
        #                             combined_list[g]["strength"][s]["coverage"] = result["coverage"],
        #                             combined_list[g]["strength"][s]["criteria_sa"] = result["criteria_sa"],
        #                             combined_list[g]["strength"][s]["criteria_p"] = result["criteria_p"],
        #                             combined_list[g]["strength"][s]["group_1"] = result["group_1"],
        #                             combined_list[g]["strength"][s]["group_66"] = result["group_66"],
        #                             combined_list[g]["strength"][s]["group_66a"] = result["group_66a"],
        #                             combined_list[g]["strength"][s]["group_19823"] = result["group_19823"],
        #                             combined_list[g]["strength"][s]["group_19823a"] = result["group_19823a"],
        #                             combined_list[g]["strength"][s]["group_19824"] = result["group_19824"],
        #                             combined_list[g]["strength"][s]["group_20400"] = result["group_20400"],
        #                             combined_list[g]["strength"][s]["group_20403"] = result["group_20403"],
        #                             combined_list[g]["strength"][s]["group_20514"] = result["group_20514"],
        #                             combined_list[g]["strength"][s]["group_22128"] = result["group_22128"],
        #                             combined_list[g]["strength"][s]["group_23609"] = result["group_23609"],
        #                             combined_list[g]["strength"][s]["special_auth"] = result["special_auth"],

        #                         break

        #                 # If no strength match found, create a new entry
        #                 if strength_match == False:
        #                     combined_list[g]["strength"].append({
        #                         "strength": result["strength"],
        #                         "unit_price": result["unit_price"],
        #                         "lca": result["lca"],
        #                         "criteria": result["criteria"],
        #                         "coverage": result["coverage"],
        #                         "criteria_sa": result["criteria_sa"],
        #                         "criteria_p": result["criteria_p"],
        #                         "group_1": result["group_1"],
        #                         "group_66": result["group_66"],
        #                         "group_66a": result["group_66a"],
        #                         "group_19823": result["group_19823"],
        #                         "group_19823a": result["group_19823a"],
        #                         "group_19824": result["group_19824"],
        #                         "group_20400": result["group_20400"],
        #                         "group_20403": result["group_20403"],
        #                         "group_20514": result["group_20514"],
        #                         "group_22128": result["group_22128"],
        #                         "group_23609": result["group_23609"],
        #                         "special_auth": result["special_auth"],
        #                     })

        #                 break

        #         # If not generic match found, create a new entry
        #         if generic_match == False:
        #             combined_list.append({
        #                 "generic_name": result["generic_name"],
        #                 "strength": [{
        #                     "strength": result["strength"],
        #                     "unit_price": result["unit_price"],
        #                     "lca": result["lca"],
        #                     "criteria": result["criteria"],
        #                     "coverage": result["coverage"],
        #                     "criteria_sa": result["criteria_sa"],
        #                     "criteria_p": result["criteria_p"],
        #                     "group_1": result["group_1"],
        #                     "group_66": result["group_66"],
        #                     "group_66a": result["group_66a"],
        #                     "group_19823": result["group_19823"],
        #                     "group_19823a": result["group_19823a"],
        #                     "group_19824": result["group_19824"],
        #                     "group_20400": result["group_20400"],
        #                     "group_20403": result["group_20403"],
        #                     "group_20514": result["group_20514"],
        #                     "group_22128": result["group_22128"],
        #                     "group_23609": result["group_23609"],
        #                     "special_auth": result["special_auth"],
        #                 }],
        #             })

        # # Sorts the combined_list so generic names appear in alphabetical order
        # combined_list = sorted(combined_list, key=lambda x: x["generic_name"])

        # # Sorts the combined_list so strengths appear form lowest to highest
        # import re

        # for index, combo in enumerate(combined_list):
        #     def sort_by_strength(strength):
        #         """Returns the numerical value of the "strength" key"""
        #         regex = r"([\d|\.]+\b)"

        #         strength_regex = re.search(regex, strength["strength"])

        #         if strength_regex:
        #             return float(strength_regex.group(1))
        #         else:
        #             return strength["strength"]

        #     combined_list[index]["strength"] = sorted(
        #         combo["strength"], key=sort_by_strength
        #     )

        return Response('', status=status.HTTP_200_OK)
