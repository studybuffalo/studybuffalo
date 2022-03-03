"""Tests for Drug Price Calculator API parse functions."""
# pylint: disable=protected-access
import pytest

from api.drug_price_calculator import parse
from drug_price_calculator import models


pytestmark = pytest.mark.django_db

def test__remove_extra_white_space__with_extra_white_space():
    """Tests _remove_extra_white_space handles extra white space."""
    output = parse._remove_extra_white_space('a   a    a')

    assert output == 'a a a'

def test__remove_extra_white_space__without_extra_white_space():
    """Tests _remove_extra_white_space handles already correct strings."""
    output = parse._remove_extra_white_space('a a a')

    assert output == 'a a a'

def test__remove_slash_white_space__with_extra_white_space():
    """Tests _remove_slash_white_space handles extra white space."""
    output = parse._remove_slash_white_space('a / a a')
    assert output == 'a/a a'

    output = parse._remove_slash_white_space('a/ a a')
    assert output == 'a/a a'

    output = parse._remove_slash_white_space('a /a a')
    assert output == 'a/a a'

def test__remove_slash_white_space__without_extra_white_space():
    """Tests _remove_slash_white_space handles already correct strings."""
    output = parse._remove_slash_white_space('a/a a')

    assert output == 'a/a a'

def test__convert_to_title_case__normal():
    """Tests _convert_to_title_case handles normal situations."""
    output = parse._convert_to_title_case('aaa BBB')
    assert output == 'Aaa Bbb'

def test__convert_to_title_case__with_apostrophe():
    """Tests _convert_to_title_case handles words with "'s"."""
    output = parse._convert_to_title_case('aaa\'s BBB\'s')
    assert output == 'Aaa\'s Bbb\'s'

def test__parse_brand_name__normal():
    """Tests _parse_brand_name handling of normal string."""
    output = parse._parse_brand_name('AaA')

    assert output == 'Aaa'

def test__parse_strength__normal():
    """Tests _parse_strength handling of normal string."""
    output = parse._parse_strength('AaA')

    assert output == 'aaa'

def test__parse_strength__with_percent():
    """Tests _parse_strength handling of % in string."""
    output = parse._parse_strength('AaA %')

    assert output == 'aaa%'

def test__parse_strength__with_unit_sub():
    """Tests _parse_strength handling of % in string."""
    models.SubsUnit.objects.create(original='ml', correction='mL')
    output = parse._parse_strength('AaA 5 ml')

    assert output == 'aaa 5 mL'

def test__parse_route__normal():
    """Tests _parse_route handling of normal string."""
    output = parse._parse_route('AaA')

    assert output == 'aaa'

def test__parse_dosage_form__normal():
    """Tests _parse_dosage_form handling of normal string."""
    output = parse._parse_dosage_form('AaA')

    assert output == 'aaa'

def test__parse_bsrf__valid__with_sub():
    """Tests for proper parse handling with valid data and a sub."""
    models.SubsBSRF.objects.create(
        original='b s r f', brand_name='b', strength='s', route='r', dosage_form='f'
    )

    output = parse.parse_bsrf('b s r f')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'b'
    assert output['strength'] == 's'
    assert output['route'] == 'r'
    assert output['dosage_form'] == 'f'

def test__parse_bsrf__output_without_sub():
    """Tests for output format without substitution."""
    output = parse.parse_bsrf('a')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

def test__parse_bsrf__valid__b_s____r__f():
    """Tests handling of "B S    R   F" formatted string."""
    output = parse.parse_bsrf('b 1 mg    r   f')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B'
    assert output['strength'] == '1 mg'
    assert output['route'] == 'r'
    assert output['dosage_form'] == 'f'

def test__parse_bsrf__valid__b_s____f():
    """Tests handling of "B S    F" formatted string."""
    output = parse.parse_bsrf('b 1 mg    f')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B'
    assert output['strength'] == '1 mg'
    assert output['route'] is None
    assert output['dosage_form'] == 'f'

def test__parse_bsrf__valid__b_s___f():
    """Tests handling of "B S   F" formatted string."""
    output = parse.parse_bsrf('b 1 mg   f')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B'
    assert output['strength'] == '1 mg'
    assert output['route'] is None
    assert output['dosage_form'] == 'f'

def test__parse_bsrf__valid__b_s():
    """Tests handling of "B S" formatted string."""
    output = parse.parse_bsrf('b 1 mg')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B'
    assert output['strength'] == '1 mg'
    assert output['route'] is None
    assert output['dosage_form'] is None

def test__parse_bsrf__valid__b():
    """Tests handling of "B" formatted string."""
    output = parse.parse_bsrf('b')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B'
    assert output['strength'] is None
    assert output['route'] is None
    assert output['dosage_form'] is None

def test__parse_bsrf__valid__b__with_spaces():
    """Tests handling of "B" formatted string with spaces in brand name."""
    output = parse.parse_bsrf('b b1 b2')

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] == 'B B1 B2'
    assert output['strength'] is None
    assert output['route'] is None
    assert output['dosage_form'] is None

