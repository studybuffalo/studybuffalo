from django.db import models
from django.core.validators import MaxValueValidator

from datetime import datetime

# Create your models here.

class AppData(models.Model):
    """Records information on apps to collect log data on"""
    name = models.CharField(
        help_text="Name of the application to be monitored",
    )

    log_location = models.CharField(
        help_text="Absolute directory containing the log file(s)",
    )

    file_name = models.CharField(
        help_text="Regex expression that matches the log file name(s)",
    )

    flag_start = models.CharField(
        blank=True,
        help_text=(
            "Text located in the log file that notes the application has "
            "started properly"
        ),
        null=True,
    )
    
    flag_end = models.CharField(
        blank=True,
        help_text=(
            "Text located in the log file that notes the application has "
            "finished properly"
        ),
        null=True,
    )

    review_minute = models.PositiveSmallIntegerField(
        blank=True,
        help_text="The minutes of an hour to update on",
        null=True,
        validators=[
            MaxValueValidator(59),
        ]
    )

    review_hour = models.PositiveSmallIntegerField(
        blank=True,
        help_text="The hour of the day to update on (0 = midnight)",
        null=True,
        validators=[
            MaxValueValidator(59),
        ]
    )

    review_day = models.PositiveSmallIntegerField(
        blank=True,
        help_text="The day of the month to update on (1-31)",
        null=True,
        validators=[
            MaxValueValidator(59),
        ]
    )

    review_month = models.PositiveSmallIntegerField(
        blank=True,
        help_text="The month to update on (1 = January, 12 = December)",
        null=True,
        validators=[
            MaxValueValidator(59),
        ]
    )

    review_weekday = models.PositiveSmallIntegerField(
        blank=True,
        help_text="The weekday to update on (0 = Sunday, 6 = Saturday)",
        null=True,
        validators=[
            MaxValueValidator(6),
        ]
    )
    
    next_review = models.DateTimeField(
        default=datetime.now(),
    )

    last_reviewed_log = models.DateTimeField(
        default=datetime.now(),
    )

    last_review = models.DateTimeField(
        auto_now=True,
    )

class LogEntry(models.Model):
    """Records a single log entry on an app"""
    
    app_name = models.ForeignKey(
        AppData,
        help_text="The app this entry is for",
    )

    asc_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    created = models.TimeField(
        blank=True,
        null=True,
    )

    exc_info = models.TextField(
        blank=True,
        null=True,
    )

    file_name = models.CharField(
        blank=True,
        null=True,
    )

    func_name = models.CharField(
        blank=True,
        null=True,
    )

    level_name = models.CharField(
        blank=True,
        null=True,
    )

    level_no = models.CharField(
        blank=True,
        null=True,
    )

    line_no = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    module = models.CharField(
        blank=True,
        null=True,
    )

    msecs = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    message = models.TextField(
        blank=True,
        null=True,
    )

    name = models.CharField(
        blank=True,
        null=True,
    )

    path_name = models.CharField(
        blank=True,
        null=True,
    )

    process = models.CharField(
        blank=True,
        null=True,
    )

    process_name = models.CharField(
        blank=True,
        null=True,
    )

    relative_created = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    stack_info = models.TextField(
        blank=True,
        null=True,
    )

    thread = models.CharField(
        blank=True,
        null=True,
    )

    thread_name = models.CharField(
        blank=True,
        null=True,
    )

"""Matching Django DB names against logging formatter names
        asc_time            asctime         %(asctime)s
        created             created	        %(created)f
        exc_info            exc_info
        file_name           filename	    %(filename)s
        func_name           funcName	    %(funcName)s
        level_name          levelname	    %(levelname)s
        level_no            levelno	        %(levelno)s
        line_no             lineno	        %(lineno)d
        message             message	        %(message)s
        module              module	        %(module)s
        msecs               msecs	        %(msecs)d
        name                name	        %(name)s
        path_name           pathname        %(pathname)s
        process             process	        %(process)d
        process_name        processName     %(processName)s
        relative_created    relativeCreated %(relativeCreated)d
        stack_info          stack_info
        thread              thread	        %(thread)d
        thread_name         threadName	    %(threadName)s
    """