"""Tests for the HC DPD Admin views."""
import pytest

from hc_dpd import admin


pytestmark = pytest.mark.django_db


def test__dpd_admin__trade_name(hc_dpd_original_drug_product):
    """Confirms output of the trade_name class method."""
    drug_product = hc_dpd_original_drug_product
    dpd = drug_product.drug_code

    assert admin.DPDAdmin.trade_name(dpd) == drug_product.brand_name
