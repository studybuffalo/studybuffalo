from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.Index.as_view(), name="index"),
    url(r"^archive$", views.Archive.as_view(), name="archive"),
    url(r"^(?P<pk>\d+)/$", views.PlayPageDetail.as_view(), name="play_page"),
]