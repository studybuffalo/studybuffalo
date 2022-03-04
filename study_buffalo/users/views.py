"""Views for the Users model."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from .models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a user."""
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    """Redirect view to redirect back to User Detail view."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse('users:detail', kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """View to update User details."""
    fields = ['name']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    """List view for User model."""
    model = User

    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
