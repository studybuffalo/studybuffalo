"""URLs for the Study app."""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='study_index'),
    url(r'^(?P<pk>\d+)/$', views.GuideDetail.as_view(), name='study_guide_page'),
]
