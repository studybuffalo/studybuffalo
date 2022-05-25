"""URLs for the Health Canada Drug Product Database app."""
from django.urls import path
from . import views


app_name = 'hc_dpd'

urlpatterns = [
    path('dpd/', views.DPDList.as_view(), name='dpd_list'),
    path('active-ingredient/', views.OriginalActiveIngredientList.as_view(), name='original_active_ingredient_list'),
    path('biosimilar/', views.OriginalBiosimilarList.as_view(), name='original_biosimilar_list'),
    path('company/', views.OriginalCompanyList.as_view(), name='original_company_list'),
    path('drug-product/', views.OriginalDrugProductList.as_view(), name='original_drug_product_list'),
    path('form/', views.OriginalFormList.as_view(), name='original_form_list'),
    path('inactive-product/', views.OriginalInactiveProductList.as_view(), name='original_inactive_product_list'),
    path('packaging/', views.OriginalPackagingList.as_view(), name='original_packaging_list'),
    path(
        'pharmaceutical-standard/',
        views.OriginalPharmaceuticalStandardList.as_view(),
        name='original_pharmaceutical_standard_list',
    ),
    path('route/', views.OriginalRouteList.as_view(), name='original_route_list'),
    path('schedule/', views.OriginalScheduleList.as_view(), name='original_schedule_list'),
    path('status/', views.OriginalStatusList.as_view(), name='original_status_list'),
    path('therapeutic-class/', views.OriginalTherapeuticClassList.as_view(), name='original_therapeutic_class_list'),
    path('veterinary-species/', views.OriginalVeterinarySpeciesList.as_view(), name='original_veterinary_species_list'),
]
