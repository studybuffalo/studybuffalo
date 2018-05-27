from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from flash_cards.models import Tag, Synonym
from flash_cards.serializers import TagSerializer, SynonymSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'tags': reverse('tag-list', request=request, format=format),
        'synonym': reverse('synonym-list', request=request, format=format),
    })

class TagList(APIView):
    '''List all tags, or create a new tag.'''
    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TagSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagDetail(APIView):
    '''Retrieves, updates, or deletes tag'''
    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SynonymList(APIView):
    '''List all synonym, or create a new synonym.'''
    def get(self, request, format=None):
        synonyms = Synonym.objects.all()
        serializer = SynonymSerializer(synonyms, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SynonymSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SynonymDetail(APIView):
    '''Retrieves, updates, or deletes synonym'''
    def get_object(self, pk):
        try:
            return Synonym.objects.get(pk=pk)
        except Synonym.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        synonym = self.get_object(pk)
        serializer = SynonymSerializer(synonym, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        synonym = self.get_object(pk)
        serializer = SynonymSerializer(synonym, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        synonym = self.get_object(pk)
        synonym.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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
