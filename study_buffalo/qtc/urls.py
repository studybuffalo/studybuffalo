from django.urls import path
from django.views.generic import TemplateView

app_name='qtc'

urlpatterns = [
    path('', TemplateView.as_view(template_name='qtc/index.html')),
]
