from django.db import models
import django.utils.timezone
import uuid
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Category(models.Model):
    """Defines categories for Play Items"""
    category = models.CharField(max_length=100,
                                help_text="The name of the category")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """String representing the Category object"""
        return self.category

class PlayPage(models.Model):
    """Defines a page to contain PlayItem(s)"""
    title = models.CharField(max_length=256,
                             help_text="Title for the page")

    date = models.DateField(default=django.utils.timezone.now,
                            help_text="Date the play item was release")
    
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)

    # Meta Settings
    class Meta:
        ordering = ["date", "title"]
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        """String representing the Play Image object"""
        return "{0} - {1}".format(self.date, self.title)

class PlayImage(models.Model):
    """Defines an individual image and its characteristics"""
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          editable=False,
                          help_text="Unqiue ID for this item")

    title = models.CharField(max_length=256,
                             help_text="Title to display above the image",
                             blank=True)

    type = models.CharField(max_length=1, 
                            default="i",
                            editable=False,
                            help_text="The file type of the item")

    location = models.ImageField(upload_to="play/images/original/",
                                help_text="The uploaded image (high quality)")

    alt_text = models.CharField(max_length=256,
                                blank=True,
                                help_text="Text to show on cursor hover over the item")

    description = models.TextField(blank=True,
                                   help_text="Any additional text to display below the image")

    page = models.ForeignKey("PlayPage", 
                             on_delete=models.SET_NULL, 
                             blank=True,
                             null=True)

    ordering = models.PositiveSmallIntegerField(default=1)

    # Meta Settings
    class Meta:
        ordering = ["title"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        """String representing the Play Image object"""
        return self.location.name

class PlayAudio(models.Model):
    """Defines an individual audio and its characteristics"""
    id = models.UUIDField(primary_key=True, 
                          default=uuid.uuid4,
                          editable=False,
                          help_text="Unqiue ID for this item")

    title = models.CharField(max_length=256,
                             help_text="Title to display above the audio player",
                             blank=True)

    type = models.CharField(max_length=1, 
                            default="a",
                            editable=False,
                            help_text="The file type of the item")

    location = models.FileField(upload_to="play/audio/",
                                help_text="The uploaded audio content")

    description = models.TextField(blank=True,
                                   help_text="Any additional text to display below the image")

    page = models.ForeignKey("PlayPage", 
                             on_delete=models.SET_NULL, 
                             blank=True,
                             null=True)

    ordering = models.PositiveSmallIntegerField(default=1)

    # Meta Settings
    class Meta:
        ordering = ["title"]
        verbose_name = "Audio"
        verbose_name_plural = "Audio"

    def __str__(self):
        """String representing the Play Audio object"""
        return self.title

@receiver(post_delete, sender=PlayImage)
def play_image_delete(sender, instance, **kwargs):
    """Removes the image file on model instance deletion"""
    instance.location.delete(False)