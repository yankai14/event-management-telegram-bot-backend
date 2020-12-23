from distutils.util import strtobool
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, mixins, generics, viewsets
from rest_framework.response import Response
from lms.models.event_models import Event, EventInstance
from lms.serializers.event_serializers import EventSerializer, EventInstanceSerializer
from backend.exception_classes import InvalidQueryStringParameter, ModelObjectDoesNotExist

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
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]

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


class EventInstanceViewSet(viewsets.GenericViewSet):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
    
    def list(self, request, *args, **kwargs):
        event = request.query_params.get("event", None)
        isCompleted =request.query_params.get("isCompleted", None)
        if event and isCompleted is not None:
            try:
                isCompleted = bool(strtobool(isCompleted))
            except ValueError:
                raise InvalidQueryStringParameter("Invalid isCompleted parameter")
            queryset = EventInstance.objects.filter(isCompleted=isCompleted, event__eventCode=event)
        elif event:
            queryset = EventInstance.objects.filter(event__eventCode=event)
        elif isCompleted is not None:
            try:
                isCompleted = bool(strtobool(isCompleted))
            except ValueError:
                raise InvalidQueryStringParameter("Invalid isCompleted parameter")
            queryset = EventInstance.objects.filter(isCompleted=isCompleted)
        else:
            queryset = EventInstance.objects.all()

        serializer = EventInstanceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        eventInstanceCode = kwargs["eventInstanceCode"]
        try:
            queryset = EventInstance.objects.get(eventInstanceCode=eventInstanceCode)
        except ObjectDoesNotExist:
            raise ModelObjectDoesNotExist("eventInstanceCode does not exist")
        serializer = EventInstanceSerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        serializer = EventInstanceSerializer(payload)
        validatedData = serializer.data
        serializer.create(validated_data=validatedData, eventCode=payload["eventCode"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        try:
            eventInstance = EventInstance.objects.get(eventInstanceCode=eventInstanceCode)
        except ObjectDoesNotExist:
            raise ModelObjectDoesNotExist("eventInstanceCode does not exist")
        eventInstance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
