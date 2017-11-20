from django.db import models

class Apps(models.Model):
    """List of all Django applications to monitor"""
    app_name = models.CharField(
        help_text="The name of the Django App to include",
        max_length=50,
    )
    model_pending = models.CharField(
        help_text="The model name containing the pending substitutions",
        max_length=50,
    )
    model_sub = models.CharField(
        help_text=(
            "The model name where the verified substitutions should "
            "be added to"
        ),
        max_length=50,
    )

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return self.app_name


class ModelFields(models.Model):
    """List of the model fields to include"""
    app = models.ForeignKey(
        to="Apps",
        on_delete=models.CASCADE
    )
    field_name = models.CharField(
        help_text="A field name from the model to include",
        max_length=50,
    )
    dictionary_check = models.BooleanField(
        default=False,
        help_text="Whether to add a online search button to confirm spelling",
    )

    class meta:
        verbose_name = "Model Field"
        verbose_name_plural = "Model Fields"

    def __str__(self):
        return "{} - {}".format(self.app, self.field_name)