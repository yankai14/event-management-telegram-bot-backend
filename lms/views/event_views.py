from rest_framework import permissions, mixins, generics
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from lms.views.filters.event_filter import EventFilter, EventInstanceFilter, EventInstanceFolderFilter, EventInstanceFolderPermissionsFilter
from lms.models.event_models import Event, EventInstance, EventInstanceFolder, EventInstanceFolderPermissions
from lms.serializers.event_serializers import EventInstanceFolderPermissionsSerializer, EventSerializer, EventInstanceSerializer, EventInstanceFolderSerializer, EventInstanceFolderPermissions
from lms.utils.drive_service import GDriveService
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
        if kwargs.get("eventInstanceCode"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventInstanceFolderViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    queryset = EventInstanceFolder.objects.all()
    serializer_class = EventInstanceFolderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventInstanceFolderFilter
    lookup_field = "folderId"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # Overwrite destroy method to integrate GDriveService
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        GDriveService.delete_file_or_folder(self.kwargs.get('folderId'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class EventInstanceFolderPermissionsViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    queryset = EventInstanceFolderPermissions.objects.all()
    serializer_class = EventInstanceFolderPermissionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventInstanceFolderPermissionsFilter
    lookup_field = "permissionId"

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # Overwrite destroy method to integrate GDriveService
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        GDriveService.delete_permission(self.kwargs.get('permissionId'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)