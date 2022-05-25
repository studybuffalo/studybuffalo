"""URLs for the Health Canada Drug Product Database app."""
from django.urls import path
from . import views


urlpatterns = [
    path('dpd/', views.DPDList.as_view(), name='_list'),
    path('active-ingredient/', views.OriginalActiveIngredientList.as_view()),
    path('biosimilar/', views.OriginalBiosimilarList.as_view()),
    path('company/', views.OriginalCompanyList.as_view()),
    path('drug-product/', views.OriginalDrugProductList.as_view()),
    path('form/', views.OriginalFormList.as_view()),
    path('inactive-product/', views.OriginalInactiveProductList.as_view()),
    path('packaging/', views.OriginalPackagingList.as_view()),
    path('pharmaceutical-standard/', views.OriginalPharmaceuticalStandardList.as_view()),
    path('route/', views.OriginalRouteList.as_view()),
    path('schedule/', views.OriginalScheduleList.as_view()),
    path('status/', views.OriginalStatusList.as_view()),
    path('therapeutic-class/', views.OriginalTherapeuticClassList.as_view()),
    path('veterinary-species/', views.OriginalVeterinarySpeciesList.as_view()),
]
