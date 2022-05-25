"""Tests for URLs of HC DPD app."""
import pytest

from django.test import Client
from django.urls import reverse

from hc_dpd.tests import utils


pytestmark = pytest.mark.django_db


def test__dpd_list__302_response_if_not_logged_in():
    """Tests for 302 response if user not logged in."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:dpd_list'))

    assert response.status_code == 302


def test__dpd_list__403_response_if_not_authorized(user):
    """Tests for 403 response if user does not have permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:dpd_list'))

    assert response.status_code == 403


def test__dpd_list__200_response_via_name(user):
    """Test for 200 response for the DPD list page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:dpd_list'))

    assert response.status_code == 200


def test__dpd_list__200_response_via_url(user):
    """Tests for 200 response for the DPD list page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/dpd/')

    assert response.status_code == 200


def test__original_active_ingredient_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalActiveIngredient List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_active_ingredient_list'))

    assert response.status_code == 302


def test__original_active_ingredient_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalActiveIngredient List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_active_ingredient_list'))

    assert response.status_code == 403


def test__original_active_ingredient_list__200_response_via_name(user):
    """Test for 200 response for the OriginalActiveIngredient List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_active_ingredient_list'))

    assert response.status_code == 200


def test__original_active_ingredient_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalActiveIngredient List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/active-ingredient/')

    assert response.status_code == 200


def test__original_biosimilar_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalBiosimilar List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_biosimilar_list'))

    assert response.status_code == 302


def test__original_biosimilar_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalBiosimilar List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_biosimilar_list'))

    assert response.status_code == 403


def test__original_biosimilar_list__200_response_via_name(user):
    """Test for 200 response for the OriginalBiosimilar List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_biosimilar_list'))

    assert response.status_code == 200


def test__original_biosimilar_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalBiosimilar List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/biosimilar/')

    assert response.status_code == 200


def test__original_company_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalCompany List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_company_list'))

    assert response.status_code == 302


def test__original_company_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalCompany List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_company_list'))

    assert response.status_code == 403


def test__original_company_list__200_response_via_name(user):
    """Test for 200 response for the OriginalCompany List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_company_list'))

    assert response.status_code == 200


def test__original_company_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalCompany List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/company/')

    assert response.status_code == 200


def test__original_drug_product_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalDrugProduct List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_drug_product_list'))

    assert response.status_code == 302


def test__original_drug_product_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalDrugProduct List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_drug_product_list'))

    assert response.status_code == 403


def test__original_drug_product_list__200_response_via_name(user):
    """Test for 200 response for the OriginalDrugProduct List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_drug_product_list'))

    assert response.status_code == 200


def test__original_drug_product_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalDrugProduct List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/drug-product/')

    assert response.status_code == 200


def test__original_form_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalForm List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_form_list'))

    assert response.status_code == 302


def test__original_form_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalForm List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_form_list'))

    assert response.status_code == 403


def test__original_form_list__200_response_via_name(user):
    """Test for 200 response for the OriginalForm List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_form_list'))

    assert response.status_code == 200


def test__original_form_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalForm List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/biosimilar/')

    assert response.status_code == 200


def test__original_inactive_product_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalInactiveProduct List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_inactive_product_list'))

    assert response.status_code == 302


def test__original_inactive_product_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalInactiveProduct List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_inactive_product_list'))

    assert response.status_code == 403


def test__original_inactive_product_list__200_response_via_name(user):
    """Test for 200 response for the OriginalInactiveProduct List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_inactive_product_list'))

    assert response.status_code == 200


def test__original_inactive_product_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalInactiveProduct List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/inactive-product/')

    assert response.status_code == 200


def test__original_packaging_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalPackaging List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_packaging_list'))

    assert response.status_code == 302


def test__original_packaging_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalPackaging List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_packaging_list'))

    assert response.status_code == 403


