from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Permission
from rest_framework.exceptions import ValidationError
from lms.models.user_models import User, UserEnrollment, EventRole
from lms.models.event_models import EventInstance


class EnrollmentSerializer(serializers.Serializer):

    username = serializers.IntegerField()
    eventInstanceCode = serializers.CharField(max_length=100)
    role = serializers.ChoiceField(choices=EventRole.choices)

    def create(self, validated_data):
        if self.is_valid():
            user = get_object_or_404(User, username=validated_data.get("username", None))
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=validated_data.get("eventInstanceCode", None))
            enrollment = UserEnrollment.objects.create(user=user, eventInstance=eventInstance, role=validated_data.get("role"))
        else:
            raise ValidationError(self.errors)
        return enrollment
