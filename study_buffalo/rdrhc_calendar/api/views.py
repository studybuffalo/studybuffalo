from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics

from rdrhc_calendar.models import CalendarUser, ShiftCode

from rdrhc_calendar.api.serializers import UserSerializer

@api_view(['GET'])
@authentication_classes((TokenAuthentication))
@permission_classes((IsAuthenticated, ))
def api_root(request, format=None): # pylint: disable=redefined-builtin
    return Response({
        'users': reverse('rdrhc_calendar:api_v1:user_list', request=request, format=format),
    })

class UserList(generics.ListCreateAPIView):
    queryset = CalendarUser.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CalendarUser.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    lookup_field = 'id'

class UserShiftCodesList(generics.ListCreateAPIView):
    queryset = ShiftCode.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    lookup_field = 'id'
