# pylint: disable=redefined-builtin

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics

from django.db.models import Q

from flash_cards.models import Card, Deck, Tag, Synonym
from flash_cards.api.serializers import (
    CardSerializer, DeckSerializer, TagSerializer, SynonymSerializer,
)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_root(request, format=None):
    return Response({
        'cards': reverse('flash_cards:api_v1:card_list', request=request, format=format),
        'decks': reverse('flash_cards:api_v1:deck_list', request=request, format=format),
        'tags': reverse('flash_cards:api_v1:tag_list', request=request, format=format),
    })

class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CardSerializer

class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = CardSerializer
    lookup_field = 'id'

class DeckList(generics.ListCreateAPIView):
    queryset = Deck.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DeckSerializer

    def get_queryset(self):
        # Get the search parameters
        owner = self.request.query_params.get('owner', False)
        text_filter = self.request.query_params.get('text_filter', '')

        if owner:
            user = self.request.user.id

            # Get the initial queryset
            deck_history = Deck.history.select_related().all()

            # Get all the appropriate deck IDs
            deck_ids = deck_history.filter(history_user=user).values_list('id', flat=True)

            # Remove duplicates
            deck_ids = list(set(deck_ids))

            # Get the deck queryset
            queryset = Deck.objects.filter(id__in=deck_ids)
        else:
            queryset = Deck.objects.all()

        if text_filter:
            queryset = queryset.filter(
                Q(deck_name__icontains=text_filter) | Q(description__icontains=text_filter)
            )

        return queryset

class DeckDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DeckSerializer
    lookup_field = 'id'

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = TagSerializer
    lookup_field = 'tag_name'

class SynonymDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Synonym.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = SynonymSerializer
    lookup_field = 'synonym_name'
