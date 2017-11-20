from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^dpd/$", views.DPDList.as_view(), name="_list"),
    url(r"^active-ingredients/$", views.ActiveIngredientsList.as_view(), name="_list"),
    url(r"^companies/$", views.CompaniesList.as_view(), name="_list"),
    url(r"^drug-product/$", views.DrugProductList.as_view(), name="_list"),
    url(r"^form/$", views.FormList.as_view(), name="_list"),
    url(r"^inactive-products/$", views.InactiveProductsList.as_view(), name="_list"),
    url(r"^packaging/$", views.PackagingList.as_view(), name="_list"),
    url(r"^pharmaceutical-standard/$", views.PharmaceuticalStandardList.as_view(), name="_list"),
    url(r"^route/$", views.RouteList.as_view(), name="_list"),
    url(r"^schedule/$", views.ScheduleList.as_view(), name="_list"),
    url(r"^status/$", views.StatusList.as_view(), name="_list"),
    url(r"^therapeutic-class/$", views.TherapeuticClassList.as_view(), name="_list"),
    url(r"^veterinary-species/$", views.VeterinarySpeciesList.as_view(), name="_list"),
]
