from django.db import models
import django.utils.timezone
import os

class CarouselSlide(models.Model):
    """Defines a single slide for the front page carousel"""
    # Model fields
    background = models.ImageField(upload_to="home/carousel/",
                                   blank=True,
                                   null=True,
                                   help_text="Optional background image for the slide",)

    html = models.TextField(blank=True,
                            help_text="Any HTML to accompany the carousel slide",)

    start_date = models.DateField(default=django.utils.timezone.now,
                                  help_text="Date to start displaying the slide",)

    end_date = models.DateField(blank=True,
                                null=True,
                                help_text="Date to stop display the slide (leave blank for no end date)",)

    priority = models.SmallIntegerField(default=1,
                                        help_text="The priority order to show the slide",)

    # Meta settings
    class Meta:
        ordering = ["priority", "start_date"]
        verbose_name = "Carousel Slide"
        verbose_name_plural = "Carousel Slides"

    # Methods
    def __str__(self):
        outputStr = "{0}".format(self.start_date)

        if self.end_date:
            outputStr = "{0} - {1}".format(outputStr, self.end_date)

        if self.background:
            outputStr = "{0} ({1})".format(outputStr, 
                                           os.path.basename(self.background.name))

        return outputStr