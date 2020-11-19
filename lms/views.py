from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from lms.models.event_models import Event
from lms.serializers.event_serializers import EventSerializer

# Create your views here.


class EventView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    '''
    CRUD operations for Event objects

    * Requires token authentication.
    * All users able to access this view
    '''

    queryset = Event.objects.all()
    serializer_class = EventSerializer

    
    def get(self, request, *args, **kwargs):
        """
        Return a list of events.
        """

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create an event
        """
        return self.create(request, *args, **kwargs)