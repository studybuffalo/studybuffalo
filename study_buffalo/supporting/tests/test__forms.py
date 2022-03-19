"""Tests for the supporting Forms."""
from supporting import forms


def test__contact_form__sender_name__max_length():
    """Confirms the sender_name field has expected max length."""
    max_length = forms.ContactForm().fields['sender_name'].max_length

    assert max_length == 256


def test__contact_form__message__max_length():
    """Confirms the message field has no max length."""
    max_length = forms.ContactForm().fields['message'].max_length

    assert max_length is None
