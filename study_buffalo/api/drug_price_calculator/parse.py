"""Functions to parse iDBL data for insertion into database."""
import re

from sentry_sdk import capture_message
from drug_price_calculator import models

def _remove_extra_white_space(text):
    """Removes extra whitespace within text."""
    return re.sub(r'\s{2,}', ' ', text)

def _remove_slash_white_space(text):
    """Removes white spaces from around slashes."""
    return re.sub(r'(\s/\s|/\s|\s/)', '/', text)

def _convert_to_title_case(text):
    """Handles conversion of string to title case."""
    # Convert to title text
    text = text.title()

    # Correct errors with apostrophes and 's'
    text = re.sub(r"'S\b", "'s", text)

    return text

def _parse_brand_name(text):
    """Properly formats the brand name"""
    # Convert to title text
    text = _convert_to_title_case(text)

    # Removes extra space characters
    text = _remove_extra_white_space(text)

    # Remove extra spaces around slashes
    text = _remove_slash_white_space(text)

    return text

def _parse_strength(text):
    """Properly formats strength."""
    # Converts the strength to lower case
    text = text.lower()

    # Removes any extra spaces
    text = _remove_extra_white_space(text)

    # Remove any spaces around slashes
    text = _remove_slash_white_space(text)

    # Remove any spaces between numbers and %
    text = re.sub(r'\s%', '%', text)

    # Get substitution model for units
    unit_subs = models.SubsUnit.objects.all()

    # Apply any substitutions
    for sub in unit_subs:
        text = re.sub(r'\b%s\b' % sub.original, sub.correction, text)

    return text

def _parse_route(text):
    """Properly formats the route"""
    # Convert route to lower case
    text = text.lower()

    return text

def _parse_dosage_form(text):
    """Properly formats the dosage form"""
    # Convert route to lower case
    text = text.lower()

    return text

def parse_bsrf(raw_bsrf):
    """Parses the raw Brand Name, Strength, Routh, Dosage Form data."""
    # Check if there is a value to parse
    if not raw_bsrf:
        return {
            'brand_name': None,
            'strength': None,
            'route': None,
            'dosage_form': None,
        }

    # Remove white space
    bsrf = raw_bsrf.strip()

    # Get substitution or create pending model
    try:
        sub = models.SubsBSRF.objects.get(original=bsrf)
        pend = None
    except models.SubsBSRF.DoesNotExist:
        sub = None
        pend, _ = models.PendBSRF.objects.get_or_create(original=bsrf)

    if sub:
        return {
            'brand_name': sub.brand_name,
            'strength': sub.strength,
            'route': sub.route,
            'dosage_form': sub.dosage_form,
        }

    # Splits text multiple strings depending on the format used
    # Formats vary with number of white space between sections
    match3 = r'\S\s{3}\S'
    match4 = r'\S\s{4}\S'

    # Format: B S    R   F
    if re.search(match4, bsrf) and re.search(match3, bsrf):
        text = bsrf.split('   ')

        brand_strength = text[0].strip()
        route = text[1].strip()
        dosage_form = text[2].strip()

    # Format: B S    F
    elif re.search(match4, bsrf):
        text = bsrf.split('    ')

        brand_strength = text[0].strip()
        route = None
        dosage_form = text[1].strip()

    # Format: B S   F   or   B R   F
    #   Note: cannot properly extract the "B R   F" cases and these
    #         will be improperly formatted intentionally
    elif re.search(match3, bsrf):
        text = bsrf.split('   ')

        brand_strength = text[0].strip()
        route = None
        dosage_form = text[1].strip()

    # Format: B S
    else:
        # B S
        brand_strength = bsrf
        route = None
        dosage_form = None

    # Splits the brand_strength at the first number
    # encountered with a non-numeric character behind it
    # (excluding commas in numbers, as this is assumed
    # to be a unit)
    search = re.search(r'\s\b[0-9,]+\D+', brand_strength)

    if search:
        split = search.start()

        brand_name = brand_strength[:split].strip()
        strength = brand_strength[split:].strip()
    else:
        brand_name = brand_strength
        strength = None

    # Apply final corrections to extracted information
    if brand_name:
        brand_name = _parse_brand_name(brand_name)

    if strength:
        strength = _parse_strength(strength)

    if route:
        route = _parse_route(route)

    if dosage_form:
        dosage_form = _parse_dosage_form(dosage_form)

    # If this is a new BSRF, add the data to the pending model
    if pend:
        pend.brand_name = brand_name
        pend.strength = strength
        pend.route = route
        pend.dosage_form = dosage_form
        pend.save()

    return {
        'brand_name': brand_name,
        'strength': strength,
        'route': route,
        'dosage_form': dosage_form,
    }

def parse_generic(raw_generic):
    """Parses generic names."""
    # Check if there is a value to parse
    if not raw_generic:
        return None

    # Remove any extra white space
    original = raw_generic.strip()

    # Get substitution or create pending model
    try:
        sub = models.SubsGeneric.objects.get(original=original)
        pend = None
    except models.SubsGeneric.DoesNotExist:
        sub = None
        pend, _ = models.PendGeneric.objects.get_or_create(original=original)

    # If subsitution present, return corrected value
    if sub:
        return sub.correction

    # Otherwise apply regular processing
    # Convert to lower case
    generic = original.lower()

    # Removes extra space characters
    generic = _remove_extra_white_space(generic)

    # Remove spaces around slashes
    generic = _remove_slash_white_space(generic)

    # Add data to pend if present
    if pend:
        pend.correction = generic
        pend.save()

    return generic

def parse_manufacturer(raw_manufacturer):
    """Parses drug manufacturers."""
    # Check if there is a value to parse
    if not raw_manufacturer:
        return None

    # Remove any extra white space
    original = raw_manufacturer.strip()

    # Get substitution or create pending model
    try:
        sub = models.SubsManufacturer.objects.get(original=original)
        pend = None
    except models.SubsManufacturer.DoesNotExist:
        sub = None
        pend, _ = models.PendManufacturer.objects.get_or_create(original=original)

    # If subsitution present, return corrected value
    if sub:
        return sub.correction

    # Otherwise apply regular processing
    # Convert to title text
    manufacturer = _convert_to_title_case(original)

    # Removes extra space characters
    manufacturer = _remove_extra_white_space(manufacturer)

    # Add data to pend if present
    if pend:
        pend.correction = manufacturer
        pend.save()

    return manufacturer

def parse_unit_issue(raw_unit_issue):
    """Parses the unit of issue."""
    # Check if there is a value to parse
    if not raw_unit_issue:
        return None

    # Remove any extra white space
    original = raw_unit_issue.strip()

    # Get substitution or create pending model
    try:
        sub = models.SubsUnit.objects.get(original=original)
        pend = None
    except models.SubsUnit.DoesNotExist:
        sub = None
        pend, _ = models.PendUnit.objects.get_or_create(original=original)

    # If subsitution present, return corrected value
    if sub:
        return sub.correction

    # Otherwise apply regular processing
    # Change to lower case
    unit = original.lower()

    # Add data to pend if present
    if pend:
        pend.correction = unit
        pend.save()

    return unit

def assemble_generic_product(bsrf, generic_name):
    """Assembles a generic product name."""
    description = []

    if bsrf['strength']:
        description.append(bsrf['strength'])

    if bsrf['route']:
        description.append(bsrf['route'])

    if bsrf['dosage_form']:
        description.append(bsrf['dosage_form'])

    if description:
        return '{} ({})'.format(generic_name, ' '.join(description))

    return generic_name
