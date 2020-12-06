from distutils.util import strtobool
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  mixins
from backend.utils import MultipleFieldLookupORMixin
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
    
    @csrf_exempt
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


class EventInstanceViewSet(
                        MultipleFieldLookupORMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    queryset = EventInstance.objects.all()
    serializer_class = EventInstanceSerializer
    lookup_fields = ("eventInstanceCode", "isCompleted")

    def get_object(self):
        eventInstanceCode = self.request.query_params.get("eventInstanceCode", None)
        isCompleted = self.request.query_params.get("isCompleted", None)
        if eventInstanceCode is not None:
            self.kwargs["eventInstanceCode"] = eventInstanceCode
        if isCompleted=="True" or isCompleted=="False":
            isCompleted = bool(strtobool(isCompleted))
        else:
            self.kwargs["isCompleted"] = None
        return super(EventInstanceViewSet, self).get_object()

    def get(self, request, *args, **kwargs):
        if ("isCompleted" or "eventInstanceCode") in self.request.query_params.keys():
            return self.retrieve(request, *args, **kwargs)
    
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return response
        except ObjectDoesNotExist:
            return Response({"detail": "event of specified eventCode does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)