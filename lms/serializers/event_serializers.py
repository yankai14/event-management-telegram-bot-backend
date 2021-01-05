from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from lms.models import Event, EventInstance
from backend.exception_classes import ModelObjectAlreadyExist


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventInstanceSerializer(serializers.ModelSerializer):

    event = serializers.StringRelatedField()
    eventCode = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = EventInstance
        fields = "__all__"
        

    def create(self, validated_data):
        if self.is_valid():
            event = get_object_or_404(Event, eventCode=validated_data.get("eventCode"))
            if EventInstance.objects.filter(eventInstanceCode=validated_data["eventInstanceCode"]).exists():
                raise ModelObjectAlreadyExist(f"EventInstance already exist")
        else:

            raise ValidationError(self.errors)
        return event
        
