"""Tests for the User Admin."""
import pytest

from users.admin import MyUserCreationForm


pytestmark = pytest.mark.django_db


def test__my_user_creation_form__clean_username_success():
    """Tests that clean username validation works as expected."""
    # Instantiate the form with a new username
    form = MyUserCreationForm(
        {
            'username': 'alamode',
            'password1': '7jefB#f@Cc7YJB]2v',
            'password2': '7jefB#f@Cc7YJB]2v',
        }
    )
    # Run is_valid() to trigger the validation
    valid = form.is_valid()

    # Run the actual clean_username method
    username = form.clean_username()

    assert valid
    assert username == 'alamode'


def test__my_user_creation_form__clean_username_false(user):
    """Tests that clean_username fails when username already taken."""
    # Instantiate the form with the same username as self.user
    form = MyUserCreationForm(
        {
            'username': user.username,
            'password1': 'notalamodespassword',
            'password2': 'notalamodespassword',
        }
    )
    # Run is_valid() to trigger the validation, which is going to fail
    # because the username is already taken
    valid = form.is_valid()

    # The form.errors dict should contain a single error called 'username'
    assert valid is False
    assert len(form.errors) == 1
    assert 'username' in form.errors
