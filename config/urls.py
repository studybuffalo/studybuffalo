"""Base URL settings for the Study Buffalo website."""
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.sitemaps.views import sitemap

from supporting import views
from supporting.sitemaps import PlaySitemap, StudySitemap, ToolSitemap, ReadSitemap, StaticViewSitemap


sitemaps = {
    'play': PlaySitemap('play'),
    'study': StudySitemap('study'),
    'tools': ToolSitemap('tools'),
    'read': ReadSitemap('read'),
    'static': StaticViewSitemap('other'),
}

urlpatterns = [
    path('api/', include('study_buffalo.api.urls', namespace='api')),
    path('play/', include('play.urls')),
    path('study/', include('study.urls')),
    path('read/', include('read.urls')),
    path('tools/', views.tools_index, name='tools_index'),
    path('rdrhc-calendar/', include('rdrhc_calendar.urls', namespace='rdrhc_calendar')),
    path('tools/alberta-adaptations/', views.alberta_adaptations_index, name='alberta_adaptations_index'),
    path('tools/dictionary/', include('dictionary.urls')),
    path('tools/dpd/', include('hc_dpd.urls', namespace='hc_dpd')),
    path('tools/drug-price-calculator/', include('drug_price_calculator.urls')),
    path('tools/substitutions/', include('substitutions.urls')),
    path('tools/vancomycin-calculator/', include('vancomycin_calculator.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('design/', views.design_index, name='design_index'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('robot-policy/', views.robot_policy, name='robot_policy'),
    path('contact/', views.contact, name='contact'),
    path(
        'sitemap/',
        views.custom_sitemap,
        {'sitemaps': sitemaps, 'template_name': 'sitemap_template.html', 'content_type': None},
        name='sitemap'
    ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/complete/', views.unsubscribe_complete, name='unsubscribe_complete'),
    path('accounts/profile/', views.account_profile, name='account_profile'),
    path('accounts/', include('allauth.urls')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt'), name='robots.txt'),
    path('', views.Index.as_view(), name='index'),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TEMPORARY URLS & REDIRECTS
urlpatterns += [
    path('cabs2018/', TemplateView.as_view(template_name='pages/cabs2018.html'), name='cabs2018'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            '400/',
            default_views.bad_request,
            kwargs={'exception': Exception('Bad Request!')},
        ),
        path(
            '403/',
            default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')},
        ),
        path(
            '404/',
            default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')},
        ),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
