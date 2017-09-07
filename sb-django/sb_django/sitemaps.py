from django.contrib.sitemaps import Sitemap
from play.models import PlayPage
from django.urls import reverse

class PlaySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
       return PlayPage.objects.all()
 
    def lastmod(self, item): 
       return item.release_date

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ["contact"]

    def location(self, item):
        return reverse(item)