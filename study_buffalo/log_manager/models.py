from django.db import models
from django.utils import timezone

import pytz

# Create your models here.

class AppData(models.Model):
    """Records information on apps to collect log data on"""
    name = models.CharField(
        help_text="Name of the application to be monitored",
        max_length = 256,
    )

    log_location = models.CharField(
        help_text="Absolute directory containing the log file(s)",
        max_length = 512,
    )

    file_name = models.CharField(
        help_text="Regex expression that matches the log file name(s)",
        max_length = 512,
    )

    monitor_start = models.BooleanField(
        default=False,
        help_text=(
            "Whether to notify the user or not if there are no new log"
            "entries when the log monitor checks at the specified time"
        )
    )
    
    asc_time_format = models.CharField(
        help_text="The format of the asc_time field",
        max_length=50,
    )

    TIMEZONE_LIST = []

    for tz in pytz.common_timezones:
        TIMEZONE_LIST.append((tz, tz))

    log_timezone = models.CharField(
        blank=True,
        choices = TIMEZONE_LIST,
        help_text="What timezone this log file uses for times",
        max_length=35,
        null=True,
    )

    review_minute = models.CharField(
        blank=True,
        default="*",
        help_text="The minutes of an hour to update on",
        max_length=100,
        null=True
    )

    review_hour = models.CharField(
        blank=True,
        default="*",
        help_text="The hour of the day to update on (0 = midnight)",
        max_length=100,
        null=True
    )

    review_day = models.CharField(
        blank=True,
        default="*",
        help_text="The day of the month to update on (1-31)",
        max_length=100,
        null=True
    )

    review_month = models.CharField(
        blank=True,
        default="*",
        help_text="The month to update on (1 = January, 12 = December)",
        max_length=100,
        null=True
    )

    review_weekday = models.CharField(
        blank=True,
        default="*",
        help_text="The weekday to update on (0 = Sunday, 6 = Saturday)",
        max_length=100,
        null=True
    )
    
    next_review = models.DateTimeField(
        default=timezone.now,
    )

    last_reviewed_log = models.DateTimeField(
        default=timezone.now,
    )

    last_review = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("can_view", "Can view the app log data"),
        )

class LogEntry(models.Model):
    """Records a single log entry on an app"""
    
    app_name = models.ForeignKey(
        AppData,
        help_text="The app this entry is for",
        on_delete=models.CASCADE,
    )

    asc_time = models.DateTimeField(
        blank=True,
        null=True,
    )

    created = models.CharField(
        blank=True,
        max_length=25,
        null=True,
    )

    exc_info = models.TextField(
        blank=True,
        null=True,
    )

    file_name = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    func_name = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    level_name = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    level_no = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    line_no = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    module = models.CharField(
        blank=True,
        max_length=512,
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
        max_length=512,
        null=True,
    )

    path_name = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    process = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    process_name = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    relative_created = models.CharField(
        blank=True,
        max_length=25,
        null=True,
    )

    stack_info = models.TextField(
        blank=True,
        null=True,
    )

    thread = models.CharField(
        blank=True,
        max_length=512,
        null=True,
    )

    thread_name = models.CharField(
        blank=True,
        max_length=512,
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