"""Tests for the supporting Views."""
# pylint: disable=protected-access, too-few-public-methods, no-self-use
from datetime import datetime
from smtplib import SMTPException
from time import struct_time
from unittest.mock import patch
import pytest

from django.core import mail
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone


from updates import models
from supporting import views, forms


pytestmark = pytest.mark.django_db


class MockEmailMessage():
    """Mock of EmailMessage for testing."""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def send(self):
        """Mock of method to raise SMTPException."""
        raise SMTPException


class MockSite():
    """Mock of a site for testing."""
    def __init__(self, latest_lastmod=timezone.now()):
        self.latest_lastmod = latest_lastmod

    def get_urls(self, page, site, protocol):
        """Mock of get_urls method for testing."""
        return [{'page': page, 'site': site, 'protocol': protocol}]


class MockSiteEmptyPageError(MockSite):
    """Mock of site to raise EmptyPage error."""
    def get_urls(self, page, site, protocol):
        """Override get_urls to raise EmptyPage error."""
        raise EmptyPage


class MockSiteNotIntegerError(MockSite):
    """Mock of site to raise PageNotAnInteger error."""
    def get_urls(self, page, site, protocol):
        """Override get_urls to raise PageNotAnInteger error."""
        raise PageNotAnInteger


def mock_get_current_site(request):
    """Mocks get_current_site for testing."""
    return getattr(request, 'site', 'Test Site')


def mock_get_urls_and_mod_dates(*args, **kwargs):
    """Mocks _get_urls_and_mod_dates for testing."""
    urls = [
        {'play': 1},
        {'study': 2},
        {'tools': 3},
        {'read': 4},
        {'other': 5},
        {'maps': args[0]}
    ]
    mods = {
        'all_sites_lastmod': kwargs.get('all_sites_lastmod', False),
        'lastmod': kwargs.get('all_sites_lastmod', None),
    }

    return urls, mods


def mock_assemble_url_sections(*args):
    """Mocks _assemble_url_sections for testing."""
    return {
        'play': 1,
        'study': 2,
        'tools': 3,
        'read': 4,
        'other': 5,
    }


def test__index__200_response():
    """Confirms Index view returns 200 response."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('index'))

    # Confirm status code
    assert response.status_code == 200


def test__index__template():
    """Confirms Index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('index'))

    # Test for template
    assert (
        'index.html' in [t.name for t in response.templates]
    )


def test__index__context():
    """Confirms Index view returns expected context details."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('index'))

    # Test for default context key
    assert 'updates' in response.context


def test__index__get_queryset(updates_update):
    """Tests that expected update objects are returned."""
    # Create/update model instances for testing
    # Instance with start date before today and no end date
    update_1 = updates_update
    update_1.start_date = '2000-01-01'
    update_1.end_date = None
    update_1.save()

    # Instance with start date before today and future end date
    update_2 = models.Update.objects.create(
        title='Update 2',
        icon=update_1.icon,
        start_date='2000-01-02',
        end_date='3000-01-01',
    )

    # Instance with start date and end date before today
    update_3 = models.Update.objects.create(
        title='Update 3',
        icon=update_1.icon,
        start_date='2000-01-02',
        end_date='2001-01-01',
    )

    # Instance with start date after today
    update_4 = models.Update.objects.create(
        title='Update 4',
        icon=update_1.icon,
        start_date='3000-01-02',
    )

    index = views.Index()
    query = index.get_queryset()
    query_ids = query.values_list('pk', flat=True)

    assert update_1.pk in query_ids
    assert update_2.pk in query_ids
    assert update_3.pk not in query_ids
    assert update_4.pk not in query_ids


def test__tools_index__200_response():
    """Confirms tools index view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.tools_index(request)

    # Confirm status code
    assert response.status_code == 200


def test__tools_index__template():
    """Confirms tools index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('tools_index'))

    # Test for template
    assert (
        'tools_index.html' in [t.name for t in response.templates]
    )


def test__adaptations_index__200_response():
    """Confirms adaptations index view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.alberta_adaptations_index(request)

    # Confirm status code
    assert response.status_code == 200


