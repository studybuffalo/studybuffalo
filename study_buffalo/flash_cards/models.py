from django.db import models

from simple_history.models import HistoricalRecords

'''Card Model
    ID
    Question > Part Container IDFK
    MC Answer > MC Container IDFK
    Matching Answer > Matching Container IDFK
    Freeform Answer > Part Container IDFK
    reviewed = True/False
    Active = True/False
    date_modified
    date_reviewed

    Would validate model to ensure only one answer present (others = None)
    Non-null answer determines question type and output
'''

class PartContainer(models.Model):
    '''Container to hold one or more parts'''
    history = HistoricalRecords()

class AbstractPart(models.Model):
    '''Abstract model to construct parts'''
    container = models.ForeignKey(
        to=PartContainer,
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField(
        default=1,
    )
    history = HistoricalRecords()

    class Meta:
        abstract = True

class TextPart(AbstractPart):
    text = models.CharField(
        max_length=2048,
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
        upload_to='flash_cards',
    )
    history = HistoricalRecords()

class MultipleChoiceContainer(models.Model):
    '''Container for multiple choice answers'''
    history = HistoricalRecords()

class MultipleChoiceAnswer(models.Model):
    question_container = models.ForeignKey(
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

'''References Model
    ID
    Card IDFK
    Reference
'''

'''Tag Model
    ID
    tag name
'''

'''Synonym model
    ID
    synonym name
    tag IDFK
'''

'''Set Model
    ID
    Title
    status = reviewed, pending review
    Reviewed = True/False
    Active = True/False
    date_modified
    date_reviewed
'''

'''Set by Card
    ID
    Set IDFK
    Card IDFK
'''

'''Set by tag
    ID
    Set IDFK
    tag IDFK
'''

''' User Stats for Sets
    ID
    user IDFK
    Set IDFK
    date_completed
    # correct
    # partially correct
    # incorrect
    total # of questions
'''

''' User Stats Overall
    Total number of questions answered
    Total number correct
    Total number partially correct
    Total number incorrect
'''

'''Other Stats that can be compiled from models
    Total number questions user has completed and breakdown (from sets model)
    Number of created/modified cards and sets from history
    Current status on deck from the last entry on set
'''
# # Study Buffalo Flash Cards
# ## Overview
# - Users will be presented with flash cards for them to answer in various formats
# - Formats may include multiple choice, fill in the blank, free-form
# - Each individual card could be tagged into multiple collections to generate unique sets
# - Cards and sets can be created by users; users can report any concerns with questions
# - Certain individuals will have the ability to verify cards and resolve concerns (receive fee for this?)
# - Ability will be to have some features monetized (e.g. Mental Health & Movember)
# - Let users set the number of questions they answer
# - Recycle older questions if the user incorrectly answers
# - Leaderboards, personal records?
# - Vast majority of all features will require proper records of changes

# ## Flash Card Design
# - Questions and answers
# 	- Text
# 	- Audio
# 	- Video
# 	- Images

# ## Question Types
# ### Multiple Choice
# - One question
# - Multiple choices, one answer
# - Can be marked either correct or incorrect

# ### Multiple Multiple Choice
# - One question
# - Multiple choices, multiple answers
# - Can be marked either correct, partially correct, or incorrect

# ### Matching
# - Multiple questions
# - Multiple answers
# - Can be marked either correct, partially correct, or incorrect

# ### Freeform
# - One question
# - No answers
# - Marked by user as either correct, partially correct, or incorrect

# ## Cards & Sets
# - Each card has one question type
# - Each card may have multiple "tags"
# - Sets can be made up of specific cards and/or tags

# ## Tags
# - Can be created by the users
# - Tags can have synonyms that map to a single tag
# - Advanced users may merge and consolidate tags

# ## App Functionality for User
# - Users will be required to create an account to continue
# - Users will have ability to study a set, create new cards, and create new sets
# - Users may combine multiple sets to study
# - Users will set number of questions to study in the set
# - Users may set a time limit to the session
# - Study session ends with timer is up or all questions are answered
