"""Admin settings for the Read app."""
from django.contrib import admin
from .models import Publication, DocumentPublication, HTMLPublication


admin.site.register(DocumentPublication)
admin.site.register(HTMLPublication)


class DocumentPublicationInline(admin.StackedInline):
    """Admin inline for the Document Publication model."""
    model = DocumentPublication
    extra = 0


class HTMLPublicationInline(admin.StackedInline):
    """Admin inline for the HTML Publication model."""
    model = HTMLPublication
    extra = 0


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    """Admin settings for the Publication model."""
    list_display = ('title', 'description', 'date_published',)
    list_filer = ('date_published',)
    fields = [
        'title',
        'description',
        'date_published',
    ]
    inlines = [DocumentPublicationInline, HTMLPublicationInline]
