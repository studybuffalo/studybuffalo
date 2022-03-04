"""Views and objects to support creation of a sitemap."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from play.models import PlayPage
from study.models import Guide
from read.models import Publication


class CustomSitemap(Sitemap):
    """Extends the Sitemap model to allow specifying a group section"""
    def __init__(self, section):
        self.section = section
        self.latest_lastmod = None

    def __get(self, name, obj, default=None):
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)

        return attr

    def _urls(self, page, protocol, domain):
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod

        for item in self.paginator.page(page).object_list:
            loc = f'{protocol}://{domain}{self.__get("location", item)}'
            priority = self.__get('priority', item)
            lastmod = self.__get('lastmod', item)

            if all_items_lastmod:
                all_items_lastmod = lastmod is not None

                if (all_items_lastmod and (latest_lastmod is None or lastmod > latest_lastmod)):
                    latest_lastmod = lastmod

            # Modified to include a specified section in urls.py
            url_info = {
                'item': item,
                'location': loc,
                'lastmod': lastmod,
                'changefreq': self.__get('changefreq', item),
                'priority': str(priority if priority is not None else ''),
                'section': self.section,
            }

            urls.append(url_info)

        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod

        return urls


class PlaySitemap(CustomSitemap):
    """Sitemap class for the Play app."""
    changefreq = 'weekly'
    priority = 0.7
    section = 'play'

    def items(self):
        return PlayPage.objects.all()

    @staticmethod
    def lastmod(item):
        """Returns the last modified date for an item."""
        return item.release_date


class StudySitemap(CustomSitemap):
    """Sitemap class for the Study app."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Guide.objects.all()

    @staticmethod
    def lastmod(item):
        """Returns the last modified date for an item."""
        return item.last_update


class ReadSitemap(CustomSitemap):
    """Sitemap class for the Read app."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Publication.objects.all()

    @staticmethod
    def lastmod(item):
        """Returns the last modified date for an item."""
        return item.date_published


class ToolSitemap(CustomSitemap):
    """Sitemap class for the Tools app."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Modified so that you can pass a page name to reverse location
        # and a title for display
        return [
            {'name': 'alberta_adaptations_index', 'title': 'Alberta Adaptations'},
            {'name': 'drug_price_calculator_index', 'title': 'Drug Price Calculator'},
            {'name': 'vancomycin_calculator_index', 'title': 'Vancomycin Calculator'},
        ]

    def location(self, item):
        return reverse(item['name'])


class StaticViewSitemap(CustomSitemap):
    """Sitemap class for the static pages app."""
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        # Modified so that you can pass a page name to reverse location
        # and a title for display
        return [
            {'name': 'design_index', 'title': 'Design Index'},
            {'name': 'contact', 'title': 'Contact'},
            {'name': 'privacy_policy', 'title': 'Privacy Policy'},
            {'name': 'robot_policy', 'title': 'Robot Policy'},
        ]

    def location(self, item):
        return reverse(item['name'])
