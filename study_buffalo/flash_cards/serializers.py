from rest_framework import serializers

from django.utils import timezone

from flash_cards.models import Card, Deck, Tag, Synonym

class PartSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000, required=False)
    image = serializers.ImageField(required=False)
    audio = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    order = serializers.IntegerField(default=1, min_value=1)
    def validate(self, date):
        # Check that one part type is provided
        provided = (
            1 if data['text'] else 0
            + 1 if data['image'] else 0
            + 1 if data['audio'] else 0
            + 1 if data['video'] else 0
        )

        if provided == 0:
            raise serializers.ValidationError('Must submit 1 type of content')
        elif provided > 1:
            raise serializers.ValidationError('Must submit only 1 type of content')

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
    order = serializers.IntegerField(default=1, min_value=1)
    side = serializers.ChoiceField(choices=SIDE_CHOICES)
    pair = serializers.IntegerField(default=1, min_value=1)

class AnswerSerializer(serializers.Serializer):
    multiple_choice = MultipleChoiceSerializer(many=True, required=False)
    matching = MatchingSerializer(many=True, required=False)
    freeform = PartSerializer(many=True, required=False)

class ReferenceSerializer(serializers.Serializer):
    reference = serializers.CharField(required=False, max_length=500)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name')

class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ('deck_uuid', 'deck_name', 'reviewed', 'active', 'date_modified', 'date_reviewed')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = (
            'question', 'answer_multiple_choice', 'answer_matching', 'answer_freefrom',
            'rationale', 'reviewed', 'active', 'date_modified', 'date_reviewed'
        )


class NewCardSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    deck = DeckSerializer(many=True)
    question = PartSerializer(many=True)
    answer = AnswerSerializer()
    rationale = PartSerializer(many=True)
    reviewed = serializers.BooleanField(default=False)
    active = serializers.BooleanField(default=False)
    date_modified = serializers.DateField(default=timezone.now)
    date_reviewed = serializers.DateField(default=timezone.now)
    reference = ReferenceSerializer(many=True)
    tag = TagSerializer(many=True)
