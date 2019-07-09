"""Functions to parse iDBL data for insertion into database."""
import re


def parse_bsrf(bsrf):
    """
    # Checks if the text has a substitution
    # Remove extra white space from searchText
    searchText = re.sub(r'\s{2,}', ' ', text)
    sub = binary_search(searchText, bsrfSubs)

    if sub:
        brandName = sub.brandName
        strength = sub.strength
        route = sub.route
        dosageForm = sub.dosageForm
        matched = True

    # If no substitution, apply regular processing
    else:
        # Splits text multiple strings depending on the format
        # used
        # Formats vary with number of white space between
        # sections
        match3 = r'\S\s{3}\S'
        match4 = r'\S\s{4}\S'

        # Format: B S    R   F
        if re.search(match4, text) and re.search(match3, text):
            try:
                text = text.split('   ')

                brandStrength = text[0].strip()
                route = text[1].strip()
                dosageForm = text[2].strip()
            except Exception:
                log.critical('URL %s: Error extracting BSRF', url)

                brandStrength = text
                route = None
                dosageForm = None

        # Format: B S    F
        elif re.search(match4, text):
            try:
                text = text.split('    ')

                brandStrength = text[0].strip()
                route = None
                dosageForm = text[1].strip()
            except Exception:
                log.critical(
                    'URL %s: Error extracting 4 space BSF', url
                )

                brandStrength = text
                route = None
                dosageForm = None

        # Format: B S   F   or   B R   F
        # Note: cannot properly extract the B R   F cases
        elif re.search(match3, text):
            try:
                text = text.split('   ')

                brandStrength = text[0].strip()
                route = None
                dosageForm = text[1].strip()
            except Exception:
                log.critical(
                    'URL %s: Error extracting 3 space BSF', url
                )

                brandStrength = text
                route = None
                dosageForm = None

        # Format: B S
        else:
            # B S
            brandStrength = text
            route = None
            dosageForm = None

        # Splits the brandStrength at the first number
        # encountered with a non-numeric character behind it
        # (excluding commas in numbers, as this is assumed
        # to be a unit)
        search = re.search(r'\s\b[0-9,]+\D+', brandStrength)

        if search:
            split = search.start()

            brandName = brandStrength[:split].strip()
            strength = brandStrength[split:].strip()
        else:
            brandName = brandStrength
            strength = None

        # Apply final corrections to extracted information
        if brandName:
            brandName = parse_brand_name(brandName)

        if strength:
            strength = parse_strength(strength)

        if route:
            route = parse_route(route)

        if dosageForm:
            dosageForm = parse_dosage_form(dosageForm)

        # Flags html as not having sub match
        matched = False


    output = BSRF(brandName, strength, route, dosageForm,
                  searchText, matched)

    return output
    """
    return {
        'brand_name': '',
        'strength': '',
        'route': '',
        'dosage_form': '',
    }

def parse_generic(generic):
    """
        # Remove parenthesis
        original = text[1:len(text) - 1]

        # Check if this text has a substitution
        sub = binary_search(original, subs)

        # If there is a sub, apply it
        if sub:
            generic = sub
            matched = True

        # Otherwise apply regular processing
        else:
            # Convert to lower case
            generic = original.lower()

            # Removes extra space characters
            generic = re.sub(r'\s{2,}', ' ', generic)

            # Remove spaces around slashes
            generic = re.sub(r'/\s', '/', generic)

            matched = False

        return Generic(generic, original, matched)

    try:
        genericText = html.find_all('tr', class_='idblTable')[2]\
                            .td.div.string.strip()

        generic = parse_generic(genericText)
    except:
        log.critical('URL %s: unable to extract generic name' % url)
    """

    return ''

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

    # Applies any remaining corrections
    unit_subs = [] # TODO: fix this
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
