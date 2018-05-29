# pylint: disable=redefined-builtin

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status, generics

from .models import Card, Deck, Tag, Synonym, Reference
from .api.serializers import CardSerializer, NewCardSerializer, DeckSerializer, TagSerializer, SynonymSerializer, ReferenceSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_root(request, format=None):
    return Response({
        'cards': reverse('flash_cards:api_v1:card_list', request=request, format=format),
        'decks': reverse('flash_cards:api_v1:deck_list', request=request, format=format),
        'tags': reverse('flash_cards:api_v1:tag_list', request=request, format=format),
    })

class Cards(APIView):
    def get(self, request, format=None):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NewCardSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response([serializer.data], status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeckList(generics.ListCreateAPIView):
    queryset = Deck.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DeckSerializer

class DeckDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = DeckSerializer

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

class ReferenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reference.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ReferenceSerializer

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

# Other Stats that can be compiled from models
#     Total number questions user has completed and breakdown (from sets model)
#     Number of created/modified cards and sets from history
#     Current status on deck from the last entry on set
