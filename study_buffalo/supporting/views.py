"""Additional and (generally) static views to support the website."""
from calendar import timegm
import datetime
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.http import http_date
from django.views import generic

from supporting.forms import ContactForm, UnsubscribeForm
from updates.models import Update


class Index(generic.ListView):
    """View to create an index page for the updates section."""
    context_object_name = 'updates'
    template_name = 'index.html'

    def get_queryset(self):
        today = datetime.datetime.today()
        return Update.objects.filter(
            start_date__lte=today
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gt=today)
        )

def tools_index(request):
    """View for the tool page"""
    return render(
        request,
        'tools_index.html',
        context={},
    )

def alberta_adaptations_index(request):
    """View for the alberta adaptations page"""
    return render(
        request,
        'alberta_adaptations_index.html',
        context={},
    )

def design_index(request):
    """View for the design page"""
    return render(
        request,
        'design_index.html',
        context={},
    )

def privacy_policy(request):
    """View for the privacy policy page"""
    return render(
        request,
        'privacy_policy.html',
        context={},
    )

def robot_policy(request):
    """View for the robot policy page"""
    return render(
        request,
        'robot_policy.html',
        context={},
    )

def contact(request):
    """View for the contact information page"""
    # If POST process and send email
    if request.method == 'POST':

        # Create a form instance and populate with data
        form = ContactForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            sender_name = form.cleaned_data['sender_name']
            sender_email = form.cleaned_data['sender_email']
            sender_subject = form.cleaned_data['sender_subject']
            message = form.cleaned_data['message']

            email_template = get_template('contact_email_template.txt')

            email_content = email_template.render({
                'sender_name': sender_name,
                'sender_email': sender_email,
                'message': message,
            })

            email = EmailMessage(
                sender_subject,
                email_content,
                sender_email,
                ['info@studybuffalo.com'],
                headers = {'Reply-To': sender_email},
            )

            try:
                # Send the email
                email.send()

                # Generate the success message
                messages.success(
                    request,
                    (
                        'Your message has been sent, we will get back '
                        'to you as soon as we can.'
                    )
                )

                # redirect to a new URL:
                return redirect('contact')
            except TypeError:
                # Notify user of the error
                messages.error(
                    request,
                    (
                        'There was an error sending your message - '
                        'please confirm your email has been entered '
                        'properly'
                    )
                )

    # If other request, generate (and populate) form
    else:
        form = ContactForm()

    return render(
        request,
        'contact.html',
        context={'form': form},
    )

def unsubscribe(request):
    """View for the email unsubscribe page"""
    # If POST process and send email
    if request.method == 'POST':
        # Create a form instance and populate with data
        form = UnsubscribeForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            sender_email = form.cleaned_data['email']

            email_template = get_template('unsubscribe_email_template.txt')

            email_content = email_template.render({'email': sender_email})

            email = EmailMessage(
                'Email Unsubscribe Request',
                email_content,
                sender_email,
                ['info@studybuffalo.com'],
                headers = {'Reply-To': sender_email},
            )

            try:
                # Send the email
                email.send()

                # redirect to a new URL:
                return redirect('unsubscribe_complete')
            except TypeError:
                # Notify user of the error
                messages.error(
                    request,
                    (
                        'There was an error processing your request - '
                        'please confirm your email has been entered '
                        'properly'
                    )
                )

    # If other request, generate (and populate) form
    else:
        form = UnsubscribeForm()

    return render(
        request,
        'unsubscribe.html',
        context={'form': form},
    )

def unsubscribe_complete(request):
    """View to render confirmation of successful unsubscribe."""
    return render(
        request,
        'unsubscribe_complete.html',
        context={},
    )

@login_required
def account_profile(request):
    """The user profile page"""
    return render(
        request,
        'account/profile.html',
        context={},
    )

def x_robots_tag(func):
    """Adds tag no announce no indexing by robots"""
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner

@x_robots_tag
def custom_sitemap(request, sitemaps, section=None, template_name='sitemap.xml', content_type='application/xml'): # pylint: disable=too-many-locals, too-many-branches
    """A custom sitemap view to generate an HTML sitemap"""
    req_protocol = request.scheme
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404(f'No sitemap available for section: {section}')
        maps = [sitemaps[section]]
    else:
        maps = sitemaps.values()

    page = request.GET.get('p', 1)

    lastmod = None
    all_sites_lastmod = True
    urls = []

    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
            if all_sites_lastmod:
                site_lastmod = getattr(site, 'latest_lastmod', None)

                if site_lastmod is not None:
                    site_lastmod = (
                        site_lastmod.utctimetuple() if isinstance(site_lastmod, datetime.datetime)
                        else site_lastmod.timetuple()
                    )
                    lastmod = site_lastmod if lastmod is None else max(lastmod, site_lastmod)
                else:
                    all_sites_lastmod = False
        except EmptyPage as empty_page_error:
            raise Http404(f'Page {page} empty') from empty_page_error
        except PageNotAnInteger as not_an_integer:
            raise Http404(f'No page {page}') from not_an_integer

    # Create filters for the various pages
    play_urls = []
    study_urls = []
    tools_urls = []
    read_urls = []
    other_urls = []

    for url in urls:
        if url['section'] == 'play':
            play_urls.append(url)
        elif url['section'] == 'study':
            study_urls.append(url)
        elif url['section'] == 'tools':
            tools_urls.append(url)
        elif url['section'] == 'read':
            read_urls.append(url)
        else:
            other_urls.append(url)

    # Context modified to include various filtered URL sets
    response = TemplateResponse(
        request,
        template_name,
        context={
            'urlset': urls,
            'play_urlset': play_urls,
            'study_urlset': study_urls,
            'tools_urlset': tools_urls,
            'read_urlset': read_urls,
            'other_urlset': other_urls,
        },
        content_type=content_type,
    )

    if all_sites_lastmod and lastmod is not None:
        # if lastmod is defined for all sites, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        response['Last-Modified'] = http_date(timegm(lastmod))

    return response
