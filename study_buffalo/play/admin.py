"""Admin settings for the Play app."""
from django.contrib import admin
from .models import PlayPage, PlayImage, PlayAudio, Category

admin.site.register(PlayImage)
admin.site.register(PlayAudio)
admin.site.register(Category)

class PlayImageInline(admin.StackedInline):
    """Admin inline for the Play Image model."""
    model = PlayImage
    extra = 0
    fields = ['original_image', ('title', 'alt_text', 'ordering'), 'description', ]

class PlayAudioInline(admin.StackedInline):
    """Admin inline for the Play Audio model."""
    model = PlayAudio
    extra = 0

@admin.register(PlayPage)
class PlayPageAdmin(admin.ModelAdmin):
    """Admin for the Play Page."""
    list_display = ('date', 'title', 'release_date', 'category')
    list_filter = ('date', 'release_date', 'category')
    fields = ['title', ('date', 'release_date'), 'category']
    inlines = [PlayImageInline, PlayAudioInline]
