from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics

from rdrhc_calendar.models import CalendarUser

from rdrhc_calendar.api.serializers import UserSerializer

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def api_root(request, format=None): # pylint: disable=redefined-builtin
    return Response({
        'users': reverse('rdrhc_calendar:api_v1:user_list', request=request, format=format),
    })

class UserList(generics.ListCreateAPIView):
    queryset = CalendarUser.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarUser.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    lookup_field = 'id'
