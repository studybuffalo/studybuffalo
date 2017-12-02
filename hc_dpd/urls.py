from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^dpd/$", views.DPDList.as_view(), name="_list"),
    url(r"^active-ingredient/$", views.ActiveIngredientList.as_view()),
    url(r"^company/$", views.CompanyList.as_view()),
    url(r"^drug-product/$", views.DrugProductList.as_view()),
    url(r"^form/$", views.FormList.as_view()),
    url(r"^inactive-product/$", views.InactiveProductList.as_view()),
    url(r"^packaging/$", views.PackagingList.as_view()),
    url(r"^pharmaceutical-standard/$", views.PharmaceuticalStandardList.as_view()),
    url(r"^route/$", views.RouteList.as_view()),
    url(r"^schedule/$", views.ScheduleList.as_view()),
    url(r"^status/$", views.StatusList.as_view()),
    url(r"^therapeutic-class/$", views.TherapeuticClassList.as_view()),
    url(r"^veterinary-species/$", views.VeterinarySpeciesList.as_view()),
]
