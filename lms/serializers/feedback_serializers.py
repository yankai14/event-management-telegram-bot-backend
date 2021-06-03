from rest_framework import serializers
from lms.models.feedback_models import EventInstanceFeedback
from lms.models.user_models import UserEnrollment
from lms.models.event_models import EventInstance, Event
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from backend.exception_classes import ModelObjectAlreadyExist


class EventInstanceFeedbackSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, write_only=True)
    eventInstanceCode = serializers.CharField(max_length=100, write_only=True)    
    userEnrollment = serializers.StringRelatedField()
    eventInstance = serializers.StringRelatedField()

    class Meta:
        model = EventInstanceFeedback
        fields = ['userEnrollment','eventInstance','eventInstanceFeedback','date_created','eventInstanceCode','username']
        "__all__"
        extra_kwargs = {
            "userEnrollment" : {"read_only":True},
            "eventInstance" : {"read_only":True},
        }

    def create(self,validated_data):
        if self.is_valid():
            user = get_object_or_404(UserEnrollment, user__username=validated_data.get('username',None))
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=validated_data.get("eventInstanceCode", None))

        else:
            raise ValidationError(self.errors)
        
        return EventInstanceFeedback.objects.create(userEnrollment=user, eventInstance=eventInstance)


