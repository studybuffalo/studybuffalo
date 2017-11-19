"""
Definition of urls for studybuffalo.
"""

import django.contrib.auth.views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView

from . import views
from .sitemaps import *

import environ

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
    url(r"^rdrhc-calendar/", include("rdrhc_calendar.urls")),
    url(r"^tools/alberta-adaptations/", views.alberta_adaptations_index, name="alberta_adaptations_index"),
    url(r"^tools/dpd/", include("hc_dpd.urls")),
    url(r"^tools/drug-price-calculator/", include("drug_price_calculator.urls")),
    url(r"^tools/vancomycin-calculator/", include("vancomycin_calculator.urls")),
    url(r"^design/$", views.design_index, name="design_index"),
    url(r"^privacy-policy/", views.privacy_policy, name="privacy_policy"),
    url(r"^robot-policy/", views.robot_policy, name="robot_policy"),
    url(r"^contact/", views.contact, name="contact"),
    url(r"^sitemap/", views.custom_sitemap, {"sitemaps": sitemaps, "template_name": "sitemap_template.html", "content_type": None}, name="sitemap"),
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r"^logs/", include("log_manager.urls")),
    url(r"^unsubscribe/$", views.unsubscribe, name="unsubscribe"),
    url(r"^unsubscribe/complete$", views.unsubscribe_complete, name="unsubscribe_complete"),
    url(r"^accounts/profile/$", views.account_profile, name="account_profile"),
    url(r"^accounts/", include("allauth.urls")),
    url(r"^robots\.txt$", TemplateView.as_view(template_name="robots.txt"), name="robots.txt"),
    url(r"^$", views.Index.as_view(), name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Set a secure path for the admin site
# Set the Base Directory
BASE_DIR = environ.Path(__file__) - 2

# Connect to the .env file
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(env_file=BASE_DIR.path('..', 'config').file('studybuffalo.env'))

admin_regex = r"%s/" % env('ADMIN_URL')

urlpatterns += [
    url(admin_regex, include(admin.site.urls)),
]