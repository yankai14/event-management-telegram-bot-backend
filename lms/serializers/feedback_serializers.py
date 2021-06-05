from rest_framework import serializers
from lms.models.feedback_models import EventInstanceFeedback
from lms.models.user_models import UserEnrollment
from lms.models.event_models import EventInstance, Event
from lms.serializers.enrollment_serializers import EnrollmentSerializer
from lms.serializers.event_serializers import EventInstanceSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from backend.exception_classes import ModelObjectAlreadyExist


class EventInstanceFeedbackSerializer(serializers.ModelSerializer):

    userEnrollment = EnrollmentSerializer(read_only=True)
    eventInstance = EventInstanceSerializer(read_only=True)

    username = serializers.CharField(max_length=200, write_only=True)
    eventInstanceCode = serializers.CharField(max_length=200, write_only=True)
    eventInstanceFeedback = serializers.CharField()

    class Meta:
        model = EventInstanceFeedback
        fields = "__all__"
        extra_kwargs = {"userEnrollment": {"read_only": True}, "eventInstance": {"read_only": True}}

    def create(self, validated_data):
        if self.is_valid():
            username = validated_data.get("username")
            eventInstanceCode = validated_data.get("eventInstanceCode")
            eventInstanceFeedback = validated_data.get("eventInstanceFeedback")

            userEnrollment = get_object_or_404(UserEnrollment, user__username=username)
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=eventInstanceCode)
            
            eventFeedback = EventInstanceFeedback.objects.create(userEnrollment=userEnrollment, eventInstance=eventInstance, eventInstanceFeedback=eventInstanceFeedback)
        
        return eventFeedback
            