def test__adaptations_index__template():
    """Confirms adaptations index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('alberta_adaptations_index'))

    # Test for template
    assert (
        'alberta_adaptations_index.html' in [t.name for t in response.templates]
    )


def test__design_index__200_response():
    """Confirms design index view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.design_index(request)

    # Confirm status code
    assert response.status_code == 200


def test__design_index__template():
    """Confirms design index view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('design_index'))

    # Test for template
    assert (
        'design_index.html' in [t.name for t in response.templates]
    )


def test__privacy_policy__200_response():
    """Confirms privacy_policy view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.privacy_policy(request)

    # Confirm status code
    assert response.status_code == 200


def test__privacy_policy__template():
    """Confirms privacy_policy view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('privacy_policy'))

    # Test for template
    assert (
        'privacy_policy.html' in [t.name for t in response.templates]
    )


def test__robot_policy__200_response():
    """Confirms robot_policy view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    response = views.robot_policy(request)

    # Confirm status code
    assert response.status_code == 200


def test__robot_policy__template():
    """Confirms robot_policy view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('robot_policy'))

    # Test for template
    assert (
        'robot_policy.html' in [t.name for t in response.templates]
    )


def test__contact__200_response():
    """Confirms contact view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    request.META = {}
    response = views.contact(request)

    # Confirm status code
    assert response.status_code == 200


def test__contact__template():
    """Confirms contact view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.post(reverse('contact'))

    # Test for template
    assert (
        'contact.html' in [t.name for t in response.templates]
    )


def test__contact__context():
    """Confirms contact view returns expected context details."""
    # Create request, view, and response
    client = Client()
    response = client.post(reverse('contact'))

    # Test for default context key
    assert 'form' in response.context


def test__contact__post__valid_data():
    """Tests handling of valid form submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {
        'sender_name': 'Name',
        'sender_email': 'name@email.com',
        'sender_subject': 'General Inquiry',
        'message': 'Message',
    }

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('contact'), data=data, follow=True)

    # Confirm one email was sent and it has expected content
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'General Inquiry'

    # Confirm Message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 1
    assert 'Your message has been sent' in str(messages[0])


def test__contact__post__invalid_data():
    """Tests handling of invalid form submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {
        'sender_name': 'Name',
        'sender_email': 'name@email.com',
        'sender_subject': 'ERROR',
        'message': 'Message',
    }

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('contact'), data=data, follow=True)

    # Confirm no email was sent
    assert len(mail.outbox) == 0

    # Confirm no message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 0

    # Confirm form errors present
    assert response.context['form'].errors == {
        'sender_subject': [
            'Select a valid choice. ERROR is not one of the available choices.',
        ],
    }

    # Confirm form data sent back
    assert response.context['form'].data['sender_name'] == 'Name'


@patch('supporting.views.EmailMessage', MockEmailMessage)
def test__contact__post__email_smtp_exception():
    """Tests handling of SMTP exception on email submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {
        'sender_name': 'Name',
        'sender_email': 'name@email.com',
        'sender_subject': 'General Inquiry',
        'message': 'Message',
    }

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('contact'), data=data, follow=True)

    # Confirm no email was sent
    assert len(mail.outbox) == 0

    # Confirm Message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 1
    assert 'There was an error sending your message' in str(messages[0])


def test__contact__get__valid():
    """Tests handling of GET submission."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('contact'))

    # Confirm a form was returned
    assert isinstance(response.context['form'], forms.ContactForm)


def test__unsubscribe__200_response():
    """Confirms unsubscribe view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    request.META = {}
    response = views.unsubscribe(request)

    # Confirm status code
    assert response.status_code == 200


def test__unsubscribe__template():
    """Confirms unsubscribe view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe'))

    # Test for template
    assert (
        'unsubscribe.html' in [t.name for t in response.templates]
    )


def test__unsubscribe__context():
    """Confirms unsubscribe view returns expected context details."""
    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe'))

    # Test for default context key
    assert 'form' in response.context


def test__unsubscribe__post__valid_data():
    """Tests handling of valid form submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {'email': 'name@email.com'}

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe'), data=data, follow=True)

    # Confirm one email was sent and it has expected content
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Email Unsubscribe Request'

    # Confirm no Message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 0


