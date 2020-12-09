from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from lms.models import Event, EventInstance
from backend.exception_classes import ModelObjectDoesNotExist, ModelObjectAlreadyExist


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
        try:
            event = Event.objects.get(eventCode=eventCode)
            validated_data["event"] = event
        except ObjectDoesNotExist:
            raise ModelObjectDoesNotExist("eventCode is invalid", code=status.HTTP_404_NOT_FOUND)

        if EventInstance.objects.filter(eventInstanceCode=validated_data["eventInstanceCode"]).exists():
            raise ModelObjectAlreadyExist(f"EventInstance already exist")

        return super(EventInstanceSerializer, self).create(validated_data)
        
