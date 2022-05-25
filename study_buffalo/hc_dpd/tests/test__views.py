"""Tests for Views of HC DPD app."""
import pytest

from django.test import Client
from django.urls import reverse

from hc_dpd.tests import utils


pytestmark = pytest.mark.django_db


def test__dpd_list__template(user):
    """Test for proper template in DPDList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:dpd_list'))

    # Test for template
    assert (
        'hc_dpd/dpd_list.html' in [t.name for t in response.templates]
    )


def test__dpd_list__context(user):
    """Confirms DPDList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:dpd_list'))

    # Test for context key
    assert 'dpd_list' in response.context


def test__original_active_ingredient_list__template(user):
    """Test for proper template in OriginalActiveIngredientList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_active_ingredient_list'))

    # Test for template
    assert (
        'hc_dpd/originalactiveingredient_list.html' in [t.name for t in response.templates]
    )


def test__original_active_ingredient_list__context(user):
    """Confirms OriginalActiveIngredientList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_active_ingredient_list'))

    # Test for context key
    assert 'active_ingredient_list' in response.context


def test__original_biosimilar_list__template(user):
    """Test for proper template in OriginalBiosimilarList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_biosimilar_list'))

    # Test for template
    assert (
        'hc_dpd/originalbiosimilar_list.html' in [t.name for t in response.templates]
    )


def test__original_biosimilar_list__context(user):
    """Confirms OriginalBiosimilarList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_biosimilar_list'))

    # Test for context key
    assert 'biosimilar_list' in response.context


def test__original_company_list__template(user):
    """Test for proper template in OriginalCompanyList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_company_list'))

    # Test for template
    assert (
        'hc_dpd/originalcompany_list.html' in [t.name for t in response.templates]
    )


def test__original_company_list__context(user):
    """Confirms OriginalCompanyList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_company_list'))

    # Test for context key
    assert 'company_list' in response.context


def test__original_drug_product_list__template(user):
    """Test for proper template in OriginalDrugProductList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_drug_product_list'))

    # Test for template
    assert (
        'hc_dpd/originaldrugproduct_list.html' in [t.name for t in response.templates]
    )


def test__original_drug_product_list__context(user):
    """Confirms OriginalDrugProductList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_drug_product_list'))

    # Test for context key
    assert 'drug_product_list' in response.context


def test__original_form_list__template(user):
    """Test for proper template in OriginalFormList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_form_list'))

    # Test for template
    assert (
        'hc_dpd/originalform_list.html' in [t.name for t in response.templates]
    )


def test__original_form_list__context(user):
    """Confirms OriginalFormList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_form_list'))

    # Test for context key
    assert 'form_list' in response.context


def test__original_inactive_product_list__template(user):
    """Test for proper template in OriginalInactiveProduct views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_inactive_product_list'))

    # Test for template
    assert (
        'hc_dpd/originalinactiveproduct_list.html' in [t.name for t in response.templates]
    )


def test__original_inactive_product_list__context(user):
    """Confirms OriginalInactiveProduct view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_inactive_product_list'))

    # Test for context key
    assert 'inactive_product_list' in response.context


def test__original_packaging_list__template(user):
    """Test for proper template in OriginalPackaging views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_packaging_list'))

    # Test for template
    assert (
        'hc_dpd/originalpackaging_list.html' in [t.name for t in response.templates]
    )


def test__original_packaging_list__context(user):
    """Confirms OriginalPackaging view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_packaging_list'))

    # Test for context key
    assert 'packaging_list' in response.context


def test__original_pharmaceutical_standard_list__template(user):
    """Test for proper template in OriginalPharmaceuticalStandardList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_pharmaceutical_standard_list'))

    # Test for template
    assert (
        'hc_dpd/originalpharmaceuticalstandard_list.html' in [t.name for t in response.templates]
    )


def test__original_pharmaceutical_standard_list__context(user):
    """Confirms OriginalPharmaceuticalStandardList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_pharmaceutical_standard_list'))

    # Test for context key
    assert 'pharmaceutical_standard_list' in response.context


def test__original_route_list__template(user):
    """Test for proper template in OriginalRouteList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_route_list'))

    # Test for template
    assert (
        'hc_dpd/originalroute_list.html' in [t.name for t in response.templates]
    )


def test__original_route_list__context(user):
    """Confirms OriginalRouteList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_route_list'))

    # Test for context key
    assert 'route_list' in response.context


def test__original_schedule_list__template(user):
    """Test for proper template in OriginalScheduleList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_schedule_list'))

    # Test for template
    assert (
        'hc_dpd/originalschedule_list.html' in [t.name for t in response.templates]
    )


def test__original_schedule_list__context(user):
    """Confirms OriginalScheduleList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_schedule_list'))

    # Test for context key
    assert 'schedule_list' in response.context


def test__original_status_list__template(user):
    """Test for proper template in OriginalStatusList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_status_list'))

    # Test for template
    assert (
        'hc_dpd/originalstatus_list.html' in [t.name for t in response.templates]
    )


def test__original_status_list__context(user):
    """Confirms OriginalStatusList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_status_list'))

    # Test for context key
    assert 'status_list' in response.context


def test__original_therapeutic_class_list__template(user):
    """Test for proper template in OriginalTherapeuticClassList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_therapeutic_class_list'))

    # Test for template
    assert (
        'hc_dpd/originaltherapeuticclass_list.html' in [t.name for t in response.templates]
    )


def test__original_therapeutic_class_list__context(user):
    """Confirms OriginalTherapeuticClassList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_therapeutic_class_list'))

    # Test for context key
    assert 'therapeutic_class_list' in response.context


def test__original_veterinary_species_list__template(user):
    """Test for proper template in OriginalVeterinarySpeciesList views."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_veterinary_species_list'))

    # Test for template
    assert (
        'hc_dpd/originalveterinaryspecies_list.html' in [t.name for t in response.templates]
    )


def test__original_veterinary_species_list__context(user):
    """Confirms OriginalVeterinarySpeciesList view returns expected context name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_veterinary_species_list'))

    # Test for context key
    assert 'veterinary_species_list' in response.context
