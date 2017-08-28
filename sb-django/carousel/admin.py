from django.contrib import admin

from .models import CarouselSlide

@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "priority", "background")
    list_filter = ("start_date", "end_date")