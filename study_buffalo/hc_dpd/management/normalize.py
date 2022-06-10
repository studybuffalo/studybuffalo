# import logging

# from .normalization_functions import (
#     convert_integer, convert_boolean, convert_date, correct_ahfs,
#     correct_brand_name, correct_company_name, correct_company_type,
#     correct_dosage, correct_descriptor, correct_din, correct_ingredient,
#     correct_pharmaceutical_std, correct_product_categorization,
#     correct_route_of_administration, correct_street_name, correct_strength,
#     correct_suite_number, correct_unit, correct_upc
# )
# from .substitution_functions import Substitutions


# # Setup logging
# log = logging.getLogger(__name__)

# # Setup the Substitution data
# SUB_DATA = Substitutions()

# def normalize_active_ingredients(data):
#     """Normalizes the active ingredient entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "active_ingredient_code": item[1],
#             "ingredient": correct_ingredient(item[2], SUB_DATA.ingredient),
#             "ingredient_supplied_ind": item[3],
#             "strength": correct_strength(item[4]),
#             "strength_unit": correct_unit(item[5], SUB_DATA.unit),
#             "strength_type": item[6],
#             "dosage_value": correct_dosage(item[7]),
#             "base": convert_boolean(item[8], "Y"),
#             "dosage_unit": correct_unit(item[9], SUB_DATA.unit),
#             "notes": item[10],
#             "ingredient_f": item[11],
#             "strength_unit_f": item[12],
#             "strength_type_f": item[13],
#             "dosage_unit_f": item[14],
#         })

#     return normalized_data

# def normalize_companies(data):
#     """Normalizes the companies entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "mfr_code": item[1],
#             "company_code": convert_integer(item[2]),
#             "company_name": correct_company_name(item[3], SUB_DATA.company_name),
#             "company_type": correct_company_type(item[4]),
#             "address_mailing_flag": convert_boolean(item[5], "Y"),
#             "address_billing_flag": convert_boolean(item[6], "Y"),
#             "address_notification_flag": convert_boolean(item[7], "Y"),
#             "address_other": convert_boolean(item[8], "Y"),
#             "suite_number": correct_suite_number(item[9], SUB_DATA.suite_number),
#             "street_name": correct_street_name(item[10], SUB_DATA.street_name),
#             "city_name": item[11],
#             "province": item[12],
#             "country": item[13],
#             "postal_code": item[14],
#             "post_office_box": item[15],
#             "province_f": item[16],
#             "country_f": item[17],
#         })

#     return normalized_data

# def normalize_drug_product(data):
#     """Normalizes the drug product entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "product_categorization": correct_product_categorization(
#                 item[1], SUB_DATA.product_categorization
#             ),
#             "class_e": item[2],
#             "drug_identification_number": correct_din(item[3]),
#             "brand_name": correct_brand_name(item[4], SUB_DATA.brand_name),
#             "descriptor": correct_descriptor(item[5], SUB_DATA.descriptor),
#             "pediatric_flag": convert_boolean(item[6], "Y"),
#             "accession_number": item[7],
#             "number_of_ais": item[8],
#             "last_update_date": convert_date(item[9]),
#             "ai_group_no": item[10],
#             "class_f": item[11],
#             "brand_name_f": item[12],
#             "descriptor_f": item[13],
#         })

#     return normalized_data

# def normalize_form(data):
#     """Normalizes the form entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "pharm_form_code": convert_integer(item[1]),
#             "pharmaceutical_form": item[2],
#             "pharmaceutical_form_f": item[3],
#         })

#     return normalized_data

# def normalize_inactive_products(data):
#     """Normalizes the inactive products entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "drug_identification_number": correct_din(item[1]),
#             "brand_name": correct_brand_name(item[2], SUB_DATA.brand_name),
#             "history_date": convert_date(item[3]),
#         })

#     return normalized_data

# def normalize_packaging(data):
#     """Normalizes the packaging entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "upc": correct_upc(item[1]),
#             "package_size_unit": correct_unit(item[2], SUB_DATA.unit),
#             "package_type": item[3],
#             "package_size": item[4],
#             "product_information": item[5],
#             "package_size_unit_f": item[6],
#             "package_type_f": item[7],
#         })

