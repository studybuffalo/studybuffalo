"""URLs for the Read app."""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='pub_index'),
    url(r'^(?P<pk>\d+)/$', views.PublicationDetail.as_view(), name='pub_page'),
]
