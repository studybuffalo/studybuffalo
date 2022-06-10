# import logging
# from bisect import bisect_left

# from hc_dpd.models import (
#     SubAHFS, SubBrand, SubCompanyName, SubDescriptor, SubIngredient,
#     SubProductCategorization, SubRouteOfAdministration,
#     SubPharmaceuticalStd, SubStreetName, SubSuiteNumber, SubUnit
# )


# # Setup logging
# log = logging.getLogger(__name__)


# class SubList(object):
#     """An object of lists of original text and index-matched subs"""
#     def __init__(self, original, substitution):
#         self.original = original
#         self.substitution = substitution

# def generate_sub_list(model):
#     """Converts Django sub data model to a SubList object"""
#     # Sorts all the model objects alphabetically (cannot use "ordery_by"
#     # due to differences in how database engines sort)
#     original = []
#     substitution = []

#     # Add the first item to the lists
#     model_list = list(model.objects.values())

#     if len(model_list):
#         original.append(model_list[0]["original"])
#         substitution.append(model_list[0]["substitution"])

#         # Remove first entry
#         model_list.pop(0)

#     for item in model_list:
#         # Find where to insert next item
#         i = bisect_left(original, item["original"])

#         # Insert the dictionaries into the lists
#         original.insert(i, item["original"])
#         substitution.insert(i, item["substitution"])

#     return SubList(original, substitution)


# class Substitutions(object):
#     def __init__(self):
#         self.ahfs = generate_sub_list(SubAHFS)
#         self.brand_name = generate_sub_list(SubBrand)
#         self.company_name = generate_sub_list(SubCompanyName)
#         self.descriptor = generate_sub_list(SubDescriptor)
#         self.ingredient = generate_sub_list(SubIngredient)
#         self.product_categorization = generate_sub_list(SubProductCategorization)
#         self.route_of_administration = generate_sub_list(SubRouteOfAdministration)
#         self.pharmaceutical_std = generate_sub_list(SubPharmaceuticalStd)
#         self.street_name = generate_sub_list(SubStreetName)
#         self.suite_number = generate_sub_list(SubSuiteNumber)
#         self.unit = generate_sub_list(SubUnit)
