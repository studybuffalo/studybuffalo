"""Serializers for the Drug Price Calculator API."""
from sentry_sdk import capture_message

from rest_framework import serializers

from hc_dpd import models
