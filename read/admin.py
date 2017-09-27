from django.contrib import admin
from .models import Publication, DocumentPublication, HTMLPublication

admin.site.register(DocumentPublication)
admin.site.register(HTMLPublication)

class DocumentPublicationInline(admin.StackedInline):
    model = DocumentPublication
    extra = 0

class HTMLPublicationInline(admin.StackedInline):
    model = HTMLPublication
    extra = 0

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "date_published",)
    list_filer = ("date_published",)
    fields = [
        "title",
        "description", 
        "date_published", 
    ]
    inlines = [DocumentPublicationInline, HTMLPublicationInline]