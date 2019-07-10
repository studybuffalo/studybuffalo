"""Functions to parse iDBL data for insertion into database."""
import re

from sentry_sdk import capture_message
from drug_price_calculator import models


def parse_bsrf(bsrf):
    """Parses the raw Brand Name, Strength, Routh, Dosage Form data."""
    # Get substitution or create pending model
    try:
        sub = models.SubsBSRF.objects.get(bsrf=bsrf)
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
        try:
            text = bsrf.split('   ')

            brand_strength = text[0].strip()
            route = text[1].strip()
            dosage_form = text[2].strip()
        except IndexError:
            capture_message(
                message='Error processing "{}"'.format(bsrf), level=30
            )

            brand_strength = bsrf
            route = None
            dosage_form = None

    # Format: B S    F
    elif re.search(match4, bsrf):
        try:
            text = bsrf.split('    ')

            brand_strength = text[0].strip()
            route = None
            dosage_form = text[1].strip()
        except IndexError:
            capture_message(
                message='Error processing "{}"'.format(bsrf), level=30
            )

            brand_strength = bsrf
            route = None
            dosage_form = None

    # Format: B S   F   or   B R   F
    # Note: cannot properly extract the B R   F cases
    elif re.search(match3, bsrf):
        try:
            text = bsrf.split('   ')

            brand_strength = text[0].strip()
            route = None
            dosage_form = text[1].strip()
        except IndexError:
            capture_message(
                message='Error processing "{}"'.format(bsrf), level=30
            )

            brand_strength = bsrf
            route = None
            dosage_form = None

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
    generic = re.sub(r'\s{2,}', ' ', generic)

    # Remove spaces around slashes
    generic = re.sub(r'/\s', '/', generic)

    # Add data to pend if present
    if pend:
        pend.correction = generic
        pend.save()

    return generic

def parse_manufacturer(manufacturer):
    return ''

def parse_unit_of_issue(unit_issue):
    return ''

def _parse_brand_name(text):
    """Properly formats the brand name"""
    # Convert to title text
    text = text.title()

    # Removes extra space characters
    text = re.sub(r'\s{2,}', ' ', text)

    # Correct errors with apostrophes and 's'
    text = re.sub(r"'S\b'", "'s", text)

    return text

def _parse_strength(text):
    """Manually corrects errors not fixed by .lower()."""
    # Converts the strength to lower case
    text = text.lower()

    # Removes any extra spaces
    text = re.sub(r'\s{2,}', ' ', text)

    # Remove any spaces around slashes
    text = re.sub(r'\s/\s', '/', text)

    # Remove any spaces between numbers and %
    text = re.sub(r'\s%', '%', text)

    # Get substitution model for units
    try:
        unit_subs = models.SubsUnit.objects.all()
    except models.SubsUnit.DoesNotExist:
        unit_subs = []

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
