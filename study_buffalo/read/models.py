"""Models for the Read app."""
from django.db import models
from django.urls import reverse


class Publication(models.Model):
    """Defines the main publication model"""
    title = models.CharField(
        help_text='The title of the study guide',
        max_length=100,
    )
    description = models.CharField(
        help_text='A short description of the study guide',
        max_length=256,
    )
    date_published = models.DateField(
        help_text='The date the first version was released',
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.date_published} - {self.title}'

    def get_absolute_url(self):
        """Returns the URL to this page"""
        return reverse('pub_page', args=[str(self.id)])


class HTMLPublication(models.Model):
    """Defines an HTML publication"""
    publication = models.ForeignKey(
        'Publication',
        on_delete=models.CASCADE,
    )
    html = models.TextField(
        help_text='The HTML content to display the publication'
    )

    def __str__(self):
        return f'HTML for {self.publication}'


class DocumentPublication(models.Model):
    """Defines a document study guide"""
    publication = models.ForeignKey(
        'Publication',
        on_delete=models.CASCADE,
    )
    document = models.FileField(
        help_text='The publicationfile to upload (PDF preferred)',
        upload_to='publications',
    )

    def __str__(self):
        return f'Document for {self.publication}'
