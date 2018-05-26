from django.shortcuts import render
from django.views import generic
from .models import Guide

class Index(generic.ListView):
    model = Guide
    context_object_name = "guide_list"
    template_name = "study/index.html"

class GuideDetail(generic.DetailView):
    model = Guide

    context_object_name = "guide_page"