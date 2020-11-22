from rest_framework import serializers
from lms.models import Event, EventInstance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInstance
        fields = "__all__"