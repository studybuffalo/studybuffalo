"""URLs for the RDRHC Calendar API."""
from django.conf.urls import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.rdrhc_calendar import views

app_name = 'api_v1'
urlpatterns = [
    path('authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/<int:user_id>/emails/', views.UserEmailList.as_view(), name='user_email_list'),
    path('users/<int:user_id>/emails/first-sent/', views.UserEmailFirstSent.as_view(), name='user_email_first_sent'),
    path('shifts/', views.ShiftList.as_view(), name='shift_list'),
    path('shifts/<int:user_id>/', views.UserScheduleList.as_view(), name='user_schedule_list'),
    path('shifts/<int:user_id>/delete/', views.UserScheduleDelete.as_view(), name='user_schedule_delete'),
    path('shifts/<int:user_id>/upload/', views.UserScheduleUpload.as_view(), name='user_schedule_upload'),
    path('shift-codes/<int:user_id>/', views.UserShiftCodesList.as_view(), name='user_shift_codes_list'),
    path('shift-codes/missing/upload/', views.MissingShiftCodesUpload.as_view(), name='missing_shift_codes_upload'),
    path('stat-holidays/', views.StatHolidaysList.as_view(), name='stat_holidays_list'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
