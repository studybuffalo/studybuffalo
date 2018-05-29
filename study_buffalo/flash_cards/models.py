import uuid

from simple_history.models import HistoricalRecords

from django.conf import settings
from django.db import models
from django.utils import timezone


class PartContainer(models.Model):
    '''Container to hold one or more parts'''
    history = HistoricalRecords()

    def __str__(self):
        return 'PartContainer'

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

    def __str__(self):
        return '{} - {}'.format(self.order, self.text)

class MediaPart(AbstractPart):
    MEDIA_TYPES = (
        ('a', 'Audio'),
        ('i', 'Image'),
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

    def __str__(self):
        return '{} - {} - {}'.format(self.order, self.media_type, self.media)

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

    def __str__(self):
        return '{}) {} ({})'.format(
            self.order,
            self.part_container,
            'correct' if self.correct else 'incorrect'
        )

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

    def __str__(self):
        return '{}) {} ({})'.format(
            self.order,
            self.part_container,
            'left' if self.side == 'l' else 'right'
        )

class Card(models.Model):
    card_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='card UUID',
    )
    question = models.ForeignKey(
        PartContainer,
        on_delete=models.CASCADE,
    )
    answer_multiple_choice = models.ForeignKey(
        MultipleChoiceContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='multiple choice answer',
    )
    answer_matching = models.ForeignKey(
        MatchingAnswer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='matching answer',
    )
    answer_freeform = models.ForeignKey(
        PartContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='answer_freeform',
        verbose_name='freeform answer',
    )
    rationale = models.ForeignKey(
        PartContainer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='answer_rationale',
        verbose_name='answer rationale',
    )
    reviewed = models.BooleanField(
        default=False,
    )
    active = models.BooleanField(
        default=True,
    )
    date_modified = models.DateTimeField(
        default=timezone.now,
    )
    date_reviewed = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        # Format the question text
        question_string = str(self.question)

        if len(question_string) > 50:
            question = '{}...'.format(question_string[:47])
        else:
            question = question_string

        # Determine the answer type
        answer_type = (
            'multiple choice' if self.answer_multiple_choice else
            'matching' if self.answer_matching else 'freeform'
        )
        return '{} ({})'.format(question, answer_type)

class Reference(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
    )
    reference = models.TextField(
        max_length=500,
    )
    history = HistoricalRecords()

    def __str__(self):
        if len(self.reference) > 50:
            reference = '{}...'.format(self.reference[:50])
        else:
            reference = self.reference

        return reference

class Deck(models.Model):
    deck_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name='deck UUID',
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
        default=timezone.now,
    )
    date_reviewed = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.deck_name

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

    def __str__(self):
        return self.tag_name

class Synonym(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='synonyms',
    )
    synonym_name = models.CharField(
        max_length=100,
        unique=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return '{} (synonym for {})'.format(self.synonym_name, self.tag)

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
        verbose_name='number of questions'
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

    def __str__(self):
        return '{} stats for {}'.format(
            str(self.deck),
            str(self.user)
        )

class UserStats(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    number_decks = models.IntegerField(
        default=0,
        verbose_name='decks completed',
    )
    number_questions = models.IntegerField(
        default=0,
        verbose_name='questions completed',
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

    def __str__(self):
        return 'Stats for {}'.format(str(self.user))

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
        max_length=2000,
    )
    history = HistoricalRecords()

    class Meta:
        abstract = True

class CardFeedback(Feedback):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if len(self.comment) > 50:
            comment = '{}...'.format(self.comment[:47])
        else:
            comment = self.comment

        return '{} feedback: {}'.format(str(self.card), comment)

class DeckFeedback(Feedback):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if len(self.comment) > 50:
            comment = '{}...'.format(self.comment[:47])
        else:
            comment = self.comment

        return '{} feedback: {}'.format(str(self.deck), comment)
