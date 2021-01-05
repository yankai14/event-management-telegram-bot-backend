from rest_framework import permissions, mixins, generics
from django_filters.rest_framework import DjangoFilterBackend
from lms.views.filters.event_filter import EventFilter, EventInstanceFilter
from lms.models.event_models import Event, EventInstance
from lms.serializers.event_serializers import EventSerializer, EventInstanceSerializer

# Create your views here.


class EventViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    '''
    CRUD operations for Event objects

    * Requires token authentication.
    * All users able to access this view,
    '''

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    lookup_field = "eventCode"
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]

    def get(self, request, *args, **kwargs):
        """
        Return a list of events.
        """
        if self.request.query_params.get("eventCode", None):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create an event
        """
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update an event
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete an event
        """
        return self.destroy(request, *args, **kwargs)


class EventInstanceViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    queryset = EventInstance.objects.all()
    serializer_class = EventInstanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventInstanceFilter
    lookup_field = "eventInstanceCode"

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
    
    def get(self, request, *args, **kwargs):
        if kwargs.get("eventInstanceCode", None):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

