from rest_framework import serializers

from flash_cards.models import Tag, Synonym

class TagSerializer(serializers.HyperlinkedModelSerializer):
    synonym_set = serializers.HyperlinkedRelatedField(many=True, view_name='synonym-detail', read_only=True)

    class Meta:
        model = Tag
        fields = ('url', 'tag_name', 'synonym_set')

class SynonymSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Synonym
        fields = ('synonym_name', 'tag')
