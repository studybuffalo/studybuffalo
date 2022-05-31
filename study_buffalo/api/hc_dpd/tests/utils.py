"""Utility functions for testing."""
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from hc_dpd.models import DPD


# A complete set of data for original data upload (includes all file
# types & fields)
UPLOAD_ALL_DATA = {
    'active_ingredient': [
        {
            'drug_code': 1,
            'active_ingredient_code': 'A',
            'ingredient': 'B',
            'ingredient_supplied_ind': 'C',
            'strength': 'D',
            'strength_unit': 'E',
            'strength_type': 'F',
            'dosage_value': 'G',
            'base': 'H',
            'dosage_unit': 'I',
            'notes': 'J',
            'ingredient_f': 'K',
            'strength_unit_f': 'L',
            'strength_type_f': 'M',
            'dosage_unit_f': 'N',
        },
    ],
    'biosimilar': [
        {
            'drug_code': 1,
            'biosimilar_code': 2,
            'biosimilar_type': 'A',
            'biosimilar_type_f': 'B',
        },
    ],
    'company': [
        {
            'drug_code': 1,
            'mfr_code': 'A',
            'company_code': 2,
            'company_name': 'B',
            'company_type': 'C',
            'address_mailing_flag': 'D',
            'address_billing_flag': 'E',
            'address_notification_flag': 'F',
            'address_other': 'G',
            'suite_number': 'H',
            'street_name': 'I',
            'city_name': 'J',
            'province': 'K',
            'country': 'L',
            'postal_code': 'M',
            'post_office_box': 'N',
            'province_f': 'O',
            'country_f': 'P',
        },
    ],
    'drug_product': [
        {
            'drug_code': 1,
            'product_categorization': 'A',
            'class_e': 'B',
            'drug_identification_number': 'C',
            'brand_name': 'D',
            'descriptor': 'E',
            'pediatric_flag': 'F',
            'accession_number': 'G',
            'number_of_ais': 'H',
            'last_update_date': '2000-01-01',
            'ai_groupd_no': 'I',
            'class_f': 'J',
            'brand_name_f': 'K',
            'descriptor_f': 'L',
        },
    ],
    'form': [
        {
            'drug_code': 1,
            'pharm_form_code': 2,
            'pharmacuetical_form': 'A',
            'pharmaceutical_form_f': 'B',
        },
    ],
    'inactive_product': [
        {
            'drug_code': 1,
            'drug_identification_number': 'A',
            'brand_name': 'B',
            'history_date': '2000-01-01',
        },
    ],
    'packaging': [
        {
            'drug_code': 1,
            'upc': 'A',
            'package_size_unit': 'B',
            'package_type': 'C',
            'product_information': 'D',
            'package_size_unit_f': 'E',
            'package_type_f': 'F',
        },
    ],
    'pharmaceutical_standard': [
        {
            'drug_code': 1,
            'pharmaceutical_std': 'A',
        },
    ],
    'route': [
        {
            'drug_code': 1,
            'route_of_administration_code': 2,
            'route_of_admistration': 'A',
            'route_of_administration_f': 'B',
        },
    ],
    'schedule': [
        {
            'drug_code': 1,
            'schedule': 'A',
            'schedule_f': 'B',
        },
    ],
    'status': [
        {
            'drug_code': 1,
            'current_status_flag': 'A',
            'status': 'B',
            'history_date': '2000-01-01',
            'status_f': 'C',
            'lot_number': 'D',
            'expiration_date': '2001-01-01',
        },
    ],
    'therapeutic_class': [
        {
            'drug_code': 1,
            'tc_atc_number': 'A',
            'tc_atc': 'B',
            'tc_atc_f': 'C',
        },
    ],
    'veterinary_species': [
        {
            'drug_code': 1,
            'vet_species': 'A',
            'vet_sub_species': 'B',
            'vet_species_f': 'C',
        },
    ],
}


def add_api_view_permission(user):
    """Adds the 'api_view' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(DPD)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='api_view')
    )


def add_api_edit_permission(user):
    """Adds the 'api_edit' permission to the provided user."""
    content_type = ContentType.objects.get_for_model(DPD)
    user.user_permissions.add(
        Permission.objects.get(content_type=content_type, codename='api_edit')
    )
