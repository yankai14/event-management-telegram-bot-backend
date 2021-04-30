from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from backend.exception_classes import ModelObjectAlreadyExist
from lms.models.user_models import User, UserEnrollment
from lms.models.event_models import EventInstance


class EnrollmentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=100, write_only=True)
    eventInstanceCode = serializers.CharField(max_length=100, write_only=True)
    user = serializers.StringRelatedField()
    eventInstance = serializers.StringRelatedField()

    class Meta:
        model = UserEnrollment
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "eventInstance": {"read_only": True}}

    def create(self, validated_data):
        if self.is_valid():
            user = get_object_or_404(User, username=validated_data.get("username", None))
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=validated_data.get("eventInstanceCode", None))

            userCriteria = Q(user=user)
            eventInstanceCriteria = Q(eventInstance=eventInstance)
            if not UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists():
                enrollment = UserEnrollment.objects.create(user=user, eventInstance=eventInstance, role=validated_data.get("role"))
            else:
                raise ModelObjectAlreadyExist
        else:
            raise ValidationError(self.errors)
        return enrollment
