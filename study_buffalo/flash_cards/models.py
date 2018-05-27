from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.db import models
from django.utls import timezone


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
    history = HistorialRecords()

class MatchingAnswer(models.Model):
    SIDE_CHOICES = (
        ('l', 'Left'),
        ('r', 'Right'),
    )

    question_container = models.ForeignKey(
        MultipleChoiceContainer,
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
        MatchingAnswer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    history = HistoricalRecords()

class Card(models.Model):
    question = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    ),
    answer_multiple_choice = models.ForeignKey(
        MultipleChoiceContainer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    answer_matching = models.ForeignKey(
        MatchingAnswer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    answer_freeform = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    rationale = models.ForeignKey(
        PartContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    reviewed = models.BooleanField(
        default=False,
    )
    active = models.BooleanField(
        default=False,
    )
    date_modified = models.DateField(
        default=timezone.now
    )
    date_reviewed = models.DateField(
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
    deck_name = models.CharField(
        max_length=255,
    )
    reviewed = models.BooleanField(
        default=False,
    )
    active = models.BooleanField(
        default=False,
    )
    date_modified = models.DateField(
        default=timezone.now
    )
    date_reviewed = models.DateField(
        default=timezone.now
    )
    history = HistoricalRecords()

class CardDeck(models.Model):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.SET_NULL,
        null=True,
    )
    card = model.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
    )
    history = HistoricalRecords()

class Tag(models.Model):
    tag_name = models.CharField(
        max_length=100,
    )
    history = HistoricalRecords()

class Synonym(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    synonym_name = models.CharField(
        max_length=100,
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
    tag = model.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

class DeckStats(models.Model):
    user = models.ForeignKey(
        get_user_model,
        on_delete=models.CASCADE,
    )
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
    )
    date_completed = models.DateField(
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
        get_user_model,
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
        get_user_model,
        blank=True,
        null=True,
        default=None,
    )
    date_submitted = models.DateField(
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
