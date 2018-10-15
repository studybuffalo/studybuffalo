from django.conf.urls import include
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from rdrhc_calendar.api import views

app_name = 'api_v1'
urlpatterns = [
    path('authentication/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:id>/', views.UserDetail.as_view(), name='user_detail'),
    path('shift-codes/<int:id>/', views.UserShiftCodesList.as_view(), name='user_shift_codes_list'),
    path('', views.api_root, name='root'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
