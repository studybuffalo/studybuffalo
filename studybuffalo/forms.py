from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    sender_name = forms.CharField(
        label="Your name",
    )

    sender_email = forms.EmailField(
        error_messages={
            "required": "Please provide an email so we can contact you",
            "invalid": "Please enter a valid email so we can contact you",
        },
        label="Your email",
    )

    sender_subject = forms.ChoiceField(
        error_messages={
            "required": "Please specify a subject for your message",
        },
        label="Subject", 
        choices=(
            ("General Inquiry", "General Inquiry"),
            ("Study Guides", "Study Guides"),
            ("Practice Tools", "Practice Tools"),
        ),
        required=True,
    )

    message = forms.CharField(
        error_messages={
            "required": "Please enter a message for your email"
        },
        label="Message",
        required=True,
        widget=forms.Textarea,
    )

class UnsubscribeForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            "required": "Please provide an email to unsubscribe",
            "invalid": "Please enter a valid email to unsubscribe",
        },
        label="Your email",
        required=True,
    )