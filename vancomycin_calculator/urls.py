from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index, name="vancomycin_calculator_index"),
]