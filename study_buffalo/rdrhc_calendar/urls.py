from django.conf.urls import include
from django.urls import path

from . import views

app_name = 'rdrhc_calendar'

urlpatterns = [
    path('settings/', views.calendar_settings, name='settings'),
    path('shifts/', views.ShiftCodeList.as_view(), name='code_list'),
    path('shifts/<int:code_id>/', views.calendar_code_edit, name='code_edit'),
    path('shifts/add/', views.calendar_code_add, name='code_add'),
    path('shifts/delete/<int:code_id>/', views.calendar_code_delete, name='code_delete'),
    path('missing-codes/', views.MissingShiftCodeList.as_view(), name='missing_code_list'),
    path('missing-codes/add/<int:code_id>/', views.missing_code_add, name='missing_code_add'),
    path('missing-codes/delete/<int:code_id>/', views.missing_code_delete, name='missing_code_delete'),
    path('api/v1/', include('rdrhc_calendar.api.urls', namespace='api_v1')),
    path('', views.calendar_index, name='index'),
]