#     return normalized_data

# def normalize_pharmaceutical_standard(data):
#     """Normalizes the pharmaceutical standard entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "pharmaceutical_std": correct_pharmaceutical_std(
#                 item[1], SUB_DATA.pharmaceutical_std
#             ),
#         })

#     return normalized_data

# def normalize_route(data):
#     """Normalizes the route entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "route_of_administration_code": convert_integer(item[1]),
#             "route_of_administration": correct_route_of_administration(
#                 item[2], SUB_DATA.route_of_administration
#             ),
#             "route_of_administration_f": item[3],
#         })

#     return normalized_data

# def normalize_schedule(data):
#     """Normalizes the schedule entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "schedule": item[1],
#             "schedule_f": item[2],
#         })

#     return normalized_data

# def normalize_status(data):
#     """Normalizes the status entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "current_status_flag": convert_boolean(item[1], "Y"),
#             "status": item[2],
#             "history_date": convert_date(item[3]),
#             "status_f": item[4],
#             "lot_number": item[5],
#             "expiration_date": convert_date(item[6]),
#         })

#     return normalized_data

# def normalize_therapeutic_class(data):
#     """Normalizes the therapeutic class entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "tc_atc_number": item[1],
#             "tc_atc": item[2],
#             "tc_ahfs_number": item[3],
#             "tc_ahfs": correct_ahfs(item[4], SUB_DATA.ahfs),
#             "tc_atc_f": item[5],
#             "tc_ahfs_f": item[6],
#         })

#     return normalized_data

# def normalize_veterinary_status(data):
#     """Normalizes the veterinary status entries"""
#     normalized_data = []

#     # Cycle through each entry
#     for item in data:
#         normalized_data.append({
#             "drug_code": convert_integer(item[0]),
#             "vet_species": item[1],
#             "vet_sub_species": item[2],
#             "vet_species_f": item[3],
#         })

#     return normalized_data

# def normalize_entries(data, model):
#     """Normalizes the data based on the provided model"""
#     log.debug("Normalizing {}".format(model))

#     normalized_data = None

#     # ActiveIngredient
#     if model == "ActiveIngredients":
#         normalized_data = normalize_active_ingredients(data)

#     # Companies
#     elif model == "Companies":
#         normalized_data = normalize_companies(data)

#     # DrugProduct
#     elif model == "DrugProduct":
#         normalized_data = normalize_drug_product(data)

#     # Form
#     elif model == "Form":
#         normalized_data = normalize_form(data)

#     # InactiveProducts
#     elif model == "InactiveProducts":
#         normalized_data = normalize_inactive_products(data)

#     # Packaging
#     elif model == "Packaging":
#         normalized_data = normalize_packaging(data)

#     # PharmaceuticalStandard
#     elif model == "PharmaceuticalStandard":
#         normalized_data = normalize_pharmaceutical_standard(data)

#     # Route
#     elif model == "Route":
#         normalized_data = normalize_route(data)

#     # Schedule
#     elif model == "Schedule":
#         normalized_data = normalize_schedule(data)

#     # Status
#     elif model == "Status":
#         normalized_data = normalize_status(data)

#     # TherapeuticClass
#     elif model == "TherapeuticClass":
#         normalized_data = normalize_therapeutic_class(data)

#     # VeterinarySpecies
#     elif model == "VeterinarySpecies":
#         normalized_data = normalize_veterinary_status(data)

#     return normalized_data

# def normalize_data(dpd_data):
#     """Normalizes the extracted dpd data"""
#     # Cycle through each extension
#     for extension_key, extension in dpd_data.items():
#         log.debug("Normalizing {} files".format(extension_key))

#         # Cycle through each data file
#         for file_key, file in extension.items():
#             # Convert the data to a dictionary and normalize the entries
#             file["data"] = normalize_entries(file["data"], file["model"])

#     return dpd_data
