import json
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions, mixins
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
    lookup_field = "eventCode"

    def get_object(self):
        eventCode = self.request.query_params.get("eventCode", None)
        if eventCode is not None:
            self.kwargs["eventCode"] = eventCode
        return super(EventViewSet, self).get_object()
    
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
                        generics.GenericAPIView):

    queryset = Event.objects.all()
    serializer_class = EventInstanceSerializer
    lookup_field = "eventInstanceCode"

    def get_object(self):
        eventInstanceCode = self.request.query_params.get("eventInstanceCode", None)
        if eventInstanceCode is not None:
            self.kwargs["eventInstanceCode"] = eventInstanceCode
        return super(EventInstanceViewSet, self).get_object()

    def get(self, request, *args, **kwargs):
        if self.request.query_params.get("eventCode", None):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        eventCode = request.query_params.get("eventCode", None)
        if eventCode is not None:
            event = get_object_or_404(Event, eventCode=eventCode)
            request.data["event"] = event

        eventInstance = EventInstance.objects.create(**request.data)
        responseData = EventInstanceSerializer(eventInstance).data
        return Response(data=responseData, status=status.HTTP_201_CREATED)