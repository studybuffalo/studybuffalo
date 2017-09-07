from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from carousel.models import CarouselSlide
from .forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.template.loader import get_template

class Index(generic.ListView):
    model = CarouselSlide

    context_object_name = "slides"
    template_name = "index.html"

def tools_index(request):
    """View for the tool page"""
    return render(
        request,
        "tools_index.html",
        context={},
    )

def alberta_adaptations_index(request):
    """View for the alberta adaptations page"""
    return render(
        request,
        "alberta_adaptations_index.html",
        context={},
    )

def design_index(request):
    """View for the design page"""
    return render(
        request,
        "design_index.html",
        context={},
    )

def privacy_policy(request):
    """View for the privacy policy page"""
    return render(
        request,
        "privacy_policy.html",
        context={},
    )

def robot_policy(request):
    """View for the robot policy page"""
    return render(
        request,
        "robot_policy.html",
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
            sender_name = form.cleaned_data["sender_name"]
            sender_email = form.cleaned_data["sender_email"]
            sender_subject = form.cleaned_data["sender_subject"]
            message = form.cleaned_data["message"]

            email_template = get_template("contact_email_template.txt")
            
            email_content = email_template.render({
                "sender_name": sender_name,
                "sender_email": sender_email,
                "message": message,
            })

            email = EmailMessage(
                sender_subject,
                email_content,
                sender_email,
                ["info@studybuffalo.com"],
                headers = {"Reply-To": sender_email},
            )

            email.send()
            # redirect to a new URL:
            return redirect("contact")

    # If other request, generate (and populate) form
    else:
        form = ContactForm()

    return render(
        request,
        "contact.html",
        context={'form': form},
    )