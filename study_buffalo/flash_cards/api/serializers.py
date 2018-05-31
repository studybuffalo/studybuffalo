# pylint: disable=abstract-method,arguments-differ
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from flash_cards import models


class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Synonym
        fields = ('synonym_name', )

class TagSerializer(serializers.ModelSerializer):
    synonyms = SynonymSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = models.Tag
        fields = ('tag_name', 'synonyms', )

    def create(self, validated_data):
        # Extract any synonyms
        try:
            synonyms = validated_data.pop('synonyms')
        except KeyError:
            synonyms = []

        # Get the tag_name
        tag_name = validated_data.get('tag_name', '')

        # Add the tag to synonym set
        synonym_set = set([tag_name])

        # Add the synonyms to the set
        for synonym in synonyms:
            synonym_set.add(synonym['synonym_name'])

        # Create the tag
        tag = models.Tag.objects.create(
            tag_name=tag_name,
        )

        # Create the synonyms for this tag
        for synonym in synonym_set:
            models.Synonym.objects.create(
                tag=tag,
                synonym_name=synonym,
            )

        # Retrieve all synonyms to return with the successful response
        validated_data['synonyms'] = tag.synonyms.values('synonym_name')

        return validated_data

    def update(self, instance, validated_data):
        # Update the tag name
        tag_name = validated_data.get('tag_name', instance.tag_name)
        instance.tag_name = tag_name
        instance.save()

        # Add any new synonyms
        try:
            synonyms = validated_data.pop('synonyms')
        except KeyError:
            synonyms = []

        # Add the tag to synonym set
        synonym_set = set([tag_name])

        # Add the synonyms to the set
        for synonym in synonyms:
            synonym_set.add(synonym['synonym_name'])

        # Create any new synonyms
        for synonym in synonym_set:
            models.Synonym.objects.get_or_create(
                tag=instance,
                synonym_name=synonym,
            )

        # Retrieve all synonyms to return with the successful response
        validated_data['synonyms'] = instance.synonyms.values('synonym_name')

        return validated_data

class DeckSerializer(serializers.ModelSerializer):
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

class MultipleChoiceAnswerPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MultipleChoiceAnswerPart
        fields = (
            'order', 'media_type', 'text', 'media',
        )

class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    multiple_choice_answer_parts = MultipleChoiceAnswerPartSerializer(
        many=True,
        required=True,
    )

    class Meta:
        model = models.MultipleChoiceAnswer
        fields = ('order', 'correct', 'multiple_choice_answer_parts', )

class MatchingAnswerPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchingAnswerPart
        fields = (
            'order', 'media_type', 'text', 'media'
        )

class MatchingAnswerSerializer(serializers.ModelSerializer):
    matching_answer_parts = MatchingAnswerPartSerializer(
        many=True,
        required=True,
    )

    class Meta:
        model = models.MatchingAnswer
        fields = ('side', 'order', 'pair', 'matching_answer_parts', )

class FreeformAnswerPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FreeformAnswerPart
        fields = ('order', 'media_type', 'text', 'media', )

class RationalePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RationalePart
        fields = ('order', 'media_type', 'text', 'media')

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        fields = ('reference', )

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
    question_parts = QuestionPartSerializer(many=True, )
    multiple_choice_answers = MultipleChoiceAnswerSerializer(many=True, required=False, )
    matching_answers = MatchingAnswerSerializer(many=True, required=False, )
    freeform_answer_parts = FreeformAnswerPartSerializer(many=True, required=False, )
    rationale_parts = RationalePartSerializer(many=True, required=False, )
    references = ReferenceSerializer(many=True, required=True, )
    tags = TagSerializer(many=True, )
    decks = DeckForCardSerializer(many=True, )

    class Meta:
        model = models.Card
        fields = (
            'id', 'question_parts', 'multiple_choice_answers', 'matching_answers',
            'freeform_answer_parts', 'rationale_parts', 'reviewed', 'active',
            'date_modified', 'date_reviewed', 'references', 'tags', 'decks'
        )
        depth = 2

    def get_or_create_tag(self, validated_data):
        tag_data = validated_data.pop('tags')

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
        reference_data = validated_data.pop('references')
        tags = validated_data.pop('tags')
        decks = validated_data.pop('decks')

        try:
            multiple_choice_data = validated_data.pop('multiple_choice_answers')
        except KeyError:
            multiple_choice_data = []

        try:
            matching_data = validated_data.pop('matching_answers')
        except KeyError:
            matching_data = []

        try:
            freeform_data = validated_data.pop('freeform_answer_parts')
        except KeyError:
            freeform_data = []

        try:
            rationale_data = validated_data.pop('rationale_parts')
        except KeyError:
            rationale_data = []

        # Create the card
        card = models.Card.objects.create(**validated_data)

        # Create the question
        for part in question_data:
            models.QuestionPart.objects.create(card=card, **part)

        # If applicable, create the multiple choice answers
        for answer in multiple_choice_data:
            multiple_choice_answer = models.MultipleChoiceAnswer.objects.create(
                card=card,
                order=answer['order'],
                correct=answer['correct'],
            )

            for part in answer['multiple_choice_answer_parts']:
                models.MultipleChoiceAnswerPart.objects.create(
                    multiple_choice_answer=multiple_choice_answer,
                    **part,
                )

        # If applicable, create the matching answers
        for answer in matching_data:
            matching_answer = models.MatchingAnswer.objects.create(
                card=card,
                side=answer['side'],
                order=answer['order'],
            )

            for part in answer['matching_answer_parts']:
                models.MatchingAnswerPart.objects.create(
                    matching_answer=matching_answer,
                    **part,
                )

        # If applicable, create the freeform answers
        for part in freeform_data:
            models.FreeformAnswerPart.objects.create(
                card=card,
                **part,
            )

        # If applicable, create the rationale
        for part in rationale_data:
            models.RationalePart.objects.create(
                card=card,
                **part,
            )

        # Create the references
        for reference in reference_data:
            models.Reference.objects.create(
                card=card,
                **reference
            )

        # Assign the tags to the card
        for tag in tags:
            models.CardTag.objects.create(
                card=card,
                tag=tag,
            )

        # Assign card to the decks
        for deck in decks:
            models.CardDeck.objects.create(
                card=card,
                deck=models.Deck.objects.get(id=deck['id']),
            )

        return card

    # TODO: Add validation to only allow 1 type of answer
