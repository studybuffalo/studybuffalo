"""Tests for the supporting Sitemaps."""
# pylint: disable=protected-access
from django.utils import timezone

import pytest

from supporting import sitemaps


pytestmark = pytest.mark.django_db


def test__custom_sitemap__get__noncallable():
    """Test expected output of __get method for non-callable attribute.

        Note: this method undergoes name mangling, so note method name
        below.
    """
    sitemap = sitemaps.CustomSitemap(section='test')

    assert sitemap._CustomSitemap__get('section', None) == 'test'


def test__custom_sitemap__get__callable():
    """Test expected output of __get method for callable attribute.

        Note: this method undergoes name mangling, so note method name
        below.
    """
    sitemap = sitemaps.CustomSitemap(section='test')
    sitemap.callable_attribute = lambda x: x

    assert sitemap._CustomSitemap__get('callable_attribute', 'Other Test') == 'Other Test'


def test__custom_sitemap__get__not_present():
    """Test expected output of __get method for not present attribute.

        Note: this method undergoes name mangling, so note method name
        below.
    """
    sitemap = sitemaps.CustomSitemap(section='test')

    assert sitemap._CustomSitemap__get('fake', 'Other Test', 'Fake Test') == 'Fake Test'


def test__custom_site__urls__with_lastmod(play_page):
    """Tests for addition of 'section' in urls when lastmod present.

        Have to test with a child class as other methods need to be
        implemented for the _urls method to function.
    """
    now = timezone.now()
    play_page.release_date = now
    play_page.save()

    sitemap = sitemaps.PlaySitemap(section='test')

    urls = sitemap._urls(True, 'A', 'B')

    # Confirm section was added
    assert isinstance(urls, list)
    assert 'section' in urls[0]
    assert urls[0]['section'] == 'test'


def test__play_sitemap__items__output(play_page):
    """Confirms output of items method."""
    sitemap = sitemaps.PlaySitemap(section='test')

    items = sitemap.items()

    assert len(items) == 1
    assert items[0].pk == play_page.pk


def test__play_sitemap__lastmod__output(play_page):
    """Confirms output of lastmod method."""
    # Set defined release date for testing
    play_page.release_date = '2000-01-01T00:00:00Z'
    play_page.save()

    sitemap = sitemaps.PlaySitemap(section='test')

    assert sitemap.lastmod(play_page) == '2000-01-01T00:00:00Z'


def test__study_sitemap__items__output(study_guide):
    """Confirms output of items method."""
    sitemap = sitemaps.StudySitemap(section='test')

    items = sitemap.items()

    assert len(items) == 1
    assert items[0].pk == study_guide.pk


def test__study_sitemap__lastmod__output(study_guide):
    """Confirms output of lastmod method."""
    # Set defined release date for testing
    study_guide.last_update = '2000-01-01'
    study_guide.save()

    sitemap = sitemaps.StudySitemap(section='test')

    assert sitemap.lastmod(study_guide) == '2000-01-01'


def test__read_sitemap__items__output(read_publication):
    """Confirms output of items method."""
    sitemap = sitemaps.ReadSitemap(section='test')

    items = sitemap.items()

    assert len(items) == 1
    assert items[0].pk == read_publication.pk


def test__read_sitemap__lastmod__output(read_publication):
    """Confirms output of lastmod method."""
    # Set defined release date for testing
    read_publication.date_published = '2000-01-01'
    read_publication.save()

    sitemap = sitemaps.ReadSitemap(section='test')

    assert sitemap.lastmod(read_publication) == '2000-01-01'


def test__tools_sitemap__items__output():
    """Confirms output of items method."""
    sitemap = sitemaps.ToolSitemap(section='test')

    items = sitemap.items()

    assert isinstance(items, list)
    assert 'name' in items[0]
    assert 'title' in items[0]


def test__tools_sitemap__location__output():
    """Confirms output of location method."""
    sitemap = sitemaps.ToolSitemap(section='test')

    assert sitemap.location({'name': 'index'}) == '/'


def test__static_sitemap__items__output():
    """Confirms output of items method."""
    sitemap = sitemaps.StaticViewSitemap(section='test')

    items = sitemap.items()

    assert isinstance(items, list)
    assert 'name' in items[0]
    assert 'title' in items[0]



def test__static_sitemap__location__output():
    """Confirms output of location method."""
    sitemap = sitemaps.StaticViewSitemap(section='test')

    assert sitemap.location({'name': 'index'}) == '/'