def test__unsubscribe__post__invalid_data():
    """Tests handling of invalid form submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {'email': 'Name'}

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe'), data=data, follow=True)

    # Confirm no email was sent
    assert len(mail.outbox) == 0

    # Confirm no message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 0

    # Confirm form errors present
    assert response.context['form'].errors == {
        'email': ['Please enter a valid email to unsubscribe'],
    }

    # Confirm form data sent back
    assert response.context['form'].data['email'] == 'Name'


@patch('supporting.views.EmailMessage', MockEmailMessage)
def test__unsubscribe__post__email_smtp_exception():
    """Tests handling of SMTP exception on email submission."""
    # pylint: disable=no-member
    # Data for Form Submission
    data = {'email': 'name@email.com'}

    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe'), data=data, follow=True)

    # Confirm no email was sent
    assert len(mail.outbox) == 0

    # Confirm Message was sent
    messages = list(response.context['messages'])
    assert len(messages) == 1
    assert 'There was an error processing your request' in str(messages[0])


def test__unsubscribe__get__valid():
    """Tests handling of GET submission."""
    # Create request, view, and response
    client = Client()
    response = client.get(reverse('unsubscribe'))

    # Confirm a form was returned
    assert isinstance(response.context['form'], forms.UnsubscribeForm)


def test__unsubscribe_complete__200_response():
    """Confirms unsubscribe_complete view returns 200 response."""
    # Create request, view, and response
    request = RequestFactory()
    request.method = 'POST'
    request.POST = {}
    request.META = {}
    response = views.unsubscribe_complete(request)

    # Confirm status code
    assert response.status_code == 200


def test__unsubscribe_complete__template():
    """Confirms unsubscribe_complete view returns expected template."""
    # Create request, view, and response
    client = Client()
    response = client.post(reverse('unsubscribe_complete'))

    # Test for template
    assert (
        'unsubscribe_complete.html' in [t.name for t in response.templates]
    )


def test__account_profile__200_response(user):
    """Confirms account_profile view returns 200 response."""
    # Create request, view, and response
    client = Client()
    client.force_login(user)
    response = client.post(reverse('account_profile'))

    # Confirm status code
    assert response.status_code == 200


def test__account_profile__template(user):
    """Confirms account_profile view returns expected template."""
    # Create request, view, and response
    client = Client()
    client.force_login(user)
    response = client.post(reverse('account_profile'))

    # Test for template
    assert (
        'account/profile.html' in [t.name for t in response.templates]
    )


def test__x_robots_tag__additions():
    """Confirms proper tags are added to the response"""
    @views.x_robots_tag
    def test_function(request, *args, **kwargs):
        """Test functions for wrapper."""
        return {
            'request': request,
            'args': args,
            'kwargs': kwargs,
        }

    response = test_function({})

    assert 'X-Robots-Tag' in response
    assert response['X-Robots-Tag'] == 'noindex, noodp, noarchive'


def test__get_urls_and_mod_dates__callable_sites():
    """Tests get_urls_and_mod_dates function when sites are callable."""
    maps = [MockSite, MockSite]

    # Get URLs and modification details
    urls, mods = views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')

    # Confirm response details
    assert isinstance(urls, list)
    assert len(urls) == 2
    assert urls[0] == {'page': 'page', 'site': 'request site', 'protocol': 'request protocol'}

    assert isinstance(mods, dict)
    assert 'lastmod' in mods
    assert isinstance(mods['lastmod'], struct_time)
    assert 'all_sites_lastmod' in mods
    assert isinstance(mods['all_sites_lastmod'], bool)


def test__get_urls_and_mod_dates__noncallable_sites():
    """Tests get_urls_and_mod_dates function when sites are not callable."""
    maps = [
        MockSite(latest_lastmod=datetime(2000, 1, 1, 0, 0, 0)),
        MockSite(latest_lastmod=datetime(2001, 1, 1, 0, 0, 0)),
    ]

    # Get URLs and modification details
    _, mods = views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')

    # Confirm response details
    assert isinstance(mods, dict)
    assert 'lastmod' in mods
    assert isinstance(mods['lastmod'], struct_time)
    assert 'all_sites_lastmod' in mods
    assert isinstance(mods['all_sites_lastmod'], bool)


def test__get_urls_and_mod_dates__all_lastmod():
    """Tests get_urls_and_mod_dates function when all sites have lastmod."""
    maps = [
        MockSite(latest_lastmod=datetime(2000, 1, 1, 0, 0, 0)),
        MockSite(latest_lastmod=datetime(2001, 1, 1, 0, 0, 0)),
    ]

    # Get URLs and modification details
    _, mods = views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')

    # Confirm response details
    assert mods['lastmod'].tm_year == 2001
    assert mods['lastmod'].tm_mon == 1
    assert mods['lastmod'].tm_mday == 1
    assert mods['all_sites_lastmod'] is True


def test__get_urls_and_mod_dates__some_lastmod():
    """Tests get_urls_and_mod_dates function when some sites have lastmod."""
    maps = [
        MockSite(latest_lastmod=datetime(2000, 1, 1, 0, 0, 0)),
        MockSite(latest_lastmod=None),
    ]

    # Get URLs and modification details
    _, mods = views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')

    # Confirm response details
    assert mods['lastmod'].tm_year == 2000
    assert mods['lastmod'].tm_mon == 1
    assert mods['lastmod'].tm_mday == 1
    assert mods['all_sites_lastmod'] is False


def test__get_urls_and_mod_dates__timetuple_lastmod():
    """Tests get_urls_and_mod_dates function when lastmod is timetuple."""
    maps = [
        MockSite(latest_lastmod=datetime(2000, 1, 1).date()),
        MockSite(latest_lastmod=None),
    ]

    # Get URLs and modification details
    _, mods = views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')

    # Confirm response details
    assert mods['lastmod'].tm_year == 2000
    assert mods['lastmod'].tm_mon == 1
    assert mods['lastmod'].tm_mday == 1
    assert mods['all_sites_lastmod'] is False


def test__get_urls_and_mod_dates__empty_page_error():
    """Tests get_urls_and_mod_dates function handling of EmptyPage error."""
    maps = [MockSiteEmptyPageError(latest_lastmod=None)]

    # Get URLs and modification details
    try:
        views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')
    except Http404 as e:
        assert 'Page page empty' in str(e)
    else:
        assert False


def test__get_urls_and_mod_dates__page_not_an_integer_error():
    """Tests get_urls_and_mod_dates function handling of PageNotAnInteger error."""
    maps = [MockSiteNotIntegerError(latest_lastmod=None)]

    # Get URLs and modification details
    try:
        views._get_urls_and_mod_dates(maps, 'page', 'request site', 'request protocol')
    except Http404 as e:
        assert 'No page page' in str(e)
    else:
        assert False


def test__assemble_url_sections():
    """Tests proper output for assemble_url_sections function."""
    urls = [
        {'section': 'play', 'page': 1},
        {'section': 'study', 'page': 2},
        {'section': 'tools', 'page': 3},
        {'section': 'read', 'page': 4},
        {'section': 'other', 'page': 5},
    ]

    url_sections = views._assemble_url_sections(urls)

    assert isinstance(url_sections, dict)
    assert 'play' in url_sections
    assert isinstance(url_sections['play'], list)
    assert len(url_sections['play']) == 1
    assert url_sections['play'][0] == {'section': 'play', 'page': 1}
    assert 'study' in url_sections
    assert isinstance(url_sections['study'], list)
    assert len(url_sections['study']) == 1
    assert url_sections['study'][0] == {'section': 'study', 'page': 2}
    assert 'tools' in url_sections
    assert isinstance(url_sections['tools'], list)
    assert len(url_sections['tools']) == 1
    assert url_sections['tools'][0] == {'section': 'tools', 'page': 3}
    assert 'read' in url_sections
    assert isinstance(url_sections['read'], list)
    assert len(url_sections['read']) == 1
    assert url_sections['read'][0] == {'section': 'read', 'page': 4}
    assert 'other' in url_sections
    assert isinstance(url_sections['other'], list)
    assert len(url_sections['other']) == 1
    assert url_sections['other'][0] == {'section': 'other', 'page': 5}


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates', mock_get_urls_and_mod_dates)
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__output():
    """Tests custom_sitemap view for proper details in response."""
    # Setup details to call view
    section = 'Test Section'
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Call view and get response
    response = views.custom_sitemap(request, sitemaps, section)

    # Test for expected output details
    assert response.template_name == 'sitemap.xml'
    assert response.headers['Content-Type'] == 'application/xml'
    assert isinstance(response.context_data, dict)
    assert 'urlset' in response.context_data
    assert response.context_data['urlset'][0] == {'play': 1}
    assert 'play_urlset' in response.context_data
    assert response.context_data['play_urlset'] == 1
    assert 'study_urlset' in response.context_data
    assert response.context_data['study_urlset'] == 2
    assert 'tools_urlset' in response.context_data
    assert response.context_data['tools_urlset'] == 3
    assert 'read_urlset' in response.context_data
    assert response.context_data['read_urlset'] == 4
    assert 'other_urlset' in response.context_data
    assert response.context_data['other_urlset'] == 5


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates', mock_get_urls_and_mod_dates)
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__with_section():
    """Tests custom_sitemap view when section is provided."""
    # Setup details to call view
    section = 'Test Section'
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Call view and get response
    response = views.custom_sitemap(request, sitemaps, section)

    # Test for the passed in sitemap details to confirm right
    # paths were followed
    assert response.context_data['urlset'][5] == {'maps': [['Test Page']]}


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates', mock_get_urls_and_mod_dates)
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__without_sections():
    """Tests custom_sitemap view when sections are not provided."""
    # Setup details to call view
    section = None
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Call view and get response
    response = views.custom_sitemap(request, sitemaps, section)

    # Test for the passed in sitemap details to confirm right
    # paths were followed
    assert list(response.context_data['urlset'][5])[0] == 'maps'


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates', mock_get_urls_and_mod_dates)
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__with_invalid_section():
    """Tests custom_sitemap view when invalid section is provided."""
    # Setup details to call view
    section = 'Wrong Section'
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Call view and get response
    try:
        views.custom_sitemap(request, sitemaps, section)
    except Http404 as e:
        assert 'No sitemap available for section: Wrong Section' in str(e)
    else:
        assert False


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates')
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__with_all_lastmod(mock_get_urls):
    """Tests custom_sitemap view when all_sites_lastmod provided."""
    # Setup details to call view
    section = 'Test Section'
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Set patched return values for modify details
    mock_get_urls.return_value = (
        [],
        {
            'all_sites_lastmod': True,
            'lastmod': (2000, 1, 1, 0, 0, 0)
        },
    )

    # Call view and get response
    response = views.custom_sitemap(request, sitemaps, section)

    # Test that additional last-modified details added
    assert 'Last-Modified' in response
    assert response['Last-Modified'] == 'Sat, 01 Jan 2000 00:00:00 GMT'


@patch('supporting.views.get_current_site', mock_get_current_site)
@patch('supporting.views._get_urls_and_mod_dates')
@patch('supporting.views._assemble_url_sections', mock_assemble_url_sections)
def test__custom_sitemap__without_all_lastmod(mock_get_urls):
    """Tests custom_sitemap view when all_sites_lastmod not provided."""
    # Setup details to call view
    section = 'Test Section'
    sitemaps = {'Test Section': ['Test Page']}
    request = RequestFactory()
    request.GET = {'p': 2}
    request.scheme = 'http'

    # Set patched return values for modify details
    mock_get_urls.return_value = (
        [],
        {
            'all_sites_lastmod': False,
            'lastmod': (2000, 1, 1, 0, 0, 0)
        },
    )

    # Call view and get response
    response = views.custom_sitemap(request, sitemaps, section)

    # Test that additional last-modified details not added
    assert 'Last-Modified' not in response
