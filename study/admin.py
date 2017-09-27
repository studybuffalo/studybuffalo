from django.contrib import admin
from .models import Guide, DocumentGuide, HTMLGuide, Bounty, BountyAssignment

admin.site.register(DocumentGuide)
admin.site.register(HTMLGuide)
admin.site.register(Bounty)
admin.site.register(BountyAssignment)

class DocumentGuideInline(admin.StackedInline):
    model = DocumentGuide
    extra = 0

class HTMLGuideInline(admin.StackedInline):
    model = HTMLGuide
    extra = 0

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "last_update", "permissions")
    list_filer = ("title", "last_update", "permissions")
    fields = [
        "title",
        "short_description", 
        "long_description", 
        ("date_original", "last_update"), 
        "permissions"
    ]
    inlines = [DocumentGuideInline, HTMLGuideInline]