def test__original_packaging_list__200_response_via_name(user):
    """Test for 200 response for the OriginalPackaging List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_packaging_list'))

    assert response.status_code == 200


def test__original_packaging_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalPackaging List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/packaging/')

    assert response.status_code == 200


def test__original_pharmaceutical_standard_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalPharmaceuticalStandard List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_pharmaceutical_standard_list'))

    assert response.status_code == 302


def test__original_pharmaceutical_standard_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalPharmaceuticalStandard List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_pharmaceutical_standard_list'))

    assert response.status_code == 403


def test__original_pharmaceutical_standard_list__200_response_via_name(user):
    """Test for 200 response for the OriginalPharmaceuticalStandard List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_pharmaceutical_standard_list'))

    assert response.status_code == 200


def test__original_pharmaceutical_standard_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalPharmaceuticalStandard List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/pharmaceutical-standard/')

    assert response.status_code == 200


def test__original_route_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalRoute List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_route_list'))

    assert response.status_code == 302


def test__original_route_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalRoute List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_route_list'))

    assert response.status_code == 403


def test__original_route_list__200_response_via_name(user):
    """Test for 200 response for the OriginalRoute List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_route_list'))

    assert response.status_code == 200


def test__original_route_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalRoute List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/route/')

    assert response.status_code == 200


def test__original_schedule_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalSchedule List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_schedule_list'))

    assert response.status_code == 302


def test__original_schedule_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalSchedule List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_schedule_list'))

    assert response.status_code == 403


def test__original_schedule_list__200_response_via_name(user):
    """Test for 200 response for the OriginalSchedule List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_schedule_list'))

    assert response.status_code == 200


def test__original_schedule_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalSchedule List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/schedule/')

    assert response.status_code == 200


def test__original_status_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalStatus List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_status_list'))

    assert response.status_code == 302


def test__original_status_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalStatus List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_status_list'))

    assert response.status_code == 403


def test__original_status_list__200_response_via_name(user):
    """Test for 200 response for the OriginalStatus List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_status_list'))

    assert response.status_code == 200


def test__original_status_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalStatus List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/status/')

    assert response.status_code == 200


def test__original_therapeutic_class_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalTherapeuticClass List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_therapeutic_class_list'))

    assert response.status_code == 302


def test__original_therapeutic_class_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalTherapeuticClass List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_therapeutic_class_list'))

    assert response.status_code == 403


def test__original_therapeutic_class_list__200_response_via_name(user):
    """Test for 200 response for the OriginalTherapeuticClass List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_therapeutic_class_list'))

    assert response.status_code == 200


def test__original_therapeutic_class_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalTherapeuticClass List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/therapeutic-class/')

    assert response.status_code == 200


def test__original_veterinary_species_list__302_response_if_not_logged_in():
    """Tests for 403 response for OriginalVeterinarySpecies List page if anonymous."""
    # Set up client and response
    client = Client()
    response = client.get(reverse('hc_dpd:original_veterinary_species_list'))

    assert response.status_code == 302


def test__original_veterinary_species_list__403_response_if_not_authorized(user):
    """Tests for 403 response for OriginalVeterinarySpecies List page if no permissions."""
    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_veterinary_species_list'))

    assert response.status_code == 403


def test__original_veterinary_species_list__200_response_via_name(user):
    """Test for 200 response for the OriginalVeterinarySpecies List page via name."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Set up client and response
    client = Client()
    client.force_login(user=user)
    response = client.get(reverse('hc_dpd:original_veterinary_species_list'))

    assert response.status_code == 200


def test__original_veterinary_species_list__200_response_via_url(user):
    """Tests for 200 response for the OriginalVeterinarySpecies List page via URL."""
    # Add permission to user
    utils.add_web_view_permission(user)

    # Create client and force user login
    client = Client()
    client.force_login(user=user)

    # Test GET request
    response = client.get('/tools/dpd/veterinary-species/')

    assert response.status_code == 200
