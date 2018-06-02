# pylint: disable=abstract-method,arguments-differ
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from flash_cards import models


class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Synonym
        fields = ('synonym_name', )

class TagSerializer(serializers.Serializer):
    tag_name = serializers.CharField(max_length=100, required=True)
    synonyms = SynonymSerializer(
        many=True,
        required=False,
    )

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

        # Get or create the tag
        try:
            tag = models.Tag.objects.create(
                tag_name=tag_name,
            )
        except IntegrityError:
            raise serializers.ValidationError(
                {'tag_name': ['Tag name "{}" already exists.'.format(tag_name)]}
            )

        # Create the synonyms for this tag (if needed)
        for synonym in synonym_set:
            models.Synonym.objects.get_or_create(
                tag=tag,
                synonym_name=synonym,
            )

        # Retrieve all synonyms to return with the successful response
        validated_data['synonyms'] = tag.synonyms.values('synonym_name')

        return validated_data

    def update(self, instance, validated_data):
        # Update the tag name
        tag_name = validated_data.get('tag_name', instance.tag_name)

        try:
            instance.tag_name = tag_name
            instance.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {'tag_name': ['Tag name "{}" already exists.'.format(tag_name)]}
            )

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


    def validate(self, data):
        # VALIDATION: ensure exactly 1 answer type provided
        # Get any multiple choice answers
        try:
            multiple_choice = data['multiple_choice_answers']
        except KeyError:
            multiple_choice = False

        # Get any matching answers
        try:
            matching = data['matching_answers']
        except KeyError:
            matching = False

        # Get any freeform answers
        try:
            freeform = data['freeform_answer_parts']
        except KeyError:
            freeform = False

        # Total the number of answers
        answer_total = (
            (1 if multiple_choice else 0)
            + (1 if matching else 0)
            + (1 if freeform else 0)
        )

        if answer_total == 0:
            raise serializers.ValidationError('Must provide an answer.')
        elif answer_total > 1:
            raise serializers.ValidationError('Must provide only one answer type.')

        return data

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

    def extract_related_models(self, validated_data):
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

        related_models = {
            'question': question_data,
            'reference': reference_data,
            'tags': tags,
            'decks': decks,
            'multiple_choice': multiple_choice_data,
            'matching': matching_data,
            'freeform': freeform_data,
            'rationale': rationale_data,
        }

        return related_models, validated_data

    def create_related_fields(self, card, related_data):
        # Create the question
        for part in related_data['question']:
            models.QuestionPart.objects.create(card=card, **part)

        # If applicable, create the multiple choice answers
        for answer in related_data['multiple_choice']:
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
        for answer in related_data['matching']:
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
        for part in related_data['freeform']:
            models.FreeformAnswerPart.objects.create(
                card=card,
                **part,
            )

        # If applicable, create the rationale
        for part in related_data['rationale']:
            models.RationalePart.objects.create(
                card=card,
                **part,
            )

        # Create the references
        for reference in related_data['reference']:
            models.Reference.objects.create(
                card=card,
                **reference
            )

        # Assign the tags to the card
        for tag in related_data['tags']:
            models.CardTag.objects.create(
                card=card,
                tag=tag,
            )

        # Assign card to the decks
        for deck in related_data['decks']:
            models.CardDeck.objects.create(
                card=card,
                deck=models.Deck.objects.get(id=deck['id']),
            )

    def delete_related_models(self, card):
        # Delete question
        card.question_parts.all().delete()

        # Delete multiple choice answers
        card.multiple_choice_answers.all().delete()

        # Delete matching answers
        card.matching_answers.all().delete()

        # Delete freeform answer
        card.freeform_answer_parts.all().delete()

        # Delete rationale
        card.rationale_parts.all().delete()

        # Delete references
        card.references.all().delete()

        # Remove references to decks
        card.carddeck_set.all().delete()

        # Remove references to tags
        card.cardtag_set.all().delete()

    def create(self, validated_data):
        self.get_or_create_tag(validated_data)

        # Extract the related models
        related_data, validated_data = self.extract_related_models(validated_data)

        # Create the card
        card = models.Card.objects.create(**validated_data)

        # Create the related models
        self.create_related_fields(card, related_data)

        return card

    def update(self, card, validated_data):
        self.get_or_create_tag(validated_data)

        # Extract the related models
        related_data, validated_data = self.extract_related_models(validated_data)

        # Update the card model
        card.reviewed = validated_data['reviewed']
        card.active = validated_data['active']
        card.date_modified = validated_data['date_modified']
        card.date_reviewed = validated_data['date_reviewed']
        card.save()

        # Delete all the related fields and then repopulate them
        self.delete_related_models(card)

        # Recreate the related models
        self.create_related_fields(card, related_data)

        return card
