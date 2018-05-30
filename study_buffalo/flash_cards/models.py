import os
import uuid

from simple_history.models import HistoricalRecords

from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseAbstractModel(models.Model):
    '''Container to hold one or more parts'''
    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    history = HistoricalRecords(
        inherit=True,
    )

    class Meta:
        abstract = True

    # def __str__(self):
    #     # Get all the parts of the question
    #     text_parts = PartContainer.objects.get(id=self.id).textpart_set.all().values_list('order', 'text')
    #     media_parts = PartContainer.objects.get(id=self.id).mediapart_set.all().values_list('order', 'media_type')

    #     # Combined parts by order
    #     parts = []

    #     for part in text_parts:
    #         parts.insert(part[0], part[1])

    #     for part in media_parts:
    #         parts.insert(part[0], '<{}>'.format(part[1]))

    #     combined_parts = ' '.join(parts)

    #     # Truncate parts if length is too long
    #     if len(combined_parts) > 50:
    #         return_string = '{}...'.format(combined_parts[:47])
    #     else:
    #         return_string = combined_parts

    #     return return_string

class AbstractPart(BaseAbstractModel):
    '''Abstract model to construct parts'''
    MEDIA_TYPES = (
        ('a', 'Audio'),
        ('i', 'Image'),
        ('t', 'Text'),
        ('v', 'Video'),
    )

    order = models.PositiveIntegerField(
        default=1,
    )
    media_type = models.CharField(
        max_length=1,
        choices=MEDIA_TYPES,
        default='t',
    )
    text = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
    )
    media = models.FileField(
        upload_to='flash_cards/',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.media_type == 't':
            if len(self.text) > 40:
                return_string = '{}...'.format(self.text[:37])
            else:
                return_string = self.text
        else:
            if self.media_type == 'a':
                return_string = 'audio'
            elif self.media_type == 'i':
                return_string = 'image'
            else:
                return_string = 'video'

            file_name, file_extension = os.path.splitext(self.media.path)

            if len(file_name) > 32:
                return_string = '<{} {}... {}>'.format(
                    return_string, file_name[:32], file_extension
                )
            else:
                return_string = '<{} {}{}>'.format(
                    return_string, file_name, file_extension
                )

        return return_string

class Tag(models.Model):
    tag_name = models.CharField(
        max_length=100,
        primary_key=True,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.tag_name

class Synonym(models.Model):
    synonym_name = models.CharField(
        max_length=100,
        primary_key=True,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='synonyms',
    )
    history = HistoricalRecords()

    def __str__(self):
        return '{} (synonym for {})'.format(self.synonym_name, self.tag)

class Deck(BaseAbstractModel):
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
    tags = models.ManyToManyField(
        Tag,
        through='DeckTag',
    )

    def __str__(self):
        return self.deck_name

class Card(BaseAbstractModel):
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
    tags = models.ManyToManyField(
        Tag,
        through='CardTag',
    )
    decks = models.ManyToManyField(
        Deck,
        through='CardDeck',
    )

    def __str__(self):
        question_parts = str(self.question_parts.all().first())

        if self.multiple_choice_answers.exists():
            question_type = 'multiple choice'
            max_length = 20
        elif self.multiple_choice_answers.exists():
            question_type = 'matching'
            max_length = 29
        else:
            question_type = 'freeform'
            max_length = 29

        if len(question_parts) > max_length:
            return '{}... ({})'.format(question_parts[:max_length - 3], question_type)

        return '{} ({})'.format(question_parts, question_type)

class QuestionPart(AbstractPart):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='question_parts'
    )

class MultipleChoiceAnswer(BaseAbstractModel):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='multiple_choice_answers',
    )
    order = models.PositiveIntegerField(
        default=1,
    )
    correct = models.BooleanField(
        default=False,
    )

    def __str__(self):
        parts = MultipleChoiceAnswer.objects.get(id=self.id).multiple_choice_answer_parts.order_by('order')

        part_strings = []

        for part in parts:
            part_strings.append('{}) {}'.format(self.order, str(part)))

        part_string = ' '.join(part_strings)

        if len(part_string) > 40:
            return '{}...'.format(part_string[:37])
        else:
            return part_string

class MultipleChoiceAnswerPart(AbstractPart):
    multiple_choice_answer = models.ForeignKey(
        MultipleChoiceAnswer,
        on_delete=models.CASCADE,
        related_name='multiple_choice_answer_parts',
    )

class MatchingAnswer(BaseAbstractModel):
    SIDE_CHOICES = (
        ('l', 'Left'),
        ('r', 'Right'),
    )

    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='matching_answers',
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

    def __str__(self):
        parts = MatchingAnswer.objects.get(id=self.id).matching_answer_parts.order_by('order')

        part_strings = []

        for part in parts:
            part_strings.append('{}{}) {}'.format(self.side.upper(), self.order, str(part)))

        part_string = ' '.join(part_strings)

        if len(part_string) > 40:
            return '{}...'.format(part_string[:37])

        return part_string

class MatchingAnswerPart(AbstractPart):
    matching_answer = models.ForeignKey(
        MatchingAnswer,
        on_delete=models.CASCADE,
        related_name='matching_answer_parts',
    )

class FreeformAnswerPart(AbstractPart):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='freeform_answer_parts',
    )

class RationalePart(AbstractPart):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='rationale_parts',
    )

class Reference(BaseAbstractModel):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='references',
    )
    reference = models.TextField(
        max_length=500,
    )

    def __str__(self):
        if len(self.reference) > 50:
            reference = '{}...'.format(self.reference[:47])
        else:
            reference = self.reference

        return reference

class CardDeck(BaseAbstractModel):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
    )

class CardTag(BaseAbstractModel):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

class DeckStats(BaseAbstractModel):
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

    def __str__(self):
        return '{} stats for {}'.format(
            str(self.deck),
            str(self.user)
        )

class DeckTag(BaseAbstractModel):
    deck = models.ForeignKey(
        Deck,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

class UserStats(BaseAbstractModel):
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

    def __str__(self):
        return 'Stats for {}'.format(str(self.user))

class Feedback(BaseAbstractModel):
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