def test__parse_bsrf__pend_created():
    """Tests that PendBSRF is properly created for new raw_string."""
    parse.parse_bsrf('b 1 mg    r   f')
    pend = models.PendBSRF.objects.get(original='b 1 mg    r   f')

    assert pend.brand_name == 'B'
    assert pend.strength == '1 mg'
    assert pend.route == 'r'
    assert pend.dosage_form == 'f'

def test__parse_bsrf__no_raw_bsrf():
    """Tests handling of a blank raw_bsrf."""
    output = parse.parse_bsrf(None)

    assert 'brand_name' in output
    assert 'strength' in output
    assert 'route' in output
    assert 'dosage_form' in output

    assert output['brand_name'] is None
    assert output['strength'] is None
    assert output['route'] is None
    assert output['dosage_form'] is None

def test__parse_generic__valid__with_sub():
    """Tests for proper parse handling with valid data and a sub."""
    models.SubsGeneric.objects.create(original='AAA', correction='aaa')

    output = parse.parse_generic('AAA')

    assert output == 'aaa'

def test__parse_generic__output_without_sub():
    """Tests for output format without substitution."""
    output = parse.parse_generic('AAA')

    assert output == 'aaa'

def test__parse_generic__pend_created():
    """Tests PendGeneric is properly created for new raw_string."""
    parse.parse_generic('AAA')
    pend = models.PendGeneric.objects.get(original='AAA')

    assert pend.correction == 'aaa'

def test__parse_generic__no_sub__converts_to_lower():
    """Tests parse_generic converts to lower case when no sub."""
    output = parse.parse_generic('AaA')

    assert output == 'aaa'

def test__parse_generic__no_raw_generic():
    """Tests output with blank raw_generic."""
    output = parse.parse_generic(None)

    assert output is None

def test__parse_manufacturer__valid__with_sub():
    """Tests for proper parse handling with valid data and a sub."""
    models.SubsManufacturer.objects.create(original='AAA', correction='aaa')

    output = parse.parse_manufacturer('AAA')

    assert output == 'aaa'

def test__parse_manufacturer__output_without_sub():
    """Tests for output format without substitution."""
    output = parse.parse_manufacturer('AAA')

    assert output == 'Aaa'

def test__parse_manufacturer__pend_created():
    """Tests PendManufacturer is properly created for new raw_string."""
    parse.parse_manufacturer('AAA')
    pend = models.PendManufacturer.objects.get(original='AAA')

    assert pend.correction == 'Aaa'

def test__parse_manufacturer__no_sub__converts_to_title():
    """Tests parse_manufacturer converts to lower case when no sub."""
    output = parse.parse_manufacturer('aaa')

    assert output == 'Aaa'

def test__parse_manufacturer__no_raw_manufacturer():
    """Tests output with blank raw_manufacturer."""
    output = parse.parse_manufacturer(None)

    assert output is None

def test__parse_unit_issue__valid__with_sub():
    """Tests for proper parse handling with valid data and a sub."""
    models.SubsUnit.objects.create(original='AAA', correction='aaa')

    output = parse.parse_unit_issue('AAA')

    assert output == 'aaa'

def test__parse_unit_issue__output_without_sub():
    """Tests for output format without substitution."""
    output = parse.parse_unit_issue('AAA')

    assert output == 'aaa'

def test__parse_unit_issue__pend_created():
    """Tests PendUnit is properly created for new raw_string."""
    parse.parse_unit_issue('AAA')
    pend = models.PendUnit.objects.get(original='AAA')

    assert pend.correction == 'aaa'

def test__parse_unit_issue__no_sub__converts_to_lower():
    """Tests parse_unit_issue converts to lower case when no sub."""
    output = parse.parse_unit_issue('AaA')

    assert output == 'aaa'

def test__parse_unit_issue__no_raw_unit_issue():
    """Tests output with blank raw_unit."""
    output = parse.parse_unit_issue(None)

    assert output is None

def test__assemble_generic_product__all():
    """Tests creation of generic product name with all details."""
    output = parse.assemble_generic_product(
        {'brand_name': 'B', 'strength': 's', 'route': 'r', 'dosage_form': 'f'}, 'g'
    )

    assert output == 'g (s r f)'

def test__assemble_generic_product__strength():
    """Tests creation of generic product name with only strength."""
    output = parse.assemble_generic_product(
        {
            'brand_name': None,
            'strength': 's',
            'route': None,
            'dosage_form': None,
        },
        'g'
    )

    assert output == 'g (s)'

def test__assemble_generic_product__route():
    """Tests creation of generic product name with only strength."""
    output = parse.assemble_generic_product(
        {
            'brand_name': None,
            'strength': None,
            'route': 'r',
            'dosage_form': None,
        },
        'g'
    )

    assert output == 'g (r)'

def test__assemble_generic_product__dosage_form():
    """Tests creation of generic product name with only strength."""
    output = parse.assemble_generic_product(
        {
            'brand_name': None,
            'strength': None,
            'route': None,
            'dosage_form': 'f',
        },
        'g'
    )

    assert output == 'g (f)'

def test__assemble_generic_product__generic():
    """Tests creation of generic product name with only generic name."""
    output = parse.assemble_generic_product(
        {
            'brand_name': None,
            'strength': None,
            'route': None,
            'dosage_form': None,
        },
        'g'
    )

    assert output == 'g'
