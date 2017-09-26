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

from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

import os
from configparser import ConfigParser

# Dictionary containing your sitemap classes
sitemaps = {
   "play": PlaySitemap("play"),
   "study": StudySitemap("study"),
   "tools": ToolSitemap("tools"),
   "read": ReadSitemap("read"),
   "static": StaticViewSitemap("other"),
}

urlpatterns = [
    url(r"^play/", include("play.urls")),
    url(r"^study/", include("study.urls")),
    url(r"^read/", include("read.urls")),
    url(r"^tools/$", views.tools_index, name="tools_index"),
    url(r"^tools/alberta-adaptations/", views.alberta_adaptations_index, name="alberta_adaptations_index"),
    url(r"^tools/drug-price-calculator/", include("drug_price_calculator.urls")),
    url(r"^tools/vancomycin-calculator/", include("vancomycin_calculator.urls")),
    url(r"^design/$", views.design_index, name="design_index"),
    url(r"^privacy-policy/", views.privacy_policy, name="privacy_policy"),
    url(r"^robot-policy/", views.robot_policy, name="robot_policy"),
    url(r"^contact/", views.contact, name="contact"),
    url(r"^sitemap/", views.custom_sitemap, {"sitemaps": sitemaps, "template_name": "sitemap_template.html", "content_type": None}, name="sitemap"),
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r"^accounts/profile/$", views.account_profile, name="account_profile"),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^$", views.Index.as_view(), name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin login obscured for security reasons
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(os.path.dirname(BASE_DIR), "config", "sb_config.cfg")
config = ConfigParser()
config.read(CONFIG_PATH)
admin_regex = r"%s" % config.get("admin", "regex")

urlpatterns += [
    url(admin_regex, include(admin.site.urls)),
]