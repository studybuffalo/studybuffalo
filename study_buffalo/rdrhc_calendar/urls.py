from django.conf.urls import include
from django.urls import path, re_path

from . import views

app_name = 'rdrhc_calendar'

urlpatterns = [
    path('settings/', views.calendar_settings, name='calendar_settings'),
    path('shifts/', views.ShiftCodeList.as_view(), name='calendar_code_list'),
    re_path(r'^shifts/<int:code>/', views.calendar_code_edit, name='calendar_code_edit'),
    path('shifts/add/', views.calendar_code_add, name='calendar_code_add'),
    re_path(r'^shifts/delete/<int:code>/', views.calendar_code_delete, name='calendar_code_delete'),
    path('missing-codes/', views.MissingShiftCodeList.as_view(), name='calendar_missing_code_list'),
    re_path(r'missing-codes/add/<int:code_id>/', views.missing_code_add, name='calendar_missing_code_add'),
    re_path(r'missing-codes/delete/<int:code_id>/', views.missing_code_delete, name='calendar_missing_code_delete'),
    path('api/v1/', include('rdrhc_calendar.api.urls', namespace='api_v1')),
    path('', views.calendar_index, name='calendar_index'),
]
