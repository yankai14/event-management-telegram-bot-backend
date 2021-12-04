from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from backend.exception_classes import ModelObjectAlreadyExist
from lms.models.user_models import User
from lms.models.enrollment_models import UserEnrollment, EnrollmentStatus
from lms.models.event_models import Event, EventInstance
from lms.serializers.event_serializers import EventInstanceSerializer

# Added enrollmentStatus as read_only field

class EnrollmentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, write_only=True)
    eventInstanceCode = serializers.CharField(max_length=100, write_only=True)
    user = serializers.StringRelatedField()
    eventInstance  = EventInstanceSerializer(read_only=True)
    
    class Meta:
        model = UserEnrollment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "enrollmentStatus": {"read_only": True}}
        depth = 1
    def create(self, validated_data):
        if self.is_valid():
            user = get_object_or_404(User, username=validated_data.get("username", None))
            eventInstanceCode = validated_data.get("eventInstanceCode", None)
            if eventInstanceCode:
                testEventInstance = EventInstance.objects.filter(eventInstanceCode=eventInstanceCode)
                eventInstance = get_object_or_404(testEventInstance)

            userCriteria = Q(user=user)
            eventInstanceCriteria = Q(eventInstance=eventInstance)
            if not UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists():
                enrollment = UserEnrollment.objects.create(
                    user=user,
                    eventInstance=eventInstance,
                    role=validated_data.get("role"),
                    enrollmentStatus=EnrollmentStatus.PENDING
                )
            else:
                raise ModelObjectAlreadyExist
        else:
            raise ValidationError(self.errors)
        return enrollment
