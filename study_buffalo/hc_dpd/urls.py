"""URLs for the Health Canada Drug Product Database app."""
from django.urls import path
from . import views


urlpatterns = [
    path('dpd/', views.DPDList.as_view(), name='_list'),
    path('active-ingredient/', views.ActiveIngredientList.as_view()),
    path('biosimilar/', views.BiosimilarList.as_view()),
    path('company/', views.CompanyList.as_view()),
    path('drug-product/', views.DrugProductList.as_view()),
    path('form/', views.FormList.as_view()),
    path('inactive-product/', views.InactiveProductList.as_view()),
    path('packaging/', views.PackagingList.as_view()),
    path('pharmaceutical-standard/', views.PharmaceuticalStandardList.as_view()),
    path('route/', views.RouteList.as_view()),
    path('schedule/', views.ScheduleList.as_view()),
    path('status/', views.StatusList.as_view()),
    path('therapeutic-class/', views.TherapeuticClassList.as_view()),
    path('veterinary-species/', views.VeterinarySpeciesList.as_view()),
]
