"""Admin settings for the Users app."""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    """Updated form to change user details."""
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):
    """Updated form to create a new user."""
    error_message = UserCreationForm.error_messages.update(
        {'duplicate_username': 'This username has already been taken.'}
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        """Additional validation to confirm username is unique."""
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    """Admin details for the User model."""
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (('User Profile', {'fields': ('name',)}),) + AuthUserAdmin.fieldsets
    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']
