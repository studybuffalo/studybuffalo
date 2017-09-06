"""
Definition of urls for sb_django.
"""
from django.conf.urls import url
import django.contrib.auth.views

from django.conf.urls import include
from django.contrib import admin
from django.views.generic import RedirectView
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^play/", include("play.urls")),
    url(r"^study/", include("study.urls")),
    url(r"^read/", include("read.urls")),
    url(r"^tools$", views.tools_index, name="tools_index"),
    url(r"^tools/alberta-adaptations/", views.alberta_adaptations_index, name="alberta_adaptations_index"),
    url(r"^tools/drug-price-calculator/", include("drug_price_calculator.urls")),
    url(r"^tools/vancomycin-calculator/", include("vancomycin_calculator.urls")),
    url(r"^design/", views.design_index, name="design_index"),
    url(r"^contact/", views.contact, name="contact"),
    url(r"^$", views.Index.as_view(), name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)