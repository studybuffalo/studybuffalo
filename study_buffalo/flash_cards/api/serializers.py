# pylint: disable=abstract-method,arguments-differ
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.urls import reverse
from flash_cards import models


# TODO: Add Reference Serializer

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Synonym
        fields = ('synonym_name', )

class TagSerializer(serializers.Serializer):
    tag_name = serializers.CharField(
        max_length=100,
    )
    synonyms = SynonymSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = models.Tag
        fields = ('tag_name', 'synonyms', )

    def create(self, validated_data):
        print("Test")

class DeckSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=models.Deck()._meta.get_field('id'))

    class Meta:
        model = models.Deck
        fields = (
            'id', 'deck_name', 'reviewed', 'active', 'date_modified',
            'date_reviewed',
        )

class QuestionPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionPart
        fields = ('order', 'media_type', 'text', 'media')

class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceAnswer
        fields = ('order', 'correct', )

class MatchingAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchingAnswer
        fields = ('side', 'order', 'pair', )

class FreeformAnswerPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FreeformAnswerPart
        fields = ('order', 'media_type', 'text', 'media', )

class RationalePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RationalePart
        fields = ('order', 'media_type', 'text', 'media')

class DeckForCardSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    url = serializers.SerializerMethodField(
        source='get_url'
    )

    def get_url(self, data):
        return self.context.get('request').build_absolute_uri(
            reverse('flash_cards:api_v1:deck_detail', kwargs={'id': data.id})
        )

    def validate_id(self, data):
        # Check that deck exists
        try:
            models.Deck.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Provided deck does not exist: {}'.format(data)
            )

        return data

class CardSerializer(serializers.ModelSerializer):
    question_parts = QuestionPartSerializer(many=True)
    multiple_choice_answers = MultipleChoiceAnswerSerializer(many=True, required=False)
    matching_answers = MatchingAnswerSerializer(many=True, required=False)
    freeform_answers = FreeformAnswerPartSerializer(many=True, required=False)
    rationale_parts = RationalePartSerializer(many=True, required=False)
    tags = TagSerializer(many=True)
    decks = DeckForCardSerializer(many=True)

    class Meta:
        model = models.Card
        fields = (
            'id', 'question_parts', 'multiple_choice_answers', 'matching_answers',
            'freeform_answers', 'rationale_parts', 'reviewed', 'active',
            'date_modified', 'date_reviewed', 'references', 'tags', 'decks'
        )
        depth = 2

    def get_or_create_tag(self, validated_data):
        tag_data = validated_data.pop('tags')

        print(tag_data)

        tags = []

        # Check if this exists in the synonym list
        for tag in tag_data:
            synonym_list = models.Synonym.objects.filter(synonym_name=tag['tag_name'])

            # Synonym exists, retrieve parent tag
            if synonym_list.exists():

                tags.append(synonym_list[0].tag)

            # No synonym; create synonym and tag
            else:
                created_tag = models.Tag.objects.create(
                    tag_name=tag['tag_name'],
                )
                models.Synonym.objects.create(
                    tag=created_tag,
                    synonym_name=tag['tag_name'],
                )

                tags.append(created_tag)

        validated_data['tags'] = tags

    def create(self, validated_data):
        self.get_or_create_tag(validated_data)

        # Extract the related models
        question_data = validated_data.pop('question_parts')
        tags = validated_data.pop('tags')
        decks = validated_data.pop('decks')

        # Create the card
        card = models.Card.objects.create(**validated_data)

        # Create the question
        for part in question_data:
            models.QuestionPart.objects.create(card=card, **part)

        # Assign the tags to the card
        for tag in tags:
            models.CardTag.objects.create(
                card=card,
                tag=tag,
            )

        # Assign card to the decks
        for deck in decks:
            print(deck)
            models.CardDeck.objects.create(
                card=card,
                deck=models.Deck.objects.get(id=deck['id']),
            )

        return card
