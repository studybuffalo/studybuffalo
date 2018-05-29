# pylint: disable=abstract-method,arguments-differ
from rest_framework import serializers

from django.utils import timezone

from flash_cards.models import (
    Card, Deck, Tag, Synonym, PartContainer, MediaPart, TextPart, CardDeck, Reference, CardTag
)

class PartSerializer(serializers.Serializer):
    audio = serializers.FileField(required=False, default=None)
    image = serializers.ImageField(required=False, default=None)
    text = serializers.CharField(max_length=2000, required=False, default=None)
    video = serializers.FileField(required=False, default=None)
    order = serializers.IntegerField(default=1, min_value=1)

    def validate(self, data):
        # Check that one part type is provided
        provided = (
            (1 if data['audio'] else 0)
            + (1 if data['image'] else 0)
            + (1 if data['text'] else 0)
            + (1 if data['video'] else 0)
        )

        if provided == 0:
            raise serializers.ValidationError('Must submit 1 type of content.')
        elif provided > 1:
            raise serializers.ValidationError('Must submit only 1 type of content.')

        return data

class MultipleChoiceSerializer(serializers.Serializer):
    content = PartSerializer(many=True)
    order = serializers.IntegerField(default=1, min_value=1)
    correct = serializers.BooleanField(default=False)

class MatchingSerializer(serializers.Serializer):
    SIDE_CHOICES = (
        ('l', 'Left'),
        ('r', 'Right'),
    )

    content = PartSerializer(many=True)
    side = serializers.ChoiceField(choices=SIDE_CHOICES)
    order = serializers.IntegerField(default=1, min_value=1)
    pair = serializers.IntegerField(default=1, min_value=1)

class AnswerSerializer(serializers.Serializer):
    multiple_choice = MultipleChoiceSerializer(many=True, required=False)
    matching = MatchingSerializer(many=True, required=False)
    freeform = PartSerializer(many=True, required=False)

    def validate(self, data):
        # Check that only 1 answer type is provided
        provided = (
            (1 if 'multiple_choice' in data else 0)
            + (1 if 'matching' in data else 0)
            + (1 if 'freeform' in data else 0)
        )

        if provided == 0:
            raise serializers.ValidationError('Must provide an answer.')
        elif provided > 1:
            raise serializers.ValidationError('Must submit only one answer type.')

        return data

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name', )

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ('synonym_name', 'tag')

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('reference', 'card')

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ('deck_uuid', 'deck_name', 'reviewed', 'active', 'date_modified', 'date_reviewed')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'question', 'answer_multiple_choice', 'answer_matching', 'answer_freeform',
            'rationale', 'reviewed', 'active', 'date_modified', 'date_reviewed'
        )

class NewCardSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    question = PartSerializer(many=True)
    answer = AnswerSerializer()
    rationale = PartSerializer(many=True)
    reviewed = serializers.BooleanField(default=False)
    active = serializers.BooleanField(default=False)
    date_modified = serializers.DateTimeField(default=timezone.now)
    date_reviewed = serializers.DateTimeField(default=None)
    decks = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
    )
    references = serializers.ListField(
        child=serializers.CharField(max_length=500),
        min_length=1,
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
    )

    def create(self, validated_data):
        def assemble_part_container(parts):
            container = PartContainer.objects.create()

            for part in parts:
                if part['audio']:
                    MediaPart.objects.create(
                        container=container,
                        order=part['order'],
                        media=part['audio'],
                        media_type='a'
                    )
                elif part['image']:
                    MediaPart.objects.create(
                        container=container,
                        order=part['order'],
                        media=part['image'],
                        media_type='i'
                    )
                elif part['text']:
                    TextPart.objects.create(
                        container=container,
                        order=part['order'],
                        text=part['text']
                    )
                elif part['video']:
                    MediaPart.objects.create(
                        container=container,
                        order=part['order'],
                        media=part['video'],
                        media_type='v'
                    )

            return container

        # Assemble the question
        question = assemble_part_container(validated_data['question'])

        # Create the answer
        if 'multiple_choice' in validated_data['answer']:
            answer_multiple_choice = None
            answer_matching = None
            answer_freeform = None
        elif 'matching' in validated_data['answer']:
            answer_matching = None
            answer_multiple_choice = None
            answer_freeform = None
        elif 'freeform' in validated_data['answer']:
            answer_freeform = assemble_part_container(validated_data['answer']['freeform'])
            answer_multiple_choice = None
            answer_matching = None

        # Create the rationale
        if validated_data['rationale']:
            rationale = assemble_part_container(validated_data['rationale'])

        # Create all the new models
        card = Card.objects.create(
            question=question,
            answer_multiple_choice=answer_multiple_choice,
            answer_matching=answer_matching,
            answer_freeform=answer_freeform,
            rationale=rationale,
        )

        # Add the card to any specified decks
        for deck in validated_data['decks']:
            CardDeck.objects.create(
                deck=Deck.objects.get(deck_uuid=deck),
                card=card
            )

        # Retrieve and create the tags
        for tag in validated_data['tags']:
            synonym = Synonym.objects.filter(synonym_name=tag)

            # Synonym found, match tag to card
            if synonym:
                CardTag.objects.create(
                    card=card,
                    tag=synonym[0].tag,
                )

            # New synonym/tag; create tag to match to card
            else:
                new_tag = Tag.objects.create(
                    tag_name=tag
                )
                Synonym.objects.create(
                    tag=new_tag,
                    synonym_name=tag,
                )
                CardTag.objects.create(
                    card=card,
                    tag=new_tag,
                )

        # Add any references for this card
        for reference in validated_data['references']:
            Reference.objects.create(
                card=card,
                reference=reference,
            )

        return validated_data

    def validate_question(self, data):
        if not data:
            raise serializers.ValidationError('A question is required.')

        return data

    def validate_decks(self, data):
        for deck in data:
            if Deck.objects.filter(deck_uuid=deck).exists() is False:
                raise serializers.ValidationError('Specified deck does not exist.')

        return data
