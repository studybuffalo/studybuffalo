"""Models for the Play app."""
from datetime import datetime
from io import BytesIO
import uuid

from PIL import Image, ImageFile

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
import django.utils.timezone


class Category(models.Model):
    """Defines categories for Play Items"""
    category = models.CharField(
        max_length=100,
        help_text='The name of the category',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """String representing the Category object"""
        return self.category


class PlayPage(models.Model):
    """Defines a page to contain PlayItem(s)"""
    title = models.CharField(
        max_length=256,
        help_text='Title for the page',
    )
    date = models.DateField(
        default=django.utils.timezone.now,
        help_text='Date the play item was released',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
    )
    release_date = models.DateTimeField(
        default=django.utils.timezone.now,
        help_text='Date to release this page on',
    )

    class Meta:
        ordering = ['date', 'title']
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        """String representing the Play Image object"""
        return f'{self.date} - {self.title}'

    def get_absolute_url(self):
        """Returns the URL to this page"""
        return reverse('play_page', args=[str(self.id)])

    def previous_page(self):
        """Returns the previous primary key ID."""
        previous_pk = self.pk - 1

        if previous_pk > 0:
            return previous_pk

        return None

    def next_page(self):
        """Returns the next primary key ID."""
        next_pk = self.pk + 1

        if next_pk <= self.last_page():
            return next_pk

        return None

    @staticmethod
    def last_page():
        """Returns the latest released page."""
        latest = PlayPage.objects.filter(
            release_date__date__lte=datetime.now()
        ).order_by(
            '-release_date'
        ).last().pk

        return latest


class PlayImage(models.Model):
    """Defines an individual image and its characteristics"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unqiue ID for this item',
    )
    title = models.CharField(
        max_length=256,
        help_text='Title to display above the image',
        blank=True,
    )
    type = models.CharField(
        max_length=1,
        default='i',
        editable=False,
        help_text='The file type of the item',
    )
    original_image = models.ImageField(
        upload_to='play/images/original/',
        help_text='The uploaded image (high quality)',
    )
    resized_image = models.ImageField(
        upload_to='play/images/resized/',
        editable=False,
    )
    alt_text = models.CharField(
        max_length=256,
        blank=True,
        help_text='Text to show on cursor hover over the item',
    )
    description = models.TextField(
        blank=True,
        help_text='Any additional text to display below the image',
    )
    page = models.ForeignKey(
        'PlayPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    ordering = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = ['ordering', 'title']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def save(self, *args, **kwargs):
        """Modifies save file functionality to generate a smaller file size"""
        # Fix for truncated image files
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        # Create a lower resolution image (if needed)
        orig = Image.open(self.original_image)

        if orig.width > 800:
            oWidth = orig.width
            oHeight = orig.height
            nWidth = 800
            nHeight = int(round((nWidth / oWidth) * oHeight))

            resize = orig.resize((nWidth, nHeight), Image.ANTIALIAS)
        else:
            resize = orig

        # Reduce dolor depth
        resize_io = BytesIO()
        resize.save(resize_io, format=orig.format, optimize=True)

        # Assign the new resize image to the resized_image field
        self.resized_image.save(self.original_image.name, resize_io, save=False)

        # Save the files
        super().save()

    def __str__(self):
        """String representing the Play Image object"""
        return self.original_image.name or ''


class PlayAudio(models.Model):
    """Defines an individual audio and its characteristics"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unqiue ID for this item',
    )
    title = models.CharField(
        max_length=256,
        help_text='Title to display above the audio player',
        blank=True,
    )
    type = models.CharField(
        max_length=1,
        default='a',
        editable=False,
        help_text='The file type of the item',
    )
    audio = models.FileField(
        upload_to='play/audio/',
        help_text='The uploaded audio content',
    )
    description = models.TextField(
        blank=True,
        help_text='Any additional text to display below the image',
    )
    page = models.ForeignKey(
        'PlayPage',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    ordering = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Audio'
        verbose_name_plural = 'Audio'

    def __str__(self):
        """String representing the Play Audio object"""
        return self.title


@receiver(post_delete, sender=PlayImage)
def play_image_delete(sender, instance, **kwargs):  # pylint: disable=unused-argument
    """Removes the image file on model instance deletion"""
    instance.original_image.delete(False)
    instance.resized_image.delete(False)
