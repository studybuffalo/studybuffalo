# from bisect import bisect_left
# from datetime import date
# import logging
# import re
# from titlecase import titlecase

# from hc_dpd.models import (
#     SubAHFSPend, SubBrandPend, SubCompanyNamePend, SubDescriptorPend,
#     SubIngredientPend, SubProductCategorizationPend,
#     SubRouteOfAdministrationPend, SubPharmaceuticalStdPend,
#     SubStreetNamePend, SubSuiteNumberPend, SubUnitPend
# )

# # Setup logging
# log = logging.getLogger(__name__)


# # FREQUENTLY USED GENERAL FUNCTIONS
# def binary_search(term, sub_list):
#     """Completes a binary search for term in the provided list
#         args:
#             term        a string to search for
#             sub_list    a SubList object
#         returns:
#             Match       the substituted string
#             No Match    None
#         raises:
#             None
#     """

#     # Look for match
#     i = bisect_left(sub_list.original, term)

#     # If match found, return the corresponding object
#     if i != len(sub_list.original) and sub_list.original[i] == term:
#         return sub_list.substitution[i]
#     else:
#         return None

# def upload_pend(original, substitution, model):
#     # Add the sub if not already there
#     pend, created = model.objects.get_or_create(
#         original=original
#     )

#     # If a new entry was created, add the substitution
#     if created:
#         pend.substitution = substitution
#         pend.save()

# def remove_extra_white_space(txt):
#     """Removes any consecutive white space characters"""
#     return re.sub(r"\s{2,}", " ", txt)

# def correct_leading_decimal(txt):
#     """Adds a leading zero to a decimal if needed"""
#     # TO FIX: regex is incorrect and grabing the first character
#     # of every string
#     #return re.sub(r"^.", "0.", txt)

#     return txt


# # MORE FIELD SPECIFIC CORRECTIONS/CONVERSIONS
# def convert_integer(txt):
#     """Converts the provided text to an integer"""
#     try:
#         return int(txt)
#     except ValueError:
#         # Attempt to handle a BOM if encoding is incorrect
#         try:
#             return int(txt[2:-1])
#         except Exception:
#             log.error(
#                 "Unable to convert {} to integer".format(txt),
#                 exc_info=True
#             )

#             return 0
#     except Exception:
#         log.error(
#             "Unable to convert {} to integer".format(txt),
#             exc_info=True
#         )

#         return 0

# def convert_boolean(txt, yes):
#     """Converts provided text to boolean, based on the yes value"""
#     if txt.upper() == yes.upper():
#         return True
#     else:
#         return False

# def convert_date(txt):
#     """Converts the provided text to a date object"""
#     months = {
#         "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
#         "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
#     }

#     if re.search(r"^\d{2}-[a-zA-Z]{3}-\d{4}$", txt):
#         parts = txt.split("-")

#         day = int(parts[0])
#         month = months[parts[1]]
#         year = int(parts[2])

#         return date(year, month, day)
#     else:
#         return None

# def correct_ahfs(txt, sub_data):
#     """Corrects the formatting of the AHFS description"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubAHFSPend)

#         return sub

# def correct_brand_name(txt, sub_data):
#     """Correct the formatting of brand names"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubBrandPend)

#         return sub

# def correct_company_name(txt, sub_data):
#     """Correct the formatting of company names"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubCompanyNamePend)

#         return sub

# def correct_company_type(txt):
#     """Correct the formatting of company types"""
#     sub = titlecase(txt)
#     sub = sub.replace("Din", "DIN")

#     return sub

# def correct_dosage(txt):
#     # Correcting a missing leading zero
#     txt = correct_leading_decimal(txt)

#     return txt

# def correct_descriptor(txt, sub_data):
#     """Correct the formatting of descriptors"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = sub.lower()

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubDescriptorPend)

#         return sub

# def correct_din(txt):
#     if txt.upper() == "NOT APPLICABLE/NON APPLICABLE":
#         return "N/A"
#     else:
#         return txt

# def correct_ingredient(txt, sub_data):
#     """Correct the formatting of ingredients"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = sub.lower()

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubIngredientPend)

#         return sub

# def correct_pharmaceutical_std(txt, sub_data):
#     """Correct the formatting of pharmaceutical standards"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubPharmaceuticalStdPend)

#         return sub

# def correct_product_categorization(txt, sub_data):
#     """Correct the formatting of product categorization"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubProductCategorizationPend)

#         return sub

# def correct_route_of_administration(txt, sub_data):
#     """Correct the formatting of route of administration"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = sub.lower()

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubRouteOfAdministrationPend)

#         return sub

# def correct_street_name(txt, sub_data):
#     """Correct the formatting of street name"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubStreetNamePend)

#         return sub

# def correct_strength(txt):
#     # Correct a missing leading zero
#     txt = correct_leading_decimal(txt)

#     return txt

# def correct_suite_number(txt, sub_data):
#     """Correct the formatting of suite number"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubSuiteNumberPend)

#         return sub

# def correct_unit(txt, sub_data):
#     """Correct the formatting of unit"""
#     # Check if this item is in the substitution list
#     sub = binary_search(txt, sub_data)

#     if sub:
#         # Returns sub if present
#         return sub
#     else:
#         # Perform basic processing
#         sub = remove_extra_white_space(txt)
#         sub = titlecase(sub)

#         # Upload the to the pending sub model
#         upload_pend(txt, sub, SubUnitPend)

#         return sub

# def correct_upc(txt):
#     """Correct formatting of a UPC"""
#     sub = remove_extra_white_space(txt)

#     # Remove unneded characters
#     extra_chars = r"(\.|\+\+|2X\-)"
#     sub = re.sub(extra_chars, "", sub)

#     return sub
