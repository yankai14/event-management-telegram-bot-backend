from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from backend.exception_classes import ModelObjectAlreadyExist
from lms.models.user_models import User
from lms.models.enrollment_models import EnrollmentStatus, UserEnrollment
from lms.models.event_models import EventInstance
from lms.serializers.user_serializers import UserSerializer
from lms.serializers.event_serializers import EventInstanceSerializer


class EnrollmentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, write_only=True)
    eventInstanceCode = serializers.CharField(max_length=100, write_only=True)
    user = UserSerializer(read_only=True)
    eventInstance = EventInstanceSerializer(read_only=True)
    role = serializers.IntegerField()
    status = serializers.IntegerField()

    class Meta:
        model = UserEnrollment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True},
                        "eventInstance": {"read_only": True}}

    def create(self, validated_data):
        if self.is_valid():
            user = get_object_or_404(
                User, username=validated_data.get("username", None))
            eventInstance = get_object_or_404(
                EventInstance, eventInstanceCode=validated_data.get("eventInstanceCode", None))

            userCriteria = Q(user=user)
            eventInstanceCriteria = Q(eventInstance=eventInstance)
            if not UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists():
                enrollment = UserEnrollment.objects.create(
                    user=user,
                    eventInstance=eventInstance,
                    role=validated_data.get("role"),
                    status=EnrollmentStatus.PENDING
                )
            else:
                raise ModelObjectAlreadyExist
        else:
            raise ValidationError(self.errors)
        return enrollment
