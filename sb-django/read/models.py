from django.db import models

class Publication(models.Model):
    """Defines the main publication model"""
    # Model fields
    title = models.CharField(
        help_text="The title of the study guide",
        max_length=100,
    )

    description = models.CharField(
        help_text="A short description of the study guide",
        max_length=256,
    )

    date_published = models.DateField(
        help_text="The date the first version was released",
    )

    # Meta Statements
    class Meta:
        ordering = ["title"]

    # Methods
    def __str__(self):
        return "{0} - {1})".format(self.date, self.title)

class HTMLPublication(models.Model):
    """Defines an HTML publication"""
    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
    )

    html = models.TextField(
        help_text="The HTML content to display the publication"
    )
    
    # Meta Statements

    # Methods
    def __str__(self):
        return "HTML for {0}".format(self.study_guide)


class DocumentPublication(models.Model):
    """Defines a document study guide"""
    publication = models.ForeignKey(
        "Publication",
        on_delete=models.CASCADE,
    )

    document = models.FileField(
        help_text="The publicationfile to upload (PDF preferred)",
        upload_to="publications",
    )
    
    # Meta Statements

    # Methods
    def __str__(self):
        return "Document for {0}".format(self.study_guide)
