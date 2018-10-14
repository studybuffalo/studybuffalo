from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^atc/$", views.ATCList.as_view(), name="atc_list"),
    url(r"^coverage/$", views.CoverageList.as_view(), name="coverage_list"),
    url(r"^extra-information/$", views.ExtraInformationList.as_view(), name="extra_information_list"),
    url(r"^price/$", views.PriceList.as_view(), name="price_list"),
    url(r"^ptc/$", views.PTCList.as_view(), name="ptc_list"),
    url(r"^subs/atc/$", views.SubsATCList.as_view(), name="subs_atc_list"),
    url(r"^subs/bsrf/$", views.SubsBSRFList.as_view(), name="subs_bsrf_list"),
    url(r"^subs/generic/$", views.SubsGenericList.as_view(), name="subs_generic_list"),
    url(r"^subs/manufacturer/$", views.SubsManufacturerList.as_view(), name="subs_manufacturer_list"),
    url(r"^subs/ptc/$", views.SubsPTCList.as_view(), name="subs_ptc_list"),
    url(r"^subs/unit/$", views.SubsUnitList.as_view(), name="subs_unit_list"),
    url(r"^special-authorization/$", views.SpecialAuthorizationList.as_view(), name="special_authorization_list"),
    url(r"^live-search/$", views.live_search, name="live_search"),
    url(r"^add-item/$", views.add_item, name="add_item"),
    url(r"^comparison-search/$", views.comparison_search, name="comparison_search"),
    url(r"^generate-comparison/$", views.generate_comparison, name="generate_comparison"),
    url(r"^$", views.index, name="drug_price_calculator_index"),
]
