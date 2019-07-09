from django.conf.urls import url
from . import views

urlpatterns = [
    # Field substitutions
    url(r"^subs/bsrf/$", views.SubsBSRFList.as_view(), name="subs_bsrf_list"),
    url(r"^subs/generic/$", views.SubsGenericList.as_view(), name="subs_generic_list"),
    url(r"^subs/manufacturer/$", views.SubsManufacturerList.as_view(), name="subs_manufacturer_list"),
    url(r"^subs/unit/$", views.SubsUnitList.as_view(), name="subs_unit_list"),

    # Frontend endpoints
    url(r"^live-search/$", views.live_search, name="live_search"),
    url(r"^add-item/$", views.add_item, name="add_item"),
    url(r"^comparison-search/$", views.comparison_search, name="comparison_search"),
    url(r"^generate-comparison/$", views.generate_comparison, name="generate_comparison"),
    url(r"^$", views.index, name="drug_price_calculator_index"),
]
