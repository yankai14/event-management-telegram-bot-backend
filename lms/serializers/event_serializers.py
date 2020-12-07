from rest_framework import serializers
from lms.models import Event, EventInstance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventInstanceSerializer(serializers.ModelSerializer):

    event = serializers.StringRelatedField()

    class Meta:
        model = EventInstance
        fields = "__all__"
        extra_kwargs = {"eventCode": {"read_only": True}}

    def create(self, validated_data, eventCode):
        event = Event.objects.get(eventCode=eventCode)
        validated_data["event"] = event
        return super(EventInstanceSerializer, self).create(validated_data)
