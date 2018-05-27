import uuid

from simple_history.models import HistoricalRecords

from django.conf import settings
from django.db import models
from django.utils import timezone


class PartContainer(models.Model):
    '''Container to hold one or more parts'''
    history = HistoricalRecords()

class AbstractPart(models.Model):
    '''Abstract model to construct parts'''
    container = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(
        default=1,
    )
    history = HistoricalRecords()

    class Meta:
        abstract = True

class TextPart(AbstractPart):
    text = models.TextField(
        max_length=2000,
    )
    history = HistoricalRecords()

class MediaPart(AbstractPart):
    MEDIA_TYPES = (
        ('i', 'Image'),
        ('a', 'Audio'),
        ('v', 'Video'),
    )

    media_type = models.CharField(
        max_length=1,
        choices=MEDIA_TYPES,
        default='i',
    )
    media = models.FileField(
        upload_to='flash_cards/',
    )
    history = HistoricalRecords()

class MultipleChoiceContainer(models.Model):
    '''Container for multiple choice answers'''
    history = HistoricalRecords()

class MultipleChoiceAnswer(models.Model):
    container = models.ForeignKey(
        MultipleChoiceContainer,
        on_delete=models.CASCADE,
    )
    part_container = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(
        default=1,
    )
    correct = models.BooleanField(
        default=False,
    )
    history = HistoricalRecords()

class MatchingContainer(models.Model):
    '''Container for matching answers'''
    history = HistoricalRecords()

class MatchingAnswer(models.Model):
    SIDE_CHOICES = (
        ('l', 'Left'),
        ('r', 'Right'),
    )

    question_container = models.ForeignKey(
        MatchingContainer,
        on_delete=models.CASCADE,
    )
    part_container = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    )
    side = models.CharField(
        max_length=1,
        choices=SIDE_CHOICES,
        default='l',
    )
    order = models.PositiveIntegerField(
        default=1,
    )
    pair = models.ForeignKey(
        'MatchingAnswer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

class Card(models.Model):
    card_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    question = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    ),
    answer_multiple_choice = models.ForeignKey(
        MultipleChoiceContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    answer_matching = models.ForeignKey(
        MatchingAnswer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    answer_freeform = models.ForeignKey(
        PartContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    rationale = models.ForeignKey(
        PartContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='answer_rationale',
    )
    reviewed = models.BooleanField(
        default=False,
    )
    active = models.BooleanField(
        default=True,
    )
    date_modified = models.DateTimeField(
        default=timezone.now
    )
    date_reviewed = models.DateTimeField(
        default=timezone.now
    )
    history = HistoricalRecords()

class Reference(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
    )
    reference = models.TextField(
        max_length=500,
    )
    history = HistoricalRecords()

class Deck(models.Model):
    deck_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    deck_name = models.CharField(
        max_length=255,
    )
    reviewed = models.BooleanField(
        default=False,
    )
    active = models.BooleanField(
        default=True,
    )
    date_modified = models.DateTimeField(
        default=timezone.now
    )
    date_reviewed = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )
    history = HistoricalRecords()

class CardDeck(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.SET_NULL,
        null=True,
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
    )
    history = HistoricalRecords()

class Tag(models.Model):
    tag_name = models.CharField(
        max_length=100,
        unique=True,
    )
    history = HistoricalRecords()

class Synonym(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    synonym_name = models.CharField(
        max_length=100,
        unique=True,
    )
    history = HistoricalRecords()

class CardTag(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

class TagDeck(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

class DeckStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
    )
    date_completed = models.DateTimeField(
        default=timezone.now
    )
    number_questions = models.IntegerField(
        default=0,
    )
    number_correct = models.IntegerField(
        default=0,
    )
    number_partially_correct = models.IntegerField(
        default=0,
    )
    number_incorrect = models.IntegerField(
        default=0,
    )
    history = HistoricalRecords()

class UserStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    number_sets = models.IntegerField(
        default=0,
    )
    number_questions = models.IntegerField(
        default=0,
    )
    number_correct = models.IntegerField(
        default=0,
    )
    number_partially_correct = models.IntegerField(
        default=0,
    )
    number_incorrect = models.IntegerField(
        default=0,
    )
    history = HistoricalRecords()

class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        default=None,
        null=True,
    )
    date_submitted = models.DateTimeField(
        default=timezone.now
    )
    comment = models.TextField(
        max_length = 2000,
    )
    history = HistoricalRecords()

    class Meta:
        abstract = True

class CardFeedback(Feedback):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE
    )

class DeckFeedback(Feedback):
    Deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE
    )
