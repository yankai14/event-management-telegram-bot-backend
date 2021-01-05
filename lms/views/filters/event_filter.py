import django_filters
from django_filters.rest_framework import FilterSet
from lms.models.event_models import Event, EventInstance


class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ["id", "eventCode", "name"]


class EventInstanceFilter(FilterSet):
    event = django_filters.CharFilter(
        field_name="event__eventCode", 
        lookup_expr="exact"
    )

    class Meta:
        model = EventInstance
        fields =  ["id", "event", "eventInstanceCode", "isCompleted"]