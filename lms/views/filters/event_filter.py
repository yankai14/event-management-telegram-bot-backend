import django_filters
from django_filters.rest_framework import FilterSet
from lms.models.event_models import Event, EventInstance, EventInstanceFolder, EventInstanceFolderPermissions


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ["id", "eventCode", "name"]


class EventInstanceFilter(FilterSet):
    event = django_filters.CharFilter(
        field_name="event__eventCode", 
        lookup_expr="exact"
    )

    isOpenForSignUps = django_filters.BooleanFilter(
        field_name="isOpenForSignUps",
        lookup_expr="exact"
    )
    class Meta:
        model = EventInstance
        fields =  ["id", "event", "eventInstanceCode", "isCompleted"]


class EventInstanceFolderFilter(FilterSet):
    eventInstance = django_filters.CharFilter(
        field_name="eventInstance__eventInstanceCode",
        lookup_expr="exact"
    )

    class Meta:
        model = EventInstanceFolder
        fields = ["id", "folderId", "folderName"]


class EventInstanceFolderPermissionsFilter(FilterSet):
    user = django_filters.CharFilter(
        field_name = "user__username",
        lookup_expr="exact"
    )

    folder = django_filters.CharFilter(
        field_name="folder__folderId"
    )

    class Meta:
        model = EventInstanceFolderPermissions
        fields = ["id", "permissionId", "folderRole"]

