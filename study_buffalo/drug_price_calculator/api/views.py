
# def parse_brand_name(text):
#     """Properly formats the brand name"""
#     # Convert to title text
#     text = text.title()

#     # Removes extra space characters
#     text = re.sub(r'\s{2,}', ' ', text)

#     # Correct errors with apostrophes and 's'
#     text = re.sub(r"'S\b'", "'s", text)

#     return text

# def parse_strength(text):
#     """Manually corrects errors not fixed by .lower()."""

#     # Converts the strength to lower case
#     text = text.lower()

#     # Removes any extra spaces
#     text = re.sub(r'\s{2,}', ' ', text)

#     # Remove any spaces around slashes
#     text = re.sub(r'\s/\s', '/', text)

#     # Remove any spaces between numbers and %
#     text = re.sub(r'\s%', '%', text)

#     # Applies any remaining corrections
#     for sub in unitSubs:
#         text = re.sub(r'\b%s\b' % sub.original, sub.correction, text)

#     return text

# def parse_route(text):
#     """Properly formats the route"""

#     # Convert route to lower case
#     text = text.lower()

#     return text

# def parse_dosage_form(text):
#     """Properly formats the dosage form"""

#     # Convert route to lower case
#     text = text.lower()

#     return text

# def split_brand_strength_route_form(text):
#     """Extracts brand name, strength, route, dosage form"""

#     # Checks if the text has a substitution
#     # Remove extra white space from searchText
#     searchText = re.sub(r'\s{2,}', ' ', text)
#     sub = binary_search(searchText, bsrfSubs)

#     if sub:
#         brandName = sub.brandName
#         strength = sub.strength
#         route = sub.route
#         dosageForm = sub.dosageForm
#         matched = True

#     # If no substitution, apply regular processing
#     else:
#         # Splits text multiple strings depending on the format
#         # used
#         # Formats vary with number of white space between
#         # sections
#         match3 = r'\S\s{3}\S'
#         match4 = r'\S\s{4}\S'

#         # Format: B S    R   F
#         if re.search(match4, text) and re.search(match3, text):
#             try:
#                 text = text.split('   ')

#                 brandStrength = text[0].strip()
#                 route = text[1].strip()
#                 dosageForm = text[2].strip()
#             except Exception:
#                 log.critical('URL %s: Error extracting BSRF', url)

#                 brandStrength = text
#                 route = None
#                 dosageForm = None

#         # Format: B S    F
#         elif re.search(match4, text):
#             try:
#                 text = text.split('    ')

#                 brandStrength = text[0].strip()
#                 route = None
#                 dosageForm = text[1].strip()
#             except Exception:
#                 log.critical(
#                     'URL %s: Error extracting 4 space BSF', url
#                 )

#                 brandStrength = text
#                 route = None
#                 dosageForm = None

#         # Format: B S   F   or   B R   F
#         # Note: cannot properly extract the B R   F cases
#         elif re.search(match3, text):
#             try:
#                 text = text.split('   ')

#                 brandStrength = text[0].strip()
#                 route = None
#                 dosageForm = text[1].strip()
#             except Exception:
#                 log.critical(
#                     'URL %s: Error extracting 3 space BSF', url
#                 )

#                 brandStrength = text
#                 route = None
#                 dosageForm = None

#         # Format: B S
#         else:
#             # B S
#             brandStrength = text
#             route = None
#             dosageForm = None

#         # Splits the brandStrength at the first number
#         # encountered with a non-numeric character behind it
#         # (excluding commas in numbers, as this is assumed
#         # to be a unit)
#         search = re.search(r'\s\b[0-9,]+\D+', brandStrength)

#         if search:
#             split = search.start()

#             brandName = brandStrength[:split].strip()
#             strength = brandStrength[split:].strip()
#         else:
#             brandName = brandStrength
#             strength = None

#         # Apply final corrections to extracted information
#         if brandName:
#             brandName = parse_brand_name(brandName)

#         if strength:
#             strength = parse_strength(strength)

#         if route:
#             route = parse_route(route)

#         if dosageForm:
#             dosageForm = parse_dosage_form(dosageForm)

#         # Flags html as not having sub match
#         matched = False


#     output = BSRF(brandName, strength, route, dosageForm,
#                   searchText, matched)

#     return output

# try:
#     bsrf = html.find_all('tr', class_='idblTable')[1]\
#                .td.div.string.strip()
# except:
#     log.critical('URL %s: unable to extract BSRF string' % url)

# bsrf = split_brand_strength_route_form(bsrf)




# def parse_generic(text):
        #     """Correct formatting of generic name to be lowercase"""
        #     # Remove parenthesis
        #     original = text[1:len(text) - 1]

        #     # Check if this text has a substitution
        #     sub = binary_search(original, subs)

        #     # If there is a sub, apply it
        #     if sub:
        #         generic = sub
        #         matched = True

        #     # Otherwise apply regular processing
        #     else:
        #         # Convert to lower case
        #         generic = original.lower()

        #         # Removes extra space characters
        #         generic = re.sub(r'\s{2,}', ' ', generic)

        #         # Remove spaces around slashes
        #         generic = re.sub(r'/\s', '/', generic)

        #         matched = False

        #     return Generic(generic, original, matched)

        # try:
        #     genericText = html.find_all('tr', class_='idblTable')[2]\
        #                       .td.div.string.strip()

        #     generic = parse_generic(genericText)
        # except:
        #     log.critical('URL %s: unable to extract generic name' % url)




        # def parse_atc(text):
        #     """Splits text into a list containing ATC codes and titles."""
        #     atcList  = []

        #     # The regex matches to extract specific content
        #     searchList = [
        #         # Level 1: Anatomical Main Group
        #         r'([a-zA-Z]).*$',

        #         # Level 2: Therapeutic Subgroup
        #         r'([a-zA-Z]\d\d).*$',

        #         # Level 3: Pharmacological Subgroup
        #         r'([a-zA-Z]\d\d[a-zA-Z]).*$',

        #         # Level 4: Chemical Subgroup
        #         r'([a-zA-Z]\d\d[a-zA-Z][a-zA-Z]).*$',

        #         # Level 5: Chemical Substance
        #         r'([a-zA-Z]\d\d[a-zA-Z][a-zA-Z]\d\d)*$'
        #     ]

        #     for search in searchList:
        #         match = re.match(search, text)

        #         if match:
        #             code = match.group(1)
        #             description = binary_search(code, descriptions)
        #         else:
        #             code = None
        #             description = None

        #         atcList.append(code)
        #         atcList.append(description)

        #     return atcList

        # try:
        #     atcText = html.find_all('tr', class_='idblTable')[10]\
        #               .find_all('td')[1].string.strip()
        #     atcList = parse_atc(atcText)
        #     atc = ATC(atcList, atcText)
        # except:
        #     log.critical('URL %s: unable to extract ATC' % url)
