"""Models for the Updates app."""
from django.db import models
import django.utils.timezone


class Update(models.Model):
    """Defines a single slide for the front page carousel"""
    # Model fields
    title = models.CharField(
        max_length=256,
    )

    background = models.ImageField(
        upload_to='home/update/',
        blank=True,
        null=True,
        help_text='Optional background image',
    )

    icon = models.ImageField(
        upload_to='home/update/',
        help_text='Image for the update icon',
    )

    html = models.TextField(
        blank=True,
        help_text='Any HTML to accompany the update',
    )

    start_date = models.DateField(
        default=django.utils.timezone.now,
        help_text='Date to start displaying the update',
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        help_text='Date to stop displaying the update (leave blank for no end date)',
    )

    priority = models.SmallIntegerField(
        default=1,
        help_text='The priority order to show the slide',
    )

    # Meta settings
    class Meta:
        ordering = ['priority', 'start_date']
        verbose_name = 'Update'
        verbose_name_plural = 'Updates'

    # Methods
    def __str__(self):
        return self.title
