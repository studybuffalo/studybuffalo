from django.db import models
from django.contrib.auth.models import User

"""Planning for the Study Guides
    Acid-Base - Convert to PDF
    Cardiology - PDF
    CDA: PDF
    Circulatory System: Convert to PDF
    Complement cascade: Embeddable link
    Compounding formulary: PDF
    Cytokine Drugs: Convert to PDF
    DSM: Convert to PDF
    Nephron Transport: Convert to PDF
    Opioid Products: Embeddable link
    U of A Text Book Lists: Embeddable link
    Transplant Summary: PDF
    Varicella: Convert to PDF

    - Look into django-guardian for row-level permissions

"""

class Guide(models.Model):
    """Defines the main study guide model"""
    # Model fields
    title = models.CharField(
        help_text="The title of the study guide",
        max_length=100,
    )

    short_description = models.CharField(
        help_text="A short description of the study guide",
        max_length=256,
    )

    long_description = models.TextField(
        blank=True,
        help_text="A longer description of the study guide; supports HTML",
        null=True,
    )

    date_original = models.DateField(
        help_text="The date the first version was released",
    )

    last_update = models.DateField(
        help_text="The date of the last update",
    )

    permissions = models.CharField(
        blank=True,
        choices=(("dsm", "DSM Study Guide"),),
        help_text="If the study guide has any special permissions to access it",
        max_length=3,
        null=True,
    )

    # Meta Statements
    class Meta:
        ordering = ["title"]

    # Methods
    def __str__(self):
        return "{0} (Updated {1})".format(self.title, self.last_update)

    def has_bounty(self):
        return self.bounty_set.all().exists()

class Bounty(models.Model):
    """Defines a bounty on a study guide"""
    # Fields
    study_guide = models.ForeignKey(
        "Guide",
        on_delete=models.CASCADE,
    )

    bounty_status = models.CharField(
        choices=(("o", "Open"), ("c", "Completed"),),
        default="o",
        help_text="The status of the bounty",
        max_length=1,
    )

    bounty_amount = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text="The amount to be awarded on completion of the bounty",
        max_digits=6,
    )

    bounty_details = models.TextField(
        help_text="The details of the bounty; supports HTML",
    )
    
    # Meta Statements
    class Meta:
        ordering = ["study_guide", "bounty_status"]

    # Methods
    def __str__(self):
        return "${0} bounty on {1}".format(self.bounty_amount, self.study_guide)


class BountyAssignment(models.Model):
    """Defines the assignment of a user to a bounty"""
    bounty = models.ForeignKey(
        "Bounty",
        on_delete=models.CASCADE
    )

    assignment_status = models.CharField(
        choices=(("i", "In progress"), ("r", "Rewarded")),
        help_text="The current status of the user's work on the bounty",
        max_length=1,
    )

    assigned_user = models.ForeignKey(
        User,
        help_text="The user assigned to this bounty",
        on_delete=models.CASCADE,
    )

    proportion = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text="The proprtion of the bounty award the user received",
        max_digits=3,
    )
    
    # Meta Statements
    class Meta:
        ordering = ["bounty", "proportion", "assigned_user"]

    # Methods
    def __str__(self):
        return "{0} assigned to {1}".format(self.bounty, self.assigned_user)


class HTMLGuide(models.Model):
    """Defines an HTML study guide"""
    study_guide = models.ForeignKey(
        "Guide",
        on_delete=models.CASCADE,
    )

    html = models.TextField(
        help_text="The HTML content to display the guide"
    )
    
    # Meta Statements

    # Methods
    def __str__(self):
        return "HTML for {0}".format(self.study_guide)


class DocumentGuide(models.Model):
    """Defines a document study guide"""
    study_guide = models.ForeignKey(
        "Guide",
        on_delete=models.CASCADE,
    )

    document = models.FileField(
        help_text="The study guide file to upload (PDF preferred)",
        upload_to="study_guides",
    )
    
    # Meta Statements

    # Methods
    def __str__(self):
        return "Document for {0}".format(self.study_guide)